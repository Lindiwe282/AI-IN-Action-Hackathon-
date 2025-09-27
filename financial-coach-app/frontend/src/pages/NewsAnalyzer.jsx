import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  Container, Typography, Box, Card, CardContent, Grid, Paper, Button,
  IconButton, InputBase, Chip, Alert, Snackbar, CircularProgress,
  Stack, Avatar, Divider, List, ListItem, ListItemText, ListItemAvatar,
  useMediaQuery, CardHeader, Badge, Tab, Tabs, Switch, FormControlLabel,
  LinearProgress, Tooltip, Dialog, DialogTitle, DialogContent, DialogActions,
  TextField, InputAdornment, Slide
} from '@mui/material';
import {
  NewspaperOutlined, TrendingUp, TrendingDown, SearchRounded,
  Refresh, FilterList, BookmarkBorder, Bookmark, Share,
  ThumbUp, ThumbDown, AccessTime, Language, Analytics,
  SignalCellularAlt, ShowChart, Assessment, Timeline,
  ArrowBack, OpenInNew, Visibility, PieChart as PieIcon,
  Close, Business, CalendarToday, TipsAndUpdates, Warning,
  CheckCircle, Info, Psychology, Speed, TrendingFlat,
  ArrowUpward, ArrowDownward, Link as LinkIcon
} from '@mui/icons-material';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as ChartTooltip,
  Legend, ResponsiveContainer, Bar, PieChart, Cell, Pie,
  AreaChart, Area, BarChart
} from 'recharts';
import { styled, useTheme, alpha } from '@mui/material/styles';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const URL_API = 'http://localhost:5000/api';

// Styled components with financial coach theme
const StyledContainer = styled(Container)(({ theme }) => ({
  minHeight: '100vh',
  background: theme.palette.mode === 'dark' 
    ? 'linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%)' 
    : 'linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%)',
  paddingTop: theme.spacing(4),
  paddingBottom: theme.spacing(4),
}));

const GlassCard = styled(Paper)(({ theme }) => ({
  background: theme.palette.mode === 'dark'
    ? 'rgba(255, 255, 255, 0.05)'
    : 'rgba(255, 255, 255, 0.9)',
  backdropFilter: 'blur(20px)',
  WebkitBackdropFilter: 'blur(20px)',
  border: `1px solid ${theme.palette.mode === 'dark' 
    ? 'rgba(255, 255, 255, 0.1)' 
    : 'rgba(255, 255, 255, 0.3)'}`,
  boxShadow: theme.palette.mode === 'dark'
    ? '0 8px 32px 0 rgba(0, 0, 0, 0.37)'
    : '0 8px 32px 0 rgba(31, 38, 135, 0.15)',
  borderRadius: theme.spacing(2.5),
  overflow: 'hidden',
  position: 'relative',
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: theme.palette.mode === 'dark'
      ? '0 12px 40px 0 rgba(0, 0, 0, 0.5)'
      : '0 12px 40px 0 rgba(31, 38, 135, 0.25)',
  }
}));

const NewsCard = styled(GlassCard)(({ theme }) => ({
  cursor: 'pointer',
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  '&:hover': {
    transform: 'translateY(-2px)',
  }
}));

const HeaderBox = styled(Box)(({ theme }) => ({
  background: theme.palette.mode === 'dark'
    ? 'linear-gradient(135deg, rgba(63, 81, 181, 0.1), rgba(103, 58, 183, 0.1))'
    : 'linear-gradient(135deg, rgba(63, 81, 181, 0.05), rgba(103, 58, 183, 0.05))',
  borderRadius: theme.spacing(2.5),
  padding: theme.spacing(3),
  marginBottom: theme.spacing(3),
  backdropFilter: 'blur(10px)',
  WebkitBackdropFilter: 'blur(10px)',
  border: `1px solid ${theme.palette.mode === 'dark' 
    ? 'rgba(255, 255, 255, 0.1)' 
    : 'rgba(0, 0, 0, 0.05)'}`,
}));

const SentimentChip = styled(Chip)(({ theme, sentiment }) => {
  const getSentimentColor = () => {
    if (!sentiment) return { bg: alpha(theme.palette.warning.main, 0.1), color: theme.palette.warning.main };
    
    const sentimentLower = sentiment.toLowerCase();
    if (sentimentLower.includes('bullish') || sentimentLower === 'positive') {
      return { bg: alpha(theme.palette.success.main, 0.1), color: theme.palette.success.main };
    } else if (sentimentLower.includes('bearish') || sentimentLower === 'negative') {
      return { bg: alpha(theme.palette.error.main, 0.1), color: theme.palette.error.main };
    } else {
      return { bg: alpha(theme.palette.warning.main, 0.1), color: theme.palette.warning.main };
    }
  };
  
  const colors = getSentimentColor();
  return {
    backgroundColor: colors.bg,
    color: colors.color,
    fontWeight: 600,
    '&:hover': {
      backgroundColor: colors.bg,
    }
  };
});

// Add new styled components for the dialog
const StyledDialog = styled(Dialog)(({ theme }) => ({
  '& .MuiDialog-paper': {
    background: theme.palette.mode === 'dark'
      ? 'rgba(30, 30, 30, 0.95)'
      : 'rgba(255, 255, 255, 0.95)',
    backdropFilter: 'blur(20px)',
    WebkitBackdropFilter: 'blur(20px)',
    borderRadius: theme.spacing(2),
    maxWidth: '900px',
    width: '90%',
  }
}));

const TickerAnalysisCard = styled(Paper)(({ theme, signal }) => {
  const getBorderColor = () => {
    if (signal?.includes('BUY')) return theme.palette.success.main;
    if (signal?.includes('SELL')) return theme.palette.error.main;
    return theme.palette.warning.main;
  };
  
  return {
    border: `2px solid ${alpha(getBorderColor(), 0.3)}`,
    borderRadius: theme.spacing(1.5),
    background: theme.palette.mode === 'dark'
      ? alpha(getBorderColor(), 0.05)
      : alpha(getBorderColor(), 0.02),
  };
});

const SignalBadge = styled(Chip)(({ theme, signal }) => {
  const getSignalColor = () => {
    if (signal?.includes('BUY')) return theme.palette.success.main;
    if (signal?.includes('SELL')) return theme.palette.error.main;
    return theme.palette.warning.main;
  };
  
  return {
    backgroundColor: alpha(getSignalColor(), 0.1),
    color: getSignalColor(),
    fontWeight: 'bold',
    fontSize: '0.75rem',
  };
});

const MetricCard = styled(Box)(({ theme }) => ({
  padding: theme.spacing(1.5),
  borderRadius: theme.spacing(1),
  background: theme.palette.mode === 'dark'
    ? alpha(theme.palette.common.white, 0.03)
    : alpha(theme.palette.common.black, 0.03),
  border: `1px solid ${theme.palette.divider}`,
  minWidth: '120px',
}));

// Finance color constants
const FINANCE_COLORS = {
  primary: '#1976d2',
  bull: '#4caf50',
  bear: '#f44336',
  neutral: '#ff9800',
  gradient: {
    success: 'linear-gradient(45deg, #4caf50 30%, #66bb6a 90%)',
    danger: 'linear-gradient(45deg, #f44336 30%, #ef5350 90%)',
  }
};

const NewsAnalyzer = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const refreshIntervalRef = useRef(null);
  
  // State management
  const [selectedTicker, setSelectedTicker] = useState('AAPL');
  const [searchValue, setSearchValue] = useState('');
  const [newsData, setNewsData] = useState([]);
  const [sentimentData, setSentimentData] = useState({});
  const [marketData, setMarketData] = useState({});
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState(0);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [bookmarkedNews, setBookmarkedNews] = useState(new Set());
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });
  
  // Dialog state
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [articleAnalysis, setArticleAnalysis] = useState(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);

  // Popular tickers for quick selection
  const popularTickers = ['AAPL', 'GOOGL', 'MSFT', 'NVDA', 'AMZN', 'TSLA', 'META', 'NFLX'];

  // Data preparation functions
  const preparePieChartData = () => {
    const aggregateMetrics = sentimentData.aggregateMetrics;
    if (!aggregateMetrics) return [];
    
    // Create a basic breakdown based on available data
    const avgSentiment = aggregateMetrics.average_sentiment || 0;
    
    // Estimate distribution based on average sentiment
    let positive = 0, negative = 0, neutral = 0;
    
    if (avgSentiment > 0.2) {
      positive = 0.6;
      neutral = 0.3;
      negative = 0.1;
    } else if (avgSentiment < -0.2) {
      positive = 0.1;
      neutral = 0.3;
      negative = 0.6;
    } else {
      positive = 0.3;
      neutral = 0.5;
      negative = 0.2;
    }
    
    return [
      { name: 'Positive', value: positive, fill: '#4caf50' },
      { name: 'Negative', value: negative, fill: '#f44336' },
      { name: 'Neutral', value: neutral, fill: '#ff9800' }
    ];
  };

  const prepareTrendData = () => {
    if (!newsData || newsData.length === 0) return [];
    
    // Create trend data from articles' timestamps and sentiment scores
    const trendData = newsData.slice(0, 10).map((article, index) => ({
      time: article.time_published ? new Date(article.time_published).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : `Day ${index + 1}`,
      sentiment: article.overall_sentiment_score || 0,
      volume: article.ticker_sentiments?.filter(ts => ts.ticker === selectedTicker).reduce((acc, ts) => acc + (ts.sentiment_score || 0), 0) || Math.random() * 0.5
    })).reverse();
    
    return trendData;
  };

  // Auto-refresh effect
  useEffect(() => {
    fetchNewsAndSentiment();

    if (autoRefresh) {
      refreshIntervalRef.current = setInterval(() => {
        fetchNewsAndSentiment();
      }, 30000); // Refresh every 30 seconds
    }

    return () => {
      if (refreshIntervalRef.current) {
        clearInterval(refreshIntervalRef.current);
      }
    };
  }, [selectedTicker, autoRefresh]);

  const fetchNewsAndSentiment = async () => {
    try {
      setLoading(true);
      
      // Fetch sentiment analysis using the correct endpoint
      const sentimentResponse = await axios.get(`${URL_API}/sentiment/news/${selectedTicker}`);
      
      if (sentimentResponse.data) {
        // Update to match the new API response structure
        setSentimentData({
          aggregateMetrics: sentimentResponse.data.aggregate_sentiment || {},
          articles: sentimentResponse.data.articles || [],
          ticker: sentimentResponse.data.ticker,
          pagination: sentimentResponse.data.pagination || {},
          success: sentimentResponse.data.success
        });
        setNewsData(sentimentResponse.data.articles || []);
      }

      // Fetch market data using stock-prices endpoint
      try {
        const marketResponse = await axios.get(`${URL_API}/stock-prices?tickers=${selectedTicker}`);
        
        if (marketResponse.data && marketResponse.data.length > 0) {
          const stockData = marketResponse.data[0];
          setMarketData({
            price: stockData.price,
            change: stockData.change,
            changePercent: stockData.change_percent
          });
        }
      } catch (marketError) {
        console.warn('Market data not available:', marketError);
      }

    } catch (error) {
      console.error('Error fetching news and sentiment:', error);
      setSnackbar({ open: true, message: 'Failed to fetch news data', severity: 'error' });
      // Set empty state
      setSentimentData({
        aggregateMetrics: {},
        articles: [],
        ticker: selectedTicker,
        pagination: {},
        success: false
      });
      setNewsData([]);
    } finally {
      setLoading(false);
    }
  };

  const handleTickerChange = (ticker) => {
    setSelectedTicker(ticker);
  };

  const handleSearchInputChange = (event) => {
    setSearchValue(event.target.value.toUpperCase());
  };

  const handleSearchKeyPress = (event) => {
    if (event.key === 'Enter' && searchValue.trim()) {
      setSelectedTicker(searchValue.trim());
    }
  };

  const handleArticleClick = async (article) => {
    setSelectedArticle(article);
    setModalOpen(true);
    setAnalysisLoading(true);
    
    try {
      // Simulate article analysis - replace with actual API call
      const mockAnalysis = {
        article_info: {
          title: article.title,
          summary: article.summary,
          source: article.source,
          published: article.time_published,
        },
        sentiment_overview: {
          interpretation: {
            signal: article.overall_sentiment_label?.includes('positive') || article.overall_sentiment_score > 0.1 ? 'BUY' :
                   article.overall_sentiment_label?.includes('negative') || article.overall_sentiment_score < -0.1 ? 'SELL' : 'HOLD',
            confidence: 'Medium',
            color_code: article.overall_sentiment_score > 0.1 ? FINANCE_COLORS.bull :
                       article.overall_sentiment_score < -0.1 ? FINANCE_COLORS.bear : FINANCE_COLORS.neutral,
            explanation: `Based on sentiment analysis, this article shows ${article.overall_sentiment_label || 'neutral'} sentiment towards the market.`,
            action: article.overall_sentiment_score > 0.1 ? 'Consider buying opportunities' :
                   article.overall_sentiment_score < -0.1 ? 'Exercise caution, consider selling' : 'Wait and observe'
          }
        },
        ticker_analysis: article.ticker_sentiments?.slice(0, 3).map(ts => ({
          ticker: ts.ticker,
          signal: ts.signal || (ts.sentiment_score > 0.1 ? 'BUY' : ts.sentiment_score < -0.1 ? 'SELL' : 'HOLD'),
          sentiment_score: ts.sentiment_score,
          confidence: ts.sentiment_label === 'Bullish' || ts.sentiment_label === 'Bearish' ? 'High' : 'Medium',
          risk_level: Math.abs(ts.sentiment_score) > 0.5 ? 'High' : Math.abs(ts.sentiment_score) > 0.2 ? 'Medium' : 'Low',
          relevance_score: ts.relevance_score,
          relevance_interpretation: ts.relevance_score > 0.7 ? 'High' : ts.relevance_score > 0.4 ? 'Medium' : 'Low',
          weight: ts.relevance_score,
          explanation: `Sentiment analysis indicates ${ts.sentiment_label?.toLowerCase() || 'neutral'} sentiment for ${ts.ticker}.`,
          action: ts.sentiment_score > 0.1 ? 'Consider buying' : ts.sentiment_score < -0.1 ? 'Consider selling' : 'Hold position',
          visual: {
            color: ts.sentiment_score > 0.1 ? FINANCE_COLORS.bull : ts.sentiment_score < -0.1 ? FINANCE_COLORS.bear : FINANCE_COLORS.neutral,
            risk_color: Math.abs(ts.sentiment_score) > 0.5 ? FINANCE_COLORS.bear : FINANCE_COLORS.neutral,
            should_invest: ts.sentiment_score > 0.1
          }
        })) || [],
        investment_summary: {
          buy_signals: article.ticker_sentiments?.filter(ts => ts.sentiment_score > 0.1).length || 0,
          hold_signals: article.ticker_sentiments?.filter(ts => Math.abs(ts.sentiment_score) <= 0.1).length || 1,
          sell_signals: article.ticker_sentiments?.filter(ts => ts.sentiment_score < -0.1).length || 0,
          top_pick: article.ticker_sentiments?.find(ts => ts.sentiment_score > 0.1) ? {
            ticker: article.ticker_sentiments.find(ts => ts.sentiment_score > 0.1).ticker,
            signal: 'BUY'
          } : null,
          avoid: article.ticker_sentiments?.find(ts => ts.sentiment_score < -0.1) ? {
            ticker: article.ticker_sentiments.find(ts => ts.sentiment_score < -0.1).ticker,
            signal: 'SELL'
          } : null
        }
      };
      
      setTimeout(() => {
        setArticleAnalysis(mockAnalysis);
        setAnalysisLoading(false);
      }, 1500);
      
    } catch (error) {
      console.error('Error analyzing article:', error);
      setAnalysisLoading(false);
      setSnackbar({ open: true, message: 'Failed to analyze article', severity: 'error' });
    }
  };

  const handleCloseModal = () => {
    setModalOpen(false);
    setSelectedArticle(null);
    setArticleAnalysis(null);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown date';
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    } catch {
      return 'Unknown date';
    }
  };

  const formatSentimentScore = (score) => {
    if (typeof score !== 'number') return '0.00';
    return (score >= 0 ? '+' : '') + score.toFixed(2);
  };

  const toggleBookmark = (newsId) => {
    const newBookmarks = new Set(bookmarkedNews);
    if (newBookmarks.has(newsId)) {
      newBookmarks.delete(newsId);
    } else {
      newBookmarks.add(newsId);
    }
    setBookmarkedNews(newBookmarks);
  };

  const getSentimentIcon = (sentiment) => {
    if (!sentiment) return <Analytics color="warning" />;
    
    const sentimentLower = sentiment.toLowerCase();
    if (sentimentLower.includes('bullish')) {
      return <TrendingUp color="success" />;
    } else if (sentimentLower.includes('bearish')) {
      return <TrendingDown color="error" />;
    } else if (sentimentLower === 'positive') {
      return <TrendingUp color="success" />;
    } else if (sentimentLower === 'negative') {
      return <TrendingDown color="error" />;
    } else {
      return <Analytics color="warning" />;
    }
  };

  const getSentimentColor = (sentiment) => {
    if (!sentiment) return '#FFBB33';
    
    const sentimentLower = sentiment.toLowerCase();
    if (sentimentLower.includes('bullish')) {
      return '#00C851';
    } else if (sentimentLower.includes('bearish')) {
      return '#FF4444';
    } else if (sentimentLower === 'positive') {
      return '#00C851';
    } else if (sentimentLower === 'negative') {
      return '#FF4444';
    } else {
      return '#FFBB33';
    }
  };

  const formatTimeAgo = (timestamp) => {
    if (!timestamp) return 'Unknown';
    const now = new Date();
    const time = new Date(timestamp);
    const diffInHours = Math.floor((now - time) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'Just now';
    if (diffInHours < 24) return `${diffInHours}h ago`;
    return `${Math.floor(diffInHours / 24)}d ago`;
  };

  return (
    <StyledContainer maxWidth="xl">
      {/* Header Section */}
      <HeaderBox>
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={6}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Button
                startIcon={<ArrowBack />}
                onClick={() => navigate('/investment')}
                variant="outlined"
                sx={{ borderRadius: 2 }}
              >
                Back
              </Button>
              <Avatar sx={{ bgcolor: theme.palette.secondary.main, width: 56, height: 56 }}>
                <NewspaperOutlined fontSize="large" />
              </Avatar>
              <Box>
                <Typography variant="h4" fontWeight="bold" color="secondary">
                  News & Sentiment Analyzer
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  Real-time financial news analysis and market sentiment insights
                </Typography>
              </Box>
            </Box>
          </Grid>
          <Grid item xs={12} md={6}>
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2, alignItems: 'center' }}>
              <FormControlLabel
                control={<Switch checked={autoRefresh} onChange={(e) => setAutoRefresh(e.target.checked)} />}
                label="Auto-refresh"
              />
              <Button
                startIcon={<Refresh />}
                onClick={fetchNewsAndSentiment}
                variant="contained"
                disabled={loading}
                sx={{ borderRadius: 2, minWidth: 120 }}
              >
                {loading ? <CircularProgress size={20} color="inherit" /> : 'Refresh'}
              </Button>
            </Box>
          </Grid>
        </Grid>
      </HeaderBox>

      {/* Ticker Search */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>Search Stock Symbol</Typography>
          <TextField
            fullWidth
            value={searchValue}
            onChange={handleSearchInputChange}
            onKeyPress={handleSearchKeyPress}
            placeholder="Enter ticker symbol (e.g., AAPL, GOOGL, TSLA)"
            variant="outlined"
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchRounded sx={{ color: 'text.secondary' }} />
                </InputAdornment>
              ),
            }}
            sx={{ mb: 2 }}
          />
          <Typography variant="caption" color="text.secondary">
            Currently analyzing: <strong>{selectedTicker}</strong> • Press Enter to search for a new ticker
          </Typography>
          <Box sx={{ mt: 2 }}>
            <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
              Quick select:
            </Typography>
            <Stack direction="row" spacing={1} flexWrap="wrap">
              {popularTickers.map((ticker) => (
                <Chip
                  key={ticker}
                  label={ticker}
                  onClick={() => handleTickerChange(ticker)}
                  color={selectedTicker === ticker ? 'primary' : 'default'}
                  variant={selectedTicker === ticker ? 'filled' : 'outlined'}
                  size="small"
                  sx={{ mb: 1 }}
                />
              ))}
            </Stack>
          </Box>
        </CardContent>
      </Card>

      {/* Navigation Tabs */}
      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={activeTab}
          onChange={(e, newValue) => setActiveTab(newValue)}
          variant="fullWidth"
          textColor="primary"
          indicatorColor="primary"
        >
          <Tab label="Market Overview" icon={<ShowChart />} />
          <Tab label="Sentiment Analysis" icon={<Analytics />} />
          <Tab label="News Feed" icon={<NewspaperOutlined />} />
          <Tab label="Trends" icon={<Timeline />} />
        </Tabs>
      </Paper>

      <AnimatePresence mode="wait">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3 }}
        >
          {/* Market Overview Tab */}
          {activeTab === 0 && (
            <Grid container spacing={3}>
              {/* Market Data Cards */}
              <Grid item xs={12} md={4}>
                <GlassCard>
                  <CardContent>
                    <Typography variant="h6" color="primary" gutterBottom>
                      Current Price
                    </Typography>
                    <Typography variant="h4" fontWeight="bold">
                      ${marketData.price || '---'}
                    </Typography>
                    <Typography 
                      variant="body2" 
                      color={marketData.change >= 0 ? 'success.main' : 'error.main'}
                    >
                      {marketData.change >= 0 ? '+' : ''}{marketData.change || '--'} ({marketData.changePercent || '--'}%)
                    </Typography>
                  </CardContent>
                </GlassCard>
              </Grid>
              
              <Grid item xs={12} md={4}>
                <GlassCard>
                  <CardContent>
                    <Typography variant="h6" color="primary" gutterBottom>
                      Sentiment Score
                    </Typography>
                    <Typography variant="h4" fontWeight="bold" 
                      sx={{ color: sentimentData.aggregateMetrics?.average_sentiment > 0 ? 'success.main' : 
                                  sentimentData.aggregateMetrics?.average_sentiment < 0 ? 'error.main' : 'warning.main' }}>
                      {sentimentData.aggregateMetrics?.average_sentiment?.toFixed(3) || '0.000'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {sentimentData.aggregateMetrics?.recommendation || 'NEUTRAL'}
                    </Typography>
                  </CardContent>
                </GlassCard>
              </Grid>
              
              <Grid item xs={12} md={4}>
                <GlassCard>
                  <CardContent>
                    <Typography variant="h6" color="primary" gutterBottom>
                      Articles Analyzed
                    </Typography>
                    <Typography variant="h4" fontWeight="bold">
                      {sentimentData.aggregateMetrics?.articles_analyzed || 0}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Confidence: {sentimentData.aggregateMetrics?.confidence_level || 'Medium'}
                    </Typography>
                  </CardContent>
                </GlassCard>
              </Grid>
            </Grid>
          )}

          {/* Sentiment Analysis Tab */}
          {activeTab === 1 && (
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <GlassCard>
                  <CardHeader
                    title={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Analytics color="primary" />
                        <Typography variant="h6" fontWeight="bold">
                          Sentiment Analysis for {selectedTicker}
                        </Typography>
                      </Box>
                    }
                  />
                  <CardContent>
                    {sentimentData.aggregateMetrics && Object.keys(sentimentData.aggregateMetrics).length > 0 ? (
                      <Grid container spacing={4}>
                        <Grid item xs={12} md={6}>
                          <Stack spacing={3}>
                            <Box>
                              <Typography variant="body2" color="text.secondary" gutterBottom>
                                Overall Sentiment
                              </Typography>
                              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                                {getSentimentIcon(sentimentData.aggregateMetrics?.interpretation?.signal)}
                                <Typography variant="h5" fontWeight="bold">
                                  {sentimentData.aggregateMetrics?.recommendation || 'NEUTRAL'}
                                </Typography>
                              </Box>
                              <Typography 
                                variant="body2" 
                                sx={{ 
                                  mt: 1, 
                                  color: getSentimentColor(sentimentData.aggregateMetrics?.interpretation?.signal),
                                  fontWeight: 'medium'
                                }}
                              >
                                {sentimentData.aggregateMetrics?.interpretation?.action || 'Wait for clearer signals'}
                              </Typography>
                            </Box>
                            
                            <Box>
                              <Typography variant="body2" color="text.secondary" gutterBottom>
                                Confidence Level
                              </Typography>
                              <LinearProgress
                                variant="determinate"
                                value={sentimentData.aggregateMetrics?.confidence_level === 'High' ? 85 : 
                                       sentimentData.aggregateMetrics?.confidence_level === 'Medium' ? 65 : 40}
                                sx={{ height: 8, borderRadius: 4 }}
                              />
                              <Typography variant="body2" sx={{ mt: 1 }}>
                                {sentimentData.aggregateMetrics?.confidence_level || 'Medium'} confidence
                              </Typography>
                            </Box>
                            
                            <Box>
                              <Typography variant="body2" color="text.secondary" gutterBottom>
                                News Articles Analyzed
                              </Typography>
                              <Typography variant="h4" fontWeight="bold" color="primary">
                                {sentimentData.aggregateMetrics?.articles_analyzed || 0}
                              </Typography>
                            </Box>

                            <Box>
                              <Typography variant="body2" color="text.secondary" gutterBottom>
                                Average Sentiment Score
                              </Typography>
                              <Typography variant="h5" fontWeight="bold" 
                                sx={{ color: sentimentData.aggregateMetrics?.average_sentiment > 0 ? 'success.main' : 
                                            sentimentData.aggregateMetrics?.average_sentiment < 0 ? 'error.main' : 'warning.main' }}>
                                {sentimentData.aggregateMetrics?.average_sentiment?.toFixed(3) || '0.000'}
                              </Typography>
                            </Box>
                          </Stack>
                        </Grid>
                        
                        <Grid item xs={12} md={6}>
                          <Typography variant="body2" color="text.secondary" gutterBottom>
                            Market Signal & Risk Assessment
                          </Typography>
                          <Stack spacing={2}>
                            <Box sx={{ 
                              p: 2, 
                              borderRadius: 2, 
                              bgcolor: alpha(getSentimentColor(sentimentData.aggregateMetrics?.interpretation?.signal) || '#FFBB33', 0.1),
                              border: `1px solid ${getSentimentColor(sentimentData.aggregateMetrics?.interpretation?.signal) || '#FFBB33'}`
                            }}>
                              <Typography variant="h6" fontWeight="bold" 
                                sx={{ color: getSentimentColor(sentimentData.aggregateMetrics?.interpretation?.signal) }}>
                                {sentimentData.aggregateMetrics?.interpretation?.signal || 'HOLD'}
                              </Typography>
                              <Typography variant="body2" sx={{ mt: 1 }}>
                                Risk Level: {sentimentData.aggregateMetrics?.interpretation?.risk_level || 'Moderate'}
                              </Typography>
                              <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                                {sentimentData.aggregateMetrics?.interpretation?.explanation || 'Market conditions require careful analysis'}
                              </Typography>
                            </Box>

                            <Box>
                              <Typography variant="body2" color="text.secondary" gutterBottom>
                                Sentiment Trend
                              </Typography>
                              <Typography variant="body1" fontWeight="medium">
                                {sentimentData.aggregateMetrics?.sentiment_trend || 'Stable'}
                              </Typography>
                            </Box>

                            <Box>
                              <Typography variant="body2" color="text.secondary" gutterBottom>
                                Ticker Mentions
                              </Typography>
                              <Typography variant="h6" fontWeight="bold">
                                {sentimentData.aggregateMetrics?.ticker_mentions || 0}
                              </Typography>
                            </Box>
                          </Stack>
                        </Grid>
                      </Grid>
                    ) : (
                      <Box sx={{ textAlign: 'center', py: 4 }}>
                        <Typography variant="body1" color="text.secondary">
                          No sentiment data available. Try analyzing a different ticker.
                        </Typography>
                      </Box>
                    )}
                  </CardContent>
                </GlassCard>
              </Grid>
            </Grid>
          )}

          {/* News Feed Tab */}
          {activeTab === 2 && (
            <Grid container spacing={3}>
              {newsData.length > 0 ? (
                newsData.slice(0, 12).map((article, index) => (
                  <Grid item xs={12} md={6} lg={4} key={index}>
                    <NewsCard onClick={() => handleArticleClick(article)}>
                      <CardContent>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                          <SentimentChip
                            label={article.overall_sentiment_label || 'neutral'}
                            sentiment={article.overall_sentiment_label}
                            size="small"
                          />
                          <IconButton
                            size="small"
                            onClick={(e) => {
                              e.stopPropagation();
                              toggleBookmark(index);
                            }}
                          >
                            {bookmarkedNews.has(index) ? <Bookmark color="primary" /> : <BookmarkBorder />}
                          </IconButton>
                        </Box>
                        
                        <Typography variant="h6" fontWeight="bold" sx={{ mb: 2, lineHeight: 1.3 }}>
                          {article.title || 'News Title'}
                        </Typography>
                        
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                          {(article.summary || 'No summary available').substring(0, 150)}...
                        </Typography>

                        {/* Ticker Sentiment Summary */}
                        {article.ticker_sentiments && article.ticker_sentiments.length > 0 && (
                          <Box sx={{ mb: 2 }}>
                            <Typography variant="caption" color="text.secondary" gutterBottom>
                              Main Sentiment:
                            </Typography>
                            {article.ticker_sentiments.filter(ts => ts.ticker === selectedTicker).map((tickerSent, idx) => (
                              <Box key={idx} sx={{ mt: 1, p: 1, borderRadius: 1, bgcolor: alpha(tickerSent.color_code || '#FFBB33', 0.1) }}>
                                <Typography variant="caption" fontWeight="bold" sx={{ color: tickerSent.color_code }}>
                                  {tickerSent.signal} - {tickerSent.sentiment_label}
                                </Typography>
                                <Typography variant="caption" display="block" color="text.secondary">
                                  Score: {tickerSent.sentiment_score?.toFixed(3)} | Relevance: {tickerSent.relevance_score?.toFixed(3)}
                                </Typography>
                              </Box>
                            ))}
                          </Box>
                        )}
                        
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <AccessTime fontSize="small" color="disabled" />
                            <Typography variant="caption" color="text.secondary">
                              {formatTimeAgo(article.time_published)}
                            </Typography>
                          </Box>
                          
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography variant="caption" color="text.secondary">
                              {article.source}
                            </Typography>
                            <IconButton 
                              size="small" 
                              onClick={() => window.open(article.url, '_blank')}
                              disabled={!article.url}
                            >
                              <OpenInNew fontSize="small" />
                            </IconButton>
                          </Box>
                        </Box>
                      </CardContent>
                    </NewsCard>
                  </Grid>
                ))
              ) : (
                <Grid item xs={12}>
                  <Box sx={{ textAlign: 'center', py: 8 }}>
                    <NewspaperOutlined sx={{ fontSize: 64, color: 'text.disabled', mb: 2 }} />
                    <Typography variant="h6" color="text.secondary" gutterBottom>
                      No news articles available
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Try selecting a different ticker or refresh the data
                    </Typography>
                  </Box>
                </Grid>
              )}
            </Grid>
          )}

          {/* Trends Tab */}
          {activeTab === 3 && (
            <Grid container spacing={4}>
              <Grid item xs={12}>
                <GlassCard>
                  <CardHeader
                    title={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Timeline color="primary" />
                        <Typography variant="h6" fontWeight="bold">
                          Sentiment Trends for {selectedTicker}
                        </Typography>
                      </Box>
                    }
                  />
                  <CardContent>
                    <ResponsiveContainer width="100%" height={300}>
                      <LineChart data={prepareTrendData()}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="time" />
                        <YAxis />
                        <ChartTooltip />
                        <Legend />
                        <Line type="monotone" dataKey="sentiment" stroke="#8884d8" strokeWidth={2} />
                      </LineChart>
                    </ResponsiveContainer>
                  </CardContent>
                </GlassCard>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <GlassCard>
                  <CardHeader title="Sentiment Distribution" />
                  <CardContent>
                    <ResponsiveContainer width="100%" height={250}>
                      <PieChart>
                        <Pie
                          data={preparePieChartData()}
                          cx="50%"
                          cy="50%"
                          innerRadius={60}
                          outerRadius={80}
                          paddingAngle={5}
                          dataKey="value"
                        >
                          {preparePieChartData().map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.fill} />
                          ))}
                        </Pie>
                        <ChartTooltip />
                        <Legend />
                      </PieChart>
                    </ResponsiveContainer>
                  </CardContent>
                </GlassCard>
              </Grid>
            </Grid>
          )}
        </motion.div>
      </AnimatePresence>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert
          severity={snackbar.severity}
          onClose={() => setSnackbar({ ...snackbar, open: false })}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>

      {/* Article Analysis Modal */}
      <StyledDialog
        open={modalOpen}
        onClose={handleCloseModal}
        TransitionComponent={Slide}
        TransitionProps={{ direction: 'up' }}
      >
        {selectedArticle && (
          <>
            <DialogTitle>
              <Stack direction="row" alignItems="center" justifyContent="space-between">
                <Typography variant="h5" fontWeight="bold">
                  Article Analysis
                </Typography>
                <IconButton onClick={handleCloseModal}>
                  <Close />
                </IconButton>
              </Stack>
            </DialogTitle>
            
            <DialogContent dividers>
              {analysisLoading ? (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <CircularProgress />
                  <Typography variant="body2" sx={{ mt: 2 }}>
                    Analyzing article sentiment...
                  </Typography>
                </Box>
              ) : articleAnalysis ? (
                <Stack spacing={3}>
                  {/* Article Info */}
                  <Box>
                    <Typography variant="h6" gutterBottom>
                      {articleAnalysis.article_info.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      {articleAnalysis.article_info.summary}
                    </Typography>
                    <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
                      <Chip 
                        label={articleAnalysis.article_info.source}
                        size="small"
                        icon={<Business sx={{ fontSize: 16 }} />}
                      />
                      <Chip 
                        label={formatDate(articleAnalysis.article_info.published)}
                        size="small"
                        icon={<CalendarToday sx={{ fontSize: 16 }} />}
                      />
                    </Stack>
                  </Box>

                  {/* Overall Sentiment - Modern Finance Card */}
                  <GlassCard 
                    sx={{ 
                      p: 3,
                      background: theme.palette.mode === 'dark'
                        ? `linear-gradient(135deg, ${alpha(articleAnalysis.sentiment_overview.interpretation.color_code, 0.1)} 0%, ${alpha('#000', 0.5)} 100%)`
                        : `linear-gradient(135deg, ${alpha(articleAnalysis.sentiment_overview.interpretation.color_code, 0.1)} 0%, ${alpha('#fff', 0.5)} 100%)`,
                      border: `1px solid ${alpha(articleAnalysis.sentiment_overview.interpretation.color_code, 0.3)}`,
                    }}
                  >
                    <Stack spacing={2}>
                      <Typography variant="h6" sx={{ color: articleAnalysis.sentiment_overview.interpretation.color_code }}>
                        Overall Market Sentiment
                      </Typography>
                      <Grid container spacing={2}>
                        <Grid item xs={6}>
                          <Typography variant="body2" color="text.secondary">
                            Signal
                          </Typography>
                          <Stack direction="row" alignItems="center" spacing={1}>
                            {articleAnalysis.sentiment_overview.interpretation.signal.includes('BUY') ? (
                              <TrendingUp sx={{ color: FINANCE_COLORS.bull, fontSize: 28 }} />
                            ) : articleAnalysis.sentiment_overview.interpretation.signal.includes('SELL') ? (
                              <TrendingDown sx={{ color: FINANCE_COLORS.bear, fontSize: 28 }} />
                            ) : (
                              <TrendingFlat sx={{ color: FINANCE_COLORS.neutral, fontSize: 28 }} />
                            )}
                            <Typography variant="h5" fontWeight="bold">
                              {articleAnalysis.sentiment_overview.interpretation.signal}
                            </Typography>
                          </Stack>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="body2" color="text.secondary">
                            Confidence
                          </Typography>
                          <Typography variant="h5" fontWeight="bold" sx={{ color: articleAnalysis.sentiment_overview.interpretation.color_code }}>
                            {articleAnalysis.sentiment_overview.interpretation.confidence}
                          </Typography>
                          <LinearProgress
                            variant="determinate"
                            value={
                              articleAnalysis.sentiment_overview.interpretation.confidence === 'High' ? 90 :
                              articleAnalysis.sentiment_overview.interpretation.confidence === 'Medium' ? 60 : 30
                            }
                            sx={{
                              mt: 1,
                              height: 6,
                              borderRadius: 3,
                              backgroundColor: alpha(articleAnalysis.sentiment_overview.interpretation.color_code, 0.2),
                              '& .MuiLinearProgress-bar': {
                                backgroundColor: articleAnalysis.sentiment_overview.interpretation.color_code,
                                borderRadius: 3
                              }
                            }}
                          />
                        </Grid>
                      </Grid>
                      <Alert 
                        severity={
                          articleAnalysis.sentiment_overview.interpretation.signal.includes('BUY') ? 'success' :
                          articleAnalysis.sentiment_overview.interpretation.signal.includes('SELL') ? 'error' : 'info'
                        }
                        icon={<TipsAndUpdates />}
                        sx={{ 
                          backgroundColor: alpha(articleAnalysis.sentiment_overview.interpretation.color_code, 0.1),
                          '& .MuiAlert-icon': {
                            color: articleAnalysis.sentiment_overview.interpretation.color_code
                          }
                        }}
                      >
                        {articleAnalysis.sentiment_overview.interpretation.explanation}
                      </Alert>
                      <Typography variant="body2">
                        <strong>Recommended Action:</strong> {articleAnalysis.sentiment_overview.interpretation.action}
                      </Typography>
                    </Stack>
                  </GlassCard>

                  {/* Individual Stock Analysis - Modern Finance Theme */}
                  {articleAnalysis.ticker_analysis && articleAnalysis.ticker_analysis.length > 0 && (
                    <Box>
                      <Typography variant="h6" gutterBottom sx={{ mb: 3 }}>
                        Stock Sentiment Analysis
                      </Typography>
                      <Stack spacing={3}>
                        {articleAnalysis.ticker_analysis.map((ticker, index) => (
                          <TickerAnalysisCard key={index} signal={ticker.signal} elevation={0}>
                            <Box sx={{ p: 3 }}>
                              {/* Header Section */}
                              <Grid container alignItems="center" spacing={2} sx={{ mb: 3 }}>
                                <Grid item xs={12} md={6}>
                                  <Stack direction="row" alignItems="center" spacing={2}>
                                    <Avatar
                                      sx={{
                                        width: 56,
                                        height: 56,
                                        background: ticker.visual.color,
                                        fontSize: '1.5rem',
                                        fontWeight: 'bold'
                                      }}
                                    >
                                      {ticker.ticker.substring(0, 2)}
                                    </Avatar>
                                    <Box>
                                      <Typography variant="h5" fontWeight="bold">
                                        {ticker.ticker}
                                      </Typography>
                                      <SignalBadge signal={ticker.signal}>
                                        {ticker.signal}
                                      </SignalBadge>
                                    </Box>
                                  </Stack>
                                </Grid>
                                
                                <Grid item xs={12} md={6}>
                                  <Stack direction="row" spacing={2} justifyContent="flex-end">
                                    <MetricCard>
                                      <Typography variant="caption" color="text.secondary">
                                        Sentiment Score
                                      </Typography>
                                      <Stack direction="row" alignItems="baseline" spacing={0.5}>
                                        <Typography variant="h5" fontWeight="bold" color={ticker.sentiment_score >= 0 ? FINANCE_COLORS.bull : FINANCE_COLORS.bear}>
                                          {formatSentimentScore(ticker.sentiment_score)}
                                        </Typography>
                                        {ticker.sentiment_score > 0 ? (
                                          <ArrowUpward sx={{ fontSize: 16, color: FINANCE_COLORS.bull }} />
                                        ) : ticker.sentiment_score < 0 ? (
                                          <ArrowDownward sx={{ fontSize: 16, color: FINANCE_COLORS.bear }} />
                                        ) : (
                                          <TrendingFlat sx={{ fontSize: 16, color: FINANCE_COLORS.neutral }} />
                                        )}
                                      </Stack>
                                    </MetricCard>
                                    
                                    <MetricCard>
                                      <Typography variant="caption" color="text.secondary">
                                        Confidence
                                      </Typography>
                                      <Typography variant="h5" fontWeight="bold">
                                        {ticker.confidence}
                                      </Typography>
                                      <LinearProgress
                                        variant="determinate"
                                        value={
                                          ticker.confidence === 'High' ? 90 :
                                          ticker.confidence === 'Medium' ? 60 : 30
                                        }
                                        sx={{
                                          mt: 1,
                                          height: 4,
                                          borderRadius: 2,
                                          backgroundColor: alpha(ticker.visual.color, 0.2),
                                          '& .MuiLinearProgress-bar': {
                                            backgroundColor: ticker.visual.color,
                                            borderRadius: 2
                                          }
                                        }}
                                      />
                                    </MetricCard>
                                  </Stack>
                                </Grid>
                              </Grid>

                              {/* Metrics Grid */}
                              <Grid container spacing={2} sx={{ mb: 3 }}>
                                <Grid item xs={12} md={4}>
                                  <Paper
                                    sx={{
                                      p: 2,
                                      background: alpha(ticker.visual.risk_color, 0.05),
                                      border: `1px solid ${alpha(ticker.visual.risk_color, 0.2)}`,
                                      borderRadius: 2
                                    }}
                                  >
                                    <Stack direction="row" alignItems="center" spacing={1}>
                                      <Warning sx={{ color: ticker.visual.risk_color }} />
                                      <Box>
                                        <Typography variant="caption" color="text.secondary">
                                          Risk Level
                                        </Typography>
                                        <Typography variant="body1" fontWeight="bold" color={ticker.visual.risk_color}>
                                          {ticker.risk_level}
                                        </Typography>
                                      </Box>
                                    </Stack>
                                  </Paper>
                                </Grid>
                                
                                <Grid item xs={12} md={4}>
                                  <Paper
                                    sx={{
                                      p: 2,
                                      background: alpha(FINANCE_COLORS.primary, 0.05),
                                      border: `1px solid ${alpha(FINANCE_COLORS.primary, 0.2)}`,
                                      borderRadius: 2
                                    }}
                                  >
                                    <Stack direction="row" alignItems="center" spacing={1}>
                                      <Speed sx={{ color: FINANCE_COLORS.primary }} />
                                      <Box>
                                        <Typography variant="caption" color="text.secondary">
                                          Relevance
                                        </Typography>
                                        <Typography variant="body1" fontWeight="bold">
                                          {ticker.relevance_interpretation}
                                        </Typography>
                                        <Typography variant="caption" color="text.secondary">
                                          ({(ticker.relevance_score * 100).toFixed(0)}%)
                                        </Typography>
                                      </Box>
                                    </Stack>
                                  </Paper>
                                </Grid>
                                
                                <Grid item xs={12} md={4}>
                                  <Paper
                                    sx={{
                                      p: 2,
                                      background: alpha(ticker.visual.color, 0.05),
                                      border: `1px solid ${alpha(ticker.visual.color, 0.2)}`,
                                      borderRadius: 2
                                    }}
                                  >
                                    <Stack direction="row" alignItems="center" spacing={1}>
                                      <Psychology sx={{ color: ticker.visual.color }} />
                                      <Box>
                                        <Typography variant="caption" color="text.secondary">
                                          Weight Score
                                        </Typography>
                                        <Typography variant="body1" fontWeight="bold">
                                          {(ticker.weight * 100).toFixed(1)}%
                                        </Typography>
                                      </Box>
                                    </Stack>
                                  </Paper>
                                </Grid>
                              </Grid>

                              {/* Explanation Section */}
                              <GlassCard 
                                sx={{ 
                                  p: 2.5, 
                                  background: theme.palette.mode === 'dark'
                                    ? 'rgba(255, 255, 255, 0.02)'
                                    : 'rgba(0, 0, 0, 0.02)',
                                  border: 'none'
                                }}
                              >
                                <Stack spacing={2}>
                                  <Box>
                                    <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 1 }}>
                                      <Info sx={{ fontSize: 18, color: 'text.secondary' }} />
                                      <Typography variant="subtitle2" fontWeight="bold">
                                        Analysis Explanation
                                      </Typography>
                                    </Stack>
                                    <Typography variant="body2" color="text.secondary">
                                      {ticker.explanation}
                                    </Typography>
                                  </Box>
                                  
                                  <Divider />
                                  
                                  <Box>
                                    <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 1 }}>
                                      <TipsAndUpdates sx={{ fontSize: 18, color: ticker.visual.color }} />
                                      <Typography variant="subtitle2" fontWeight="bold">
                                        Recommended Action
                                      </Typography>
                                    </Stack>
                                    <Typography variant="body2">
                                      {ticker.action}
                                    </Typography>
                                  </Box>
                                </Stack>
                              </GlassCard>

                              {/* Investment Decision */}
                              <Box sx={{ mt: 3, textAlign: 'center' }}>
                                {ticker.visual.should_invest ? (
                                  <Chip
                                    icon={<CheckCircle />}
                                    label="Favorable for Investment"
                                    sx={{
                                      py: 2,
                                      px: 3,
                                      fontSize: '1rem',
                                      fontWeight: 'bold',
                                      background: FINANCE_COLORS.gradient.success,
                                      color: 'white',
                                      '& .MuiChip-icon': {
                                        color: 'white'
                                      }
                                    }}
                                  />
                                ) : (
                                  <Chip
                                    icon={<Warning />}
                                    label="Exercise Caution"
                                    sx={{
                                      py: 2,
                                      px: 3,
                                      fontSize: '1rem',
                                      fontWeight: 'bold',
                                      background: FINANCE_COLORS.gradient.danger,
                                      color: 'white',
                                      '& .MuiChip-icon': {
                                        color: 'white'
                                      }
                                    }}
                                  />
                                )}
                              </Box>
                            </Box>
                          </TickerAnalysisCard>
                        ))}
                      </Stack>
                    </Box>
                  )}

                  {/* Investment Summary */}
                  {articleAnalysis.investment_summary && (
                    <GlassCard sx={{ p: 3, background: alpha(FINANCE_COLORS.primary, 0.05) }}>
                      <Typography variant="h6" gutterBottom>
                        Investment Summary
                      </Typography>
                      <Grid container spacing={2}>
                        <Grid item xs={4}>
                          <Stack alignItems="center">
                            <Typography variant="h4" color="success.main" fontWeight="bold">
                              {articleAnalysis.investment_summary.buy_signals}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              Buy Signals
                            </Typography>
                          </Stack>
                        </Grid>
                        <Grid item xs={4}>
                          <Stack alignItems="center">
                            <Typography variant="h4" color="warning.main" fontWeight="bold">
                              {articleAnalysis.investment_summary.hold_signals}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              Hold Signals
                            </Typography>
                          </Stack>
                        </Grid>
                        <Grid item xs={4}>
                          <Stack alignItems="center">
                            <Typography variant="h4" color="error.main" fontWeight="bold">
                              {articleAnalysis.investment_summary.sell_signals}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              Sell Signals
                            </Typography>
                          </Stack>
                        </Grid>
                      </Grid>
                      
                      {articleAnalysis.investment_summary.top_pick && (
                        <Alert severity="success" sx={{ mt: 2 }}>
                          <Typography variant="body2">
                            <strong>Top Pick:</strong> {articleAnalysis.investment_summary.top_pick.ticker} - 
                            {articleAnalysis.investment_summary.top_pick.signal}
                          </Typography>
                        </Alert>
                      )}
                      
                      {articleAnalysis.investment_summary.avoid && (
                        <Alert severity="error" sx={{ mt: 2 }}>
                          <Typography variant="body2">
                            <strong>Avoid:</strong> {articleAnalysis.investment_summary.avoid.ticker} - 
                            {articleAnalysis.investment_summary.avoid.signal}
                          </Typography>
                        </Alert>
                      )}
                    </GlassCard>
                  )}
                </Stack>
              ) : (
                <Alert severity="error">
                  Failed to analyze article. Please try again.
                </Alert>
              )}
            </DialogContent>
            
            <DialogActions sx={{ p: 3 }}>
              <Button
                component="a"
                href={selectedArticle.url}
                target="_blank"
                rel="noopener noreferrer"
                startIcon={<LinkIcon />}
                variant="outlined"
              >
                Read Full Article
              </Button>
              <Button onClick={handleCloseModal} variant="contained">
                Close
              </Button>
            </DialogActions>
          </>
        )}
      </StyledDialog>
    </StyledContainer>
  );
};

export default NewsAnalyzer;