import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')
import yfinance as yf
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

class SentimentLevel(Enum):
    """Enum for sentiment levels"""
    BEARISH = "Bearish"
    SOMEWHAT_BEARISH = "Somewhat-Bearish"
    NEUTRAL = "Neutral"
    SOMEWHAT_BULLISH = "Somewhat-Bullish"
    BULLISH = "Bullish"

@dataclass
class SentimentInterpretation:
    """Data class for sentiment interpretation"""
    signal: str
    confidence: str
    explanation: str
    risk_level: str
    action: str
    color_code: str
    icon: str 

class SentimentalAnalysis:
    def __init__(self, api_key: Optional[str] = None, cache_duration: int = 30):
        """
        Initialize Sentiment Analysis class
        """
        self.api_key = api_key or ALPHA_VANTAGE_API_KEY
        if not self.api_key:
            raise ValueError("API key not provided. Set ALPHA_VANTAGE_API_KEY environment variable or pass api_key parameter.")
        
        self.cache_duration = cache_duration
        self.cache = {}
        self.last_fetch_time = {}
        
        
        self.session = self._create_session()
        
    def _create_session(self):
        """Create a requests session with retry logic"""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,  # Total number of retries
            backoff_factor=1,  # Wait 1, 2, 4 seconds between retries
            status_forcelist=[429, 500, 502, 503, 504],  # Retry on these status codes
            allowed_methods=["HEAD", "GET", "OPTIONS"]  # Updated from method_whitelist
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
        
    def _is_cache_valid(self, ticker: str) -> bool:
        """Check if cached data is still valid"""
        if ticker not in self.cache:
            return False
        
        last_fetch = self.last_fetch_time.get(ticker)
        if not last_fetch:
            return False
        
        return (datetime.now() - last_fetch).seconds < (self.cache_duration * 60)
    
    def get_sentiment_info(self, ticker: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get sentiment information for a ticker with improved error handling
        
        """
        # Check cache first
        if use_cache and self._is_cache_valid(ticker):
            logger.info(f"Returning cached data for {ticker}")
            return self.cache[ticker]
        
        # Try multiple times with increasing timeouts
        timeouts = [10, 20, 30]
        last_error = None
        
        for attempt, timeout in enumerate(timeouts):
            try:
                logger.info(f"Fetching sentiment data for {ticker} (attempt {attempt + 1}/{len(timeouts)}, timeout={timeout}s)")
                
                # Make API request with session (includes retry logic)
                url = 'https://www.alphavantage.co/query'
                params = {
                    'function': 'NEWS_SENTIMENT',
                    'tickers': ticker,
                    'apikey': self.api_key,
                    'limit': 50  # Limit to reduce response size and time
                }
                
                response = self.session.get(url, params=params, timeout=timeout)
                response.raise_for_status()
                
                data = response.json()
                
                # Check for API errors
                if 'Error Message' in data:
                    error_msg = f"API Error: {data['Error Message']}"
                    logger.error(error_msg)
                    # Don't retry for API errors
                    return self._get_empty_response(ticker, error_msg)
                    
                if 'Note' in data:
                    # Rate limit hit
                    logger.warning(f"Rate limit hit for {ticker}: {data['Note']}")
                    # Return cached data if available
                    if ticker in self.cache:
                        logger.info(f"Returning cached data due to rate limit")
                        return self.cache[ticker]
                    return self._get_empty_response(ticker, "API rate limit reached")
                
                # Process the data
                processed_data = self._process_sentiment_data(data, ticker)
                
                # Cache the results
                self.cache[ticker] = processed_data
                self.last_fetch_time[ticker] = datetime.now()
                
                logger.info(f"Successfully fetched sentiment data for {ticker}")
                return processed_data
                
            except requests.exceptions.Timeout:
                last_error = f"Request timed out after {timeout} seconds"
                logger.warning(f"Timeout for {ticker}: {last_error}")
                
            except requests.exceptions.ConnectionError as e:
                last_error = f"Connection error: {str(e)}"
                logger.error(f"Connection error for {ticker}: {last_error}")
                
            except requests.exceptions.RequestException as e:
                last_error = f"Request failed: {str(e)}"
                logger.error(f"Request exception for {ticker}: {last_error}")
                
            except Exception as e:
                last_error = f"Unexpected error: {str(e)}"
                logger.error(f"Unexpected error for {ticker}: {last_error}")
            
            # If not the last attempt, wait before retrying
            if attempt < len(timeouts) - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1, 2, 4 seconds
                logger.info(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
        
        # All attempts failed
        logger.error(f"All attempts failed for {ticker}. Last error: {last_error}")
        
        # Return cached data if available
        if ticker in self.cache:
            logger.info(f"Returning stale cached data for {ticker}")
            cached_data = self.cache[ticker]
            cached_data['stale'] = True
            cached_data['error'] = last_error
            return cached_data
        
        # Return empty response
        return self._get_empty_response(ticker, last_error)
    
    def _get_empty_response(self, ticker: str, error_message: str = "") -> Dict[str, Any]:
        """Return empty response structure when API fails"""
        logger.info(f"Returning empty response for {ticker}")
        return {
            'ticker': ticker,
            'items_count': '0',
            'articles': [],
            'aggregate_metrics': {
                'average_sentiment': 0,
                'sentiment_trend': 'Unknown',
                'confidence_level': 'Low',
                'articles_analyzed': 0,
                'ticker_mentions': 0,
                'recommendation': 'No data available',
                'interpretation': self.interpret_sentiment(0)
            },
            'last_updated': datetime.now().isoformat(),
            'error': error_message,
            'stale': False
        }
    
    # Keep all other methods the same as they are...
    def _process_sentiment_data(self, data: Dict, ticker: str) -> Dict[str, Any]:
        """Process raw API data into structured format"""
        articles = []
        
        for article in data.get('feed', []):
            # Extract ticker-specific sentiment
            ticker_sentiments = []
            for ts in article.get('ticker_sentiment', []):
                analyzed_sentiment = self.analyze_ticker_sentiment(ts)
                ticker_sentiments.append(analyzed_sentiment)
            
            # Process article
            processed_article = {
                'title': article.get('title', ''),
                'url': article.get('url', ''),
                'time_published': self._format_timestamp(article.get('time_published', '')),
                'authors': article.get('authors', []),
                'summary': article.get('summary', ''),
                'banner_image': article.get('banner_image', ''),
                'source': article.get('source', ''),
                'source_domain': article.get('source_domain', ''),
                'category': article.get('category_within_source', 'n/a'),
                'topics': article.get('topics', []),
                'overall_sentiment_score': float(article.get('overall_sentiment_score', 0)),
                'overall_sentiment_label': article.get('overall_sentiment_label', 'Neutral'),
                'ticker_sentiments': ticker_sentiments,
                'relevance_to_ticker': self._calculate_ticker_relevance(article, ticker)
            }
            
            # Add overall interpretation
            overall_interpretation = self.interpret_sentiment(
                processed_article['overall_sentiment_score']
            )
            processed_article['overall_interpretation'] = overall_interpretation
            
            articles.append(processed_article)
        
        # Sort articles by relevance and recency
        articles.sort(key=lambda x: (x['relevance_to_ticker'], x['time_published']), reverse=True)
        
        # Calculate aggregate metrics
        aggregate_metrics = self._calculate_aggregate_metrics(articles, ticker)
        
        return {
            'ticker': ticker,
            'items_count': data.get('items', '0'),
            'articles': articles,
            'aggregate_metrics': aggregate_metrics,
            'last_updated': datetime.now().isoformat(),
            'stale': False
        }
    
    def _format_timestamp(self, timestamp: str) -> str:
        """Format timestamp to readable format"""
        try:
            dt = datetime.strptime(timestamp, '%Y%m%dT%H%M%S')
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return timestamp
    
    def _calculate_ticker_relevance(self, article: Dict, ticker: str) -> float:
        """Calculate how relevant an article is to the specific ticker"""
        ticker_sentiments = article.get('ticker_sentiment', [])
        for ts in ticker_sentiments:
            if ts.get('ticker') == ticker:
                return float(ts.get('relevance_score', 0))
        return 0.0
    
    def interpret_sentiment(self, score: float) -> SentimentInterpretation:
        """Provide detailed interpretation of sentiment score"""
        if score >= 0.35:
            return SentimentInterpretation(
                signal='STRONG BUY',
                confidence='High',
                explanation='Very positive sentiment indicates strong bullish market opinion',
                risk_level='Moderate',
                action='Consider buying, but verify with technical analysis and fundamental analysis',
                color_code='#00C851',  # Green
                icon='trending_up'
            )
        elif score >= 0.15:
            return SentimentInterpretation(
                signal='BUY',
                confidence='Medium',
                explanation='Positive sentiment suggests favorable market conditions',
                risk_level='Moderate',
                action='Good entry point for long-term positions',
                color_code='#33B5E5',  # Light Blue
                icon='arrow_upward'
            )
        elif score <= -0.35:
            return SentimentInterpretation(
                signal='STRONG SELL',
                confidence='High',
                explanation='Very negative sentiment indicates bearish market opinion',
                risk_level='High',
                action='Consider selling or avoiding new positions',
                color_code='#FF4444',  # Red
                icon='trending_down'
            )
        elif score <= -0.15:
            return SentimentInterpretation(
                signal='SELL',
                confidence='Medium',
                explanation='Negative sentiment suggests caution',
                risk_level='Moderate-High',
                action='Review positions and consider reducing exposure',
                color_code='#FF8800',  # Orange
                icon='arrow_downward'
            )
        else:
            return SentimentInterpretation(
                signal='HOLD',
                confidence='Low',
                explanation='Neutral sentiment indicates market uncertainty',
                risk_level='Low',
                action='Wait for clearer signals before making moves',
                color_code='#FFBB33',  # Yellow
                icon='remove'
            )
    
    def analyze_ticker_sentiment(self, ticker_sentiment: Dict) -> Dict[str, Any]:
        """Analyze individual ticker sentiment"""
        sentiment_score = float(ticker_sentiment.get('ticker_sentiment_score', 0))
        relevance_score = float(ticker_sentiment.get('relevance_score', 0))
        
        interpretation = self.interpret_sentiment(sentiment_score)
        
        return {
            'ticker': ticker_sentiment.get('ticker', ''),
            'sentiment_score': sentiment_score,
            'sentiment_label': ticker_sentiment.get('ticker_sentiment_label', 'Neutral'),
            'relevance_score': relevance_score,
            'relevance_interpretation': self._interpret_relevance(relevance_score),
            'signal': interpretation.signal,
            'confidence': interpretation.confidence,
            'explanation': interpretation.explanation,
            'risk_level': interpretation.risk_level,
            'action': interpretation.action,
            'color_code': interpretation.color_code,
            'icon': interpretation.icon,
            'weight': self._calculate_signal_weight(sentiment_score, relevance_score)
        }
    
    def _interpret_relevance(self, relevance_score: float) -> str:
        """Interpret relevance score"""
        if relevance_score > 0.7:
            return 'High'
        elif relevance_score > 0.4:
            return 'Medium'
        else:
            return 'Low'
    
    def _calculate_signal_weight(self, sentiment_score: float, relevance_score: float) -> float:
        """Calculate weighted signal strength based on sentiment and relevance"""
        return abs(sentiment_score) * relevance_score
    
    def _calculate_aggregate_metrics(self, articles: List[Dict], ticker: str) -> Dict[str, Any]:
        """Calculate aggregate sentiment metrics across all articles"""
        if not articles:
            return {
                'average_sentiment': 0,
                'sentiment_trend': 'Neutral',
                'confidence_level': 'Low',
                'articles_analyzed': 0,
                'recommendation': 'Insufficient data'
            }
        
        # Calculate weighted average sentiment
        total_weight = 0
        weighted_sentiment = 0
        ticker_specific_sentiments = []
        
        for article in articles:
            for ts in article['ticker_sentiments']:
                if ts['ticker'] == ticker:
                    weight = ts['weight']
                    weighted_sentiment += ts['sentiment_score'] * weight
                    total_weight += weight
                    ticker_specific_sentiments.append(ts['sentiment_score'])
        
        avg_sentiment = weighted_sentiment / total_weight if total_weight > 0 else 0
        
        # Calculate sentiment trend (looking at time-based changes)
        sentiment_trend = self._calculate_sentiment_trend(articles, ticker)
        
        # Determine confidence level
        confidence_level = self._determine_confidence_level(
            len(ticker_specific_sentiments),
            np.std(ticker_specific_sentiments) if ticker_specific_sentiments else 0
        )
        
        # Get overall recommendation
        overall_interpretation = self.interpret_sentiment(avg_sentiment)
        
        return {
            'average_sentiment': round(avg_sentiment, 4),
            'sentiment_trend': sentiment_trend,
            'confidence_level': confidence_level,
            'articles_analyzed': len(articles),
            'ticker_mentions': len(ticker_specific_sentiments),
            'recommendation': overall_interpretation.signal,
            'interpretation': overall_interpretation
        }
    
    def _calculate_sentiment_trend(self, articles: List[Dict], ticker: str) -> str:
        """Calculate if sentiment is improving or declining over time"""
        # This is a simplified version - you could make it more sophisticated
        if len(articles) < 2:
            return 'Insufficient data'
        
        # Get recent vs older sentiments
        recent_sentiments = []
        older_sentiments = []
        
        mid_point = len(articles) // 2
        
        for i, article in enumerate(articles):
            for ts in article['ticker_sentiments']:
                if ts['ticker'] == ticker:
                    if i < mid_point:
                        recent_sentiments.append(ts['sentiment_score'])
                    else:
                        older_sentiments.append(ts['sentiment_score'])
        
        if not recent_sentiments or not older_sentiments:
            return 'Insufficient data'
        
        recent_avg = np.mean(recent_sentiments)
        older_avg = np.mean(older_sentiments)
        
        if recent_avg > older_avg + 0.1:
            return 'Improving'
        elif recent_avg < older_avg - 0.1:
            return 'Declining'
        else:
            return 'Stable'
    
    def _determine_confidence_level(self, sample_size: int, std_dev: float) -> str:
        """Determine confidence level based on sample size and consistency"""
        if sample_size < 5:
            return 'Low'
        elif sample_size < 10:
            if std_dev < 0.2:
                return 'Medium'
            else:
                return 'Low'
        else:
            if std_dev < 0.15:
                return 'High'
            elif std_dev < 0.25:
                return 'Medium'
            else:
                return 'Low'
    
    def get_sentiment_summary(self, ticker: str) -> Dict[str, Any]:
        """Get a summary of sentiment analysis for quick display"""
        try:
            data = self.get_sentiment_info(ticker)
            
            # Check if we have an error
            if 'error' in data and data.get('articles', []) == []:
                return {
                    'ticker': ticker,
                    'recommendation': 'HOLD',
                    'average_sentiment': 0,
                    'confidence': 'Low',
                    'trend': 'Unknown',
                    'last_updated': data.get('last_updated', datetime.now().isoformat()),
                    'quick_summary': 'Unable to fetch sentiment data. Please try again later.',
                    'error': data.get('error', ''),
                    'stale': data.get('stale', False)
                }
            
            aggregate = data['aggregate_metrics']
            
            return {
                'ticker': ticker,
                'recommendation': aggregate['recommendation'],
                'average_sentiment': aggregate['average_sentiment'],
                'confidence': aggregate['confidence_level'],
                'trend': aggregate['sentiment_trend'],
                'last_updated': data['last_updated'],
                'quick_summary': self._generate_quick_summary(aggregate),
                'stale': data.get('stale', False)
            }
        except Exception as e:
            logger.error(f"Error in get_sentiment_summary for {ticker}: {str(e)}")
            return {
                'ticker': ticker,
                'recommendation': 'HOLD',
                'average_sentiment': 0,
                'confidence': 'Low',
                'trend': 'Unknown',
                'last_updated': datetime.now().isoformat(),
                'quick_summary': 'Unable to analyze sentiment',
                'error': str(e)
            }
    
    def _generate_quick_summary(self, metrics: Dict) -> str:
        """Generate a human-readable quick summary"""
        sentiment = metrics['average_sentiment']
        trend = metrics['sentiment_trend']
        confidence = metrics['confidence_level']
        
        if sentiment > 0.15:
            tone = "positive"
        elif sentiment < -0.15:
            tone = "negative"
        else:
            tone = "neutral"
        
        return f"Market sentiment is {tone} with {confidence.lower()} confidence. Trend is {trend.lower()}."