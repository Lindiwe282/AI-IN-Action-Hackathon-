from flask import Blueprint, jsonify, request
import logging
from functools import wraps
from collections import defaultdict
import time

logger = logging.getLogger(__name__)

sentiment_bp = Blueprint('sentiment', __name__, url_prefix='/api/sentiment')

# Rate limiting storage
rate_limit_storage = defaultdict(list)

def rate_limit(max_calls=10, time_window=60):
    """Rate limit decorator"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time.time()
            
            # Clean old entries
            rate_limit_storage[client_ip] = [
                timestamp for timestamp in rate_limit_storage[client_ip]
                if current_time - timestamp < time_window
            ]
            
            # Check rate limit
            if len(rate_limit_storage[client_ip]) >= max_calls:
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'retry_after': time_window
                }), 429
            
            # Add current request
            rate_limit_storage[client_ip].append(current_time)
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

@sentiment_bp.route('/news/<ticker>', methods=['GET'])
@rate_limit(max_calls=10, time_window=60)
def get_news_articles(ticker):
    """Get news articles with sentiment for a ticker"""
    try:
        # Import here to avoid circular imports
        from app_portfolio import sentiment_analyzer
        
        # Clean ticker
        ticker = ticker.strip().upper()
        if not ticker:
            return jsonify({'error': 'Invalid ticker symbol'}), 400
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        per_page = min(per_page, 50)  # Limit max articles per page
        
        # Get sentiment data
        sentiment_data = sentiment_analyzer.get_sentiment_info(ticker)
        
        # Check if we have an error but still some data (stale cache)
        if sentiment_data.get('error'):
            logger.warning(f"Sentiment API error for {ticker}: {sentiment_data['error']}")
            if sentiment_data.get('stale'):
                # Add a warning to the response
                sentiment_data['warning'] = 'Using cached data due to API issues'
        
        articles = sentiment_data.get('articles', [])
        
        # Prepare articles in the format you want
        formatted_articles = []
        for article in articles:
            formatted_articles.append({
                'title': article.get('title', ''),
                'url': article.get('url', ''),
                'time_published': article.get('time_published', ''),
                'authors': article.get('authors', []),
                'summary': article.get('summary', ''),
                'banner_image': article.get('banner_image', ''),
                'source': article.get('source', ''),
                'topics': article.get('topics', []),
                'overall_sentiment_score': article.get('overall_sentiment_score', 0),
                'overall_sentiment_label': article.get('overall_sentiment_label', ''),
                'ticker_sentiments': article.get('ticker_sentiments', [])
            })
        
        # Pagination
        total_articles = len(formatted_articles)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_articles = formatted_articles[start_idx:end_idx]
        
        response_data = {
            'success': True,
            'ticker': ticker,
            'articles': paginated_articles,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_articles,
                'pages': (total_articles + per_page - 1) // per_page if per_page > 0 else 0
            },
            'aggregate_sentiment': sentiment_data.get('aggregate_metrics', {})
        }
        
        # Add warning if using stale data
        if sentiment_data.get('warning'):
            response_data['warning'] = sentiment_data['warning']
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error fetching news articles: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to fetch news articles',
            'ticker': ticker,
            'articles': [],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': 0,
                'pages': 0
            },
            'aggregate_sentiment': {
                'average_sentiment': 0,
                'articles_analyzed': 0,
                'sentiment_trend': 'neutral',
                'confidence_level': 'Low'
            }
        }), 500

@sentiment_bp.route('/article-analysis', methods=['POST'])
def analyze_article():
    """Analyze a specific article - for the modal popup"""
    try:
        # Import here to avoid circular imports
        from app_portfolio import sentiment_analyzer
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Get the article data from frontend
        article = data.get('article', {})
        if not article:
            return jsonify({'error': 'No article data provided'}), 400
        
        # Prepare detailed analysis for the modal
        detailed_analysis = {
            'article_info': {
                'title': article.get('title', ''),
                'url': article.get('url', ''),
                'source': article.get('source', ''),
                'authors': article.get('authors', []),
                'published': article.get('time_published', ''),
                'summary': article.get('summary', '')
            },
            'sentiment_overview': {
                'overall_score': article.get('overall_sentiment_score', 0),
                'overall_label': article.get('overall_sentiment_label', ''),
                'interpretation': sentiment_analyzer.interpret_sentiment(
                    article.get('overall_sentiment_score', 0)
                ).__dict__  # Convert to dict for JSON serialization
            },
            'ticker_analysis': []
        }
        
        # Analyze each ticker mentioned in the article
        # Check both 'ticker_sentiments' and 'ticker_sentiment' for compatibility
        ticker_sentiments = article.get('ticker_sentiments', []) or article.get('ticker_sentiment', [])
        
        for ticker_sentiment in ticker_sentiments:
            # Make sure we have the actual sentiment score
            sentiment_score = float(ticker_sentiment.get('ticker_sentiment_score', 0) or ticker_sentiment.get('sentiment_score', 0))
            relevance_score = float(ticker_sentiment.get('relevance_score', 0))
            
            # Create proper sentiment data
            sentiment_data = {
                'ticker': ticker_sentiment.get('ticker', ''),
                'ticker_sentiment_score': sentiment_score,
                'ticker_sentiment_label': ticker_sentiment.get('ticker_sentiment_label', ticker_sentiment.get('sentiment_label', 'Neutral')),
                'relevance_score': relevance_score
            }
            
            ticker_analysis = sentiment_analyzer.analyze_ticker_sentiment(sentiment_data)
            
            # Add visual indicators for the UI
            ticker_analysis['visual'] = {
                'color': ticker_analysis['color_code'],
                'icon': ticker_analysis['icon'],
                'should_invest': ticker_analysis['signal'] in ['BUY', 'STRONG BUY'],
                'risk_color': {
                    'Low': '#00C851',
                    'Moderate': '#FFBB33',
                    'Moderate-High': '#FF8800',
                    'High': '#FF4444'
                }.get(ticker_analysis['risk_level'], '#FFBB33')
            }
            
            detailed_analysis['ticker_analysis'].append(ticker_analysis)
        
        # Sort tickers by relevance score
        detailed_analysis['ticker_analysis'].sort(
            key=lambda x: x['relevance_score'], 
            reverse=True
        )
        
        # Add investment summary
        buy_signals = [t for t in detailed_analysis['ticker_analysis'] 
                      if t['signal'] in ['BUY', 'STRONG BUY']]
        sell_signals = [t for t in detailed_analysis['ticker_analysis'] 
                       if t['signal'] in ['SELL', 'STRONG SELL']]
        
        detailed_analysis['investment_summary'] = {
            'total_tickers': len(detailed_analysis['ticker_analysis']),
            'buy_signals': len(buy_signals),
            'sell_signals': len(sell_signals),
            'hold_signals': len(detailed_analysis['ticker_analysis']) - len(buy_signals) - len(sell_signals),
            'top_pick': buy_signals[0] if buy_signals else None,
            'avoid': sell_signals[0] if sell_signals else None
        }
        
        return jsonify({
            'success': True,
            'analysis': detailed_analysis
        })
        
    except Exception as e:
        logger.error(f"Error analyzing article: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to analyze article'
        }), 500

@sentiment_bp.route('/ticker-summary/<ticker>', methods=['GET'])
def get_ticker_sentiment_summary(ticker):
    """Get sentiment summary for a specific ticker - for header display"""
    try:
        # Import here to avoid circular imports
        from app_portfolio import sentiment_analyzer
        
        # Clean ticker
        ticker = ticker.strip().upper()
        if not ticker:
            return jsonify({'error': 'Invalid ticker symbol'}), 400
        
        # Get sentiment summary
        summary = sentiment_analyzer.get_sentiment_summary(ticker)
        
        return jsonify({
            'success': True,
            'data': {
                'ticker': ticker,
                'average_sentiment': summary.get('average_sentiment', 0),
                'recommendation': summary.get('recommendation', 'HOLD'),
                'confidence': summary.get('confidence', 'Low'),
                'trend': summary.get('trend', 'Stable'),
                'summary': summary.get('quick_summary', 'No data available')
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting ticker sentiment summary: {str(e)}")
        return jsonify({
            'success': True,  # Return success with default values
            'data': {
                'ticker': ticker,
                'average_sentiment': 0,
                'recommendation': 'HOLD',
                'confidence': 'Low',
                'trend': 'Stable',
                'summary': 'Unable to fetch sentiment data'
            }
        })

@sentiment_bp.route('/article-tickers', methods=['POST'])
def get_article_ticker_sentiments():
    """Get detailed ticker sentiments from an article"""
    try:
        # Import here to avoid circular imports
        from app_portfolio import sentiment_analyzer
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        article = data.get('article', {})
        if not article:
            return jsonify({'error': 'No article data provided'}), 400
        
        # Extract ticker sentiments from the article
        ticker_sentiments = article.get('ticker_sentiment', [])
        analyzed_sentiments = []
        
        for ts in ticker_sentiments:
            # Get the actual sentiment score from the API data
            sentiment_score = float(ts.get('ticker_sentiment_score', 0))
            relevance_score = float(ts.get('relevance_score', 0))
            
            # Analyze the sentiment
            analysis = sentiment_analyzer.analyze_ticker_sentiment({
                'ticker': ts.get('ticker', ''),
                'ticker_sentiment_score': sentiment_score,
                'ticker_sentiment_label': ts.get('ticker_sentiment_label', 'Neutral'),
                'relevance_score': relevance_score
            })
            
            analyzed_sentiments.append(analysis)
        
        return jsonify({
            'success': True,
            'ticker_sentiments': analyzed_sentiments
        })
        
    except Exception as e:
        logger.error(f"Error analyzing article ticker sentiments: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to analyze ticker sentiments'
        }), 500

# Alias for the main sentiment analysis endpoint
@sentiment_bp.route('/analyze', methods=['POST'])
def sentiment_analysis():
    """Main sentiment analysis endpoint"""
    return analyze_article()