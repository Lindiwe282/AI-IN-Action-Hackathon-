import React, { useState, useEffect, useRef, useCallback } from 'react';
import { 
  Container, Typography, Box, Card, CardContent, Grid, Paper, Button, 
  IconButton, InputBase, Chip, Alert, Snackbar, Modal, CircularProgress,
  LinearProgress, Stack, Avatar, Divider, Tooltip, List, ListItem, ListItemText,
  useMediaQuery, CardHeader, CardActions, Dialog, DialogTitle, DialogContent, 
  DialogActions, Fade, AlertTitle
} from '@mui/material';
import { 
  TrendingUp, SearchRounded, Add, Delete, Analytics, ShowChart, 
  PieChart as PieIcon, AccountBalance, TrendingDown, Refresh,
  PlayCircle, StopCircle, CheckCircle, Error, Visibility, Close,
  NewspaperOutlined, SignalCellularAlt, Info, AutoGraph, TipsAndUpdates
} from '@mui/icons-material';
import { 
  PieChart, Cell, Pie, LineChart, Line, XAxis, YAxis, CartesianGrid, 
  Tooltip as ChartTooltip, Legend, ResponsiveContainer 
} from 'recharts';
import { styled, useTheme, alpha } from '@mui/material/styles';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const URL_API = 'http://localhost:5000/api';

// Chart colors for consistent theming
const CHART_COLORS = [
  '#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#8dd1e1', 
  '#d084d0', '#87d068', '#ffa726', '#ef5350', '#5c6bc0'
];

// Custom styled components with financial coach theme
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
      ? '0 12px 48px 0 rgba(0, 0, 0, 0.5)'
      : '0 12px 48px 0 rgba(31, 38, 135, 0.25)',
  }
}));

const HeaderBox = styled(Box)(({ theme }) => ({
  background: theme.palette.mode === 'dark' 
    ? 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)' 
    : 'linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%)',
  padding: theme.spacing(3),
  borderRadius: theme.spacing(3),
  marginBottom: theme.spacing(4),
  boxShadow: theme.palette.mode === 'dark'
    ? '0 8px 32px rgba(0,0,0,0.8)'
    : '0 8px 32px rgba(0,0,0,0.08)',
  backdropFilter: 'blur(10px)',
  border: '1px solid',
  borderColor: theme.palette.mode === 'dark'
    ? 'rgba(255,255,255,0.1)'
    : 'rgba(0,0,0,0.05)',
}));

const SearchBox = styled(Paper)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  borderRadius: theme.spacing(3),
  padding: '4px 16px',
  background: theme.palette.mode === 'dark'
    ? 'rgba(255,255,255,0.05)'
    : 'rgba(0,0,0,0.02)',
  border: '1px solid',
  borderColor: theme.palette.mode === 'dark'
    ? 'rgba(255,255,255,0.1)'
    : 'rgba(0,0,0,0.08)',
  transition: 'all 0.3s ease',
  '&:hover': {
    borderColor: theme.palette.primary.main,
    boxShadow: `0 0 0 2px ${alpha(theme.palette.primary.main, 0.1)}`,
  },
}));

const StatusChip = styled(Chip)(({ theme, status }) => ({
  borderRadius: theme.spacing(2),
  fontWeight: 600,
  background: status === 'connected' 
    ? 'linear-gradient(45deg, #4caf50 30%, #81c784 90%)'
    : status === 'running'
    ? 'linear-gradient(45deg, #2196f3 30%, #64b5f6 90%)'
    : 'linear-gradient(45deg, #f44336 30%, #ef5350 90%)',
  color: 'white',
  '& .MuiChip-icon': {
    color: 'white',
  }
}));

const PortfolioChip = styled(Chip)(({ theme }) => ({
  margin: theme.spacing(0.5),
  borderRadius: theme.spacing(2),
  background: alpha(theme.palette.primary.main, 0.1),
  border: `1px solid ${alpha(theme.palette.primary.main, 0.3)}`,
  '&:hover': {
    background: alpha(theme.palette.primary.main, 0.2),
  }
}));

const StockCard = styled(Card)(({ theme, trend }) => ({
  background: theme.palette.mode === 'dark'
    ? 'rgba(255, 255, 255, 0.05)'
    : 'rgba(255, 255, 255, 0.95)',
  backdropFilter: 'blur(10px)',
  borderRadius: theme.spacing(2),
  border: `1px solid ${trend === 'up' 
    ? alpha('#4caf50', 0.3) 
    : trend === 'down' 
    ? alpha('#f44336', 0.3) 
    : alpha(theme.palette.primary.main, 0.3)}`,
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  position: 'relative',
  overflow: 'hidden',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: theme.palette.mode === 'dark'
      ? '0 8px 25px rgba(0, 0, 0, 0.4)'
      : '0 8px 25px rgba(0, 0, 0, 0.15)',
    border: `1px solid ${trend === 'up' 
      ? '#4caf50' 
      : trend === 'down' 
      ? '#f44336' 
      : theme.palette.primary.main}`,
  },
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: '3px',
    background: trend === 'up' 
      ? 'linear-gradient(90deg, #4caf50 0%, #81c784 100%)' 
      : trend === 'down' 
      ? 'linear-gradient(90deg, #f44336 0%, #ef5350 100%)'
      : 'linear-gradient(90deg, #2196f3 0%, #64b5f6 100%)',
  }
}));

const AnalysisModal = styled(Box)(({ theme }) => ({
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '90%',
  maxWidth: 1200,
  maxHeight: '90vh',
  overflow: 'auto',
  background: theme.palette.mode === 'dark'
    ? 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)'
    : 'linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%)',
  borderRadius: theme.spacing(3),
  boxShadow: theme.palette.mode === 'dark'
    ? '0 20px 60px rgba(0,0,0,0.8)'
    : '0 20px 60px rgba(0,0,0,0.15)',
  padding: theme.spacing(4),
  border: '1px solid',
  borderColor: theme.palette.mode === 'dark'
    ? 'rgba(255,255,255,0.1)'
    : 'rgba(0,0,0,0.08)',
}));

const ModalBox = styled(Box)(({ theme }) => ({
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 450,
  background: theme.palette.mode === 'dark'
    ? 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)'
    : 'linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%)',
  borderRadius: theme.spacing(3),
  boxShadow: theme.palette.mode === 'dark'
    ? '0 20px 40px rgba(0,0,0,0.8)'
    : '0 20px 40px rgba(0,0,0,0.2)',
  padding: theme.spacing(4),
  border: '1px solid',
  borderColor: theme.palette.mode === 'dark'
    ? 'rgba(255,255,255,0.1)'
    : 'rgba(0,0,0,0.08)',
}));

const StrategyCard = styled(Card)(({ theme }) => ({
  background: theme.palette.mode === 'dark' 
    ? 'rgba(255,255,255,0.03)' 
    : 'rgba(255,255,255,0.9)',
  backdropFilter: 'blur(20px)',
  borderRadius: theme.spacing(3),
  border: '1px solid',
  borderColor: theme.palette.mode === 'dark'
    ? 'rgba(255,255,255,0.1)'
    : 'rgba(0,0,0,0.08)',
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  overflow: 'hidden',
  position: 'relative',
  '&:hover': {
    transform: 'translateY(-8px)',
    boxShadow: theme.palette.mode === 'dark'
      ? '0 20px 40px rgba(0,0,0,0.5)'
      : '0 20px 40px rgba(0,0,0,0.1)',
  },
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: '4px',
    background: 'linear-gradient(45deg, #2196f3 30%, #4caf50 90%)',
  }
}));

// Custom tooltip for charts
const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <Paper sx={{ p: 1.5, background: 'rgba(0, 0, 0, 0.8)', border: '1px solid rgba(255, 255, 255, 0.2)', borderRadius: 1 }}>
        <Typography variant="body2" sx={{ color: 'white', fontWeight: 'bold' }}>
          {payload[0].name}
        </Typography>
        <Typography variant="body2" sx={{ color: payload[0].payload.fill }}>
          {`${payload[0].value.toFixed(2)}%`}
        </Typography>
      </Paper>
    );
  }
  return null;
};

const Investment = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  // State management
  const [portfolio, setPortfolio] = useState(['AAPL', 'GOOGL', 'MSFT', 'NVDA', 'AMZN']);
  const [stocks, setStocks] = useState([]);
  const [searchText, setSearchText] = useState('');
  const [filteredStocks, setFilteredStocks] = useState([]);
  const [showSearchResults, setShowSearchResults] = useState(false);
  const [portfolioAnalysis, setPortfolioAnalysis] = useState(null);
  const [stockPrices, setStockPrices] = useState({});
  const [loading, setLoading] = useState(false);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [metricDetailsOpen, setMetricDetailsOpen] = useState(false);
  const [selectedStock, setSelectedStock] = useState(null);
  const [stockModalOpen, setStockModalOpen] = useState(false);
  
  const searchInputRef = useRef(null);
  
  // Fetch stocks on component mount
  useEffect(() => {
    fetchStocks();
  }, []);

  // Fetch portfolio analysis when portfolio changes
  useEffect(() => {
    if (portfolio.length > 0) {
      fetchPortfolioAnalysis();
      fetchStockPrices(); // Also fetch prices when portfolio changes
    }
  }, [portfolio]);

  const fetchStocks = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${URL_API}/stocks`);
      setStocks(response.data || []);
    } catch (error) {
      console.error('Error fetching stocks:', error);
      setSnackbar({ open: true, message: 'Failed to fetch stocks', severity: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const fetchPortfolioAnalysis = async () => {
    if (portfolio.length === 0) return;
    
    try {
      setAnalysisLoading(true);
      // Use the correct API endpoint
      const response = await axios.post(`${URL_API}/analysis`, {
        tickers: portfolio
      });
      
      if (response.data && response.data.success) {
        setPortfolioAnalysis(response.data.data);
      } else {
        throw new Error(response.data?.error || 'Analysis failed');
      }
    } catch (error) {
      console.error('Error fetching portfolio analysis:', error);
      setSnackbar({ open: true, message: error.response?.data?.error || 'Failed to analyze portfolio', severity: 'error' });
    } finally {
      setAnalysisLoading(false);
    }
  };

  const fetchStockPrices = async () => {
    if (portfolio.length === 0) return;
    
    try {
      console.log('Fetching stock prices for:', portfolio);
      
      // Use the correct stock-prices endpoint with individual requests for better reliability
      const pricePromises = portfolio.map(async (ticker) => {
        try {
          const response = await axios.get(`${URL_API}/stock-prices?tickers=${ticker}`);
          console.log(`Response for ${ticker}:`, response.data);
          
          if (response.data && Array.isArray(response.data) && response.data.length > 0) {
            const stockData = response.data[0];
            return {
              ticker: stockData.ticker || ticker,
              price: stockData.price,
              change: stockData.change,
              change_percent: stockData.change_percent,
              error: stockData.error
            };
          } else if (response.data && !Array.isArray(response.data)) {
            // Handle single stock response format
            return {
              ticker: response.data.ticker || ticker,
              price: response.data.price,
              change: response.data.change,
              change_percent: response.data.change_percent,
              error: response.data.error
            };
          } else {
            console.warn(`No data received for ${ticker}`);
            return {
              ticker,
              price: null,
              change: null,
              change_percent: null,
              error: 'No data available'
            };
          }
        } catch (error) {
          console.error(`Error fetching price for ${ticker}:`, error);
          return {
            ticker,
            price: null,
            change: null,
            change_percent: null,
            error: error.message
          };
        }
      });
      
      const stockPriceResults = await Promise.allSettled(pricePromises);
      const stockPriceData = {};
      
      stockPriceResults.forEach((result, index) => {
        const ticker = portfolio[index];
        if (result.status === 'fulfilled' && result.value) {
          stockPriceData[ticker] = {
            price: result.value.price,
            change: result.value.change,
            change_percent: result.value.change_percent,
            error: result.value.error
          };
        } else {
          console.error(`Failed to fetch price for ${ticker}:`, result.reason);
          stockPriceData[ticker] = {
            price: null,
            change: null,
            change_percent: null,
            error: 'Failed to fetch'
          };
        }
      });
      
      console.log('Final stock price data:', stockPriceData);
      setStockPrices(stockPriceData);
      
    } catch (error) {
      console.error('Error in fetchStockPrices:', error);
      setSnackbar({ 
        open: true, 
        message: `Failed to fetch stock prices: ${error.message}`, 
        severity: 'warning' 
      });
    }
  };

  const handleSearch = (e) => {
    const value = e.target.value;
    setSearchText(value);
    
    if (value.trim() === '') {
      setFilteredStocks([]);
      setShowSearchResults(false);
    } else {
      const filtered = stocks.filter(stock =>
        stock.name?.toLowerCase().includes(value.toLowerCase()) ||
        stock.ticker?.toLowerCase().includes(value.toLowerCase())
      );
      setFilteredStocks(filtered);
      setShowSearchResults(true);
    }
  };

  const addToPortfolio = (stock) => {
    if (!portfolio.includes(stock.ticker)) {
      setPortfolio([...portfolio, stock.ticker]);
      setSnackbar({ open: true, message: `${stock.ticker} added to portfolio`, severity: 'success' });
    }
    setSearchText('');
    setShowSearchResults(false);
  };

  const handleStockClick = (stock) => {
    setSelectedStock(stock);
    setStockModalOpen(true);
    setShowSearchResults(false);
  };

  const handleStockModalClose = () => {
    setStockModalOpen(false);
    setSelectedStock(null);
  };

  const removeFromPortfolio = (ticker) => {
    setPortfolio(portfolio.filter(t => t !== ticker));
    setSnackbar({ open: true, message: `${ticker} removed from portfolio`, severity: 'info' });
  };

  const runAnalysis = async () => {
    if (portfolio.length === 0) {
      setSnackbar({ open: true, message: 'Please add stocks to your portfolio first', severity: 'warning' });
      return;
    }
    
    try {
      setIsAnalyzing(true);
      
      // Use the investment-suggestions endpoint with correct data structure
      const response = await axios.post(`${URL_API}/investment-suggestions`, {
        age: 30,
        monthly_income: 5000,
        current_savings: 10000,
        risk_tolerance: 'medium',
        investment_experience: 'beginner',
        investment_timeline: 10,
        current_portfolio: portfolio
      });
      
      if (response.data && response.data.success) {
        setSnackbar({ open: true, message: 'Analysis completed successfully!', severity: 'success' });
        // Refresh portfolio analysis with the main analysis endpoint
        await fetchPortfolioAnalysis();
      } else {
        throw new Error(response.data?.error || 'Analysis failed');
      }
    } catch (error) {
      console.error('Error running analysis:', error);
      const errorMessage = error.response?.data?.error || error.response?.data?.message || 'Analysis failed';
      setSnackbar({ open: true, message: errorMessage, severity: 'error' });
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Prepare chart data
  const preparePieChartData = () => {
    if (!portfolioAnalysis?.strategies || portfolioAnalysis.strategies.length === 0) return [];
    
    // Find the strategy with the highest total return
    const bestStrategy = portfolioAnalysis.strategies.reduce((best, current) => {
      const currentReturn = current.metrics?.total_return || 0;
      const bestReturn = best.metrics?.total_return || 0;
      return currentReturn > bestReturn ? current : best;
    });
    
    if (!bestStrategy?.ticker_allocation) return [];
    
    return Object.entries(bestStrategy.ticker_allocation)
      .filter(([_, weight]) => weight > 0) // Keep all positive weights, no matter how small
      .map(([ticker, weight], index) => ({
        name: ticker,
        value: weight * 100, // Convert to percentage
        fill: CHART_COLORS[index % CHART_COLORS.length]
      }));
  };

  const preparePerformanceData = () => {
    if (!portfolioAnalysis?.strategies || portfolioAnalysis.strategies.length === 0) return [];
    
    return portfolioAnalysis.strategies.map(strategy => ({
      name: strategy.name,
      'Total Return (%)': (strategy.metrics.total_return * 100).toFixed(2),
      'Volatility (%)': (strategy.metrics.volatility * 100).toFixed(2),
      'Sharpe Ratio': strategy.metrics.sharpe_ratio.toFixed(3)
    }));
  };

  // Prepare return chart data for detailed analysis
  const prepareReturnChartData = (strategies) => {
    if (!strategies || strategies.length === 0) return [];
    
    const totalDataPoints = strategies[0].portfolio_return?.length || 0;
    const displayPoints = Math.min(30, totalDataPoints);
    const startIndex = Math.max(0, totalDataPoints - displayPoints);
    
    const chartData = [];
    const today = new Date();
    
    for (let i = startIndex; i < totalDataPoints; i++) {
      const daysAgo = totalDataPoints - i - 1;
      const date = new Date(today);
      date.setDate(date.getDate() - daysAgo);
      
      const point = { 
        day: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        fullDate: date.toISOString()
      };
      
      strategies.forEach((strategy) => {
        if (strategy.portfolio_return && strategy.portfolio_return[i] !== undefined) {
          point[strategy.name] = (strategy.portfolio_return[i] * 100).toFixed(4);
        }
      });
      chartData.push(point);
    }
    
    return chartData;
  };

  return (
    <StyledContainer maxWidth="xl">
      {/* Header Section */}
      <HeaderBox>
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={6}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Avatar sx={{ bgcolor: theme.palette.primary.main, width: 56, height: 56 }}>
                <TrendingUp fontSize="large" />
              </Avatar>
              <Box>
                <Typography variant="h4" fontWeight="bold" color="primary">
                  AI Investment Advisory
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  Smart portfolio optimization and financial literacy insights
                </Typography>
              </Box>
            </Box>
          </Grid>
          <Grid item xs={12} md={6}>
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
              <StatusChip
                icon={<CheckCircle />}
                label="Connected"
                status="connected"
              />
              <Button
                variant="contained"
                startIcon={<NewspaperOutlined />}
                onClick={() => navigate('/news-analyzer')}
                sx={{
                  borderRadius: 3,
                  textTransform: 'none',
                  background: 'linear-gradient(45deg, #dc004e 30%, #f48fb1 90%)',
                }}
              >
                Analyze News
              </Button>
            </Box>
          </Grid>
        </Grid>
      </HeaderBox>

      {/* Main Content Grid */}
      <Grid container spacing={4}>
        {/* Portfolio Selection */}
        <Grid item xs={12} lg={4}>
          <GlassCard sx={{ height: 'fit-content' }}>
            <CardHeader
              title={
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <AccountBalance color="primary" />
                  <Typography variant="h6" fontWeight="bold">
                    Portfolio Selection
                  </Typography>
                </Box>
              }
              action={
                <Tooltip title="Refresh Analysis">
                  <IconButton onClick={fetchPortfolioAnalysis} disabled={analysisLoading}>
                    {analysisLoading ? <CircularProgress size={20} /> : <Refresh />}
                  </IconButton>
                </Tooltip>
              }
            />
            <CardContent>
              {/* Stock Search */}
              <SearchBox>
                <SearchRounded sx={{ mr: 1, color: 'text.secondary' }} />
                <InputBase
                  ref={searchInputRef}
                  placeholder="Search stocks (e.g., AAPL, Tesla)..."
                  value={searchText}
                  onChange={handleSearch}
                  sx={{ flex: 1 }}
                />
              </SearchBox>
              
              {/* Search Results */}
              {showSearchResults && (
                <Paper sx={{ 
                  mt: 1, 
                  maxHeight: 300, 
                  overflow: 'auto',
                  borderRadius: 2,
                  border: '1px solid',
                  borderColor: 'divider'
                }}>
                  <List sx={{ p: 1 }}>
                    {filteredStocks.slice(0, 5).map((stock) => (
                      <ListItem
                        key={stock.ticker}
                        button
                        onClick={() => handleStockClick(stock)}
                        sx={{
                          cursor: 'pointer',
                          borderRadius: 2,
                          mb: 0.5,
                          transition: 'all 0.2s ease',
                          '&:hover': {
                            backgroundColor: alpha(theme.palette.primary.main, 0.1),
                            transform: 'translateX(4px)',
                          },
                        }}
                      >
                        <Avatar 
                          sx={{ 
                            mr: 2, 
                            width: 40, 
                            height: 40,
                            background: 'linear-gradient(45deg, #2196f3 30%, #64b5f6 90%)',
                            fontSize: '0.875rem',
                            fontWeight: 'bold'
                          }}
                        >
                          {stock.ticker.substring(0, 2)}
                        </Avatar>
                        
                        <ListItemText
                          primary={
                            <Stack direction="row" justifyContent="space-between" alignItems="center">
                              <Box>
                                <Typography variant="body1" fontWeight="bold">
                                  {stock.ticker}
                                </Typography>
                                <Typography variant="body2" color="text.secondary" sx={{ 
                                  overflow: 'hidden',
                                  textOverflow: 'ellipsis',
                                  whiteSpace: 'nowrap',
                                  maxWidth: '200px'
                                }}>
                                  {stock.name}
                                </Typography>
                              </Box>
                              
                              <Stack direction="row" alignItems="center" spacing={1}>
                                <Chip 
                                  label="Add"
                                  size="small"
                                  sx={{ 
                                    background: alpha(theme.palette.success.main, 0.1),
                                    color: 'success.main',
                                    border: '1px solid',
                                    borderColor: alpha(theme.palette.success.main, 0.3),
                                    fontWeight: 'medium'
                                  }}
                                />
                                <Visibility sx={{ 
                                  color: 'primary.main',
                                  fontSize: 20
                                }} />
                              </Stack>
                            </Stack>
                          }
                        />
                      </ListItem>
                    ))}
                    
                    {filteredStocks.length === 0 && (
                      <ListItem>
                        <ListItemText
                          primary={
                            <Typography variant="body2" color="text.secondary" textAlign="center">
                              No stocks found matching your search
                            </Typography>
                          }
                        />
                      </ListItem>
                    )}
                  </List>
                </Paper>
              )}
              
              {/* Current Portfolio */}
              <Box sx={{ mt: 3 }}>
                <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
                  <Typography variant="subtitle1" fontWeight="bold">
                    Current Portfolio ({portfolio.length} stocks)
                  </Typography>
                  
                  {/* Portfolio Summary */}
                  {/* {portfolio.length > 0 && Object.keys(stockPrices).length > 0 && (
                    <Box sx={{ textAlign: 'right' }}>
                      {(() => {
                        const validPrices = portfolio.filter(ticker => 
                          stockPrices[ticker] && !stockPrices[ticker].error && stockPrices[ticker].price
                        );
                        
                        if (validPrices.length === 0) return null;
                        
                        const totalValue = validPrices.reduce((sum, ticker) => 
                          sum + (stockPrices[ticker].price || 0), 0
                        );
                        
                        const avgChange = validPrices.reduce((sum, ticker) => 
                          sum + (stockPrices[ticker].change_percent || 0), 0
                        ) / validPrices.length;
                        
                        return (
                          <>
                            <Typography variant="h6" fontWeight="bold">
                              ${totalValue.toFixed(2)}
                            </Typography>
                            <Typography 
                              variant="caption" 
                              sx={{ 
                                color: avgChange >= 0 ? '#4caf50' : '#f44336',
                                fontWeight: 'medium'
                              }}
                            >
                              {avgChange >= 0 ? '+' : ''}{avgChange.toFixed(2)}% avg
                            </Typography>
                          </>
                        );
                      })()}
                    </Box>
                  )} */}
                </Stack>
                
                {portfolio.length === 0 ? (
                  <Paper sx={{ 
                    p: 3, 
                    textAlign: 'center', 
                    border: '2px dashed',
                    borderColor: 'divider',
                    borderRadius: 2,
                    mt: 2
                  }}>
                    <Typography variant="body2" color="text.secondary">
                      No stocks in portfolio. Search and add stocks to get started.
                    </Typography>
                  </Paper>
                ) : (
                  <Grid container spacing={1.5} sx={{ mt: 1 }}>
                    {portfolio.map((ticker) => {
                      const stockPrice = stockPrices[ticker];
                      const trend = stockPrice?.change_percent 
                        ? (stockPrice.change_percent >= 0 ? 'up' : 'down')
                        : 'neutral';
                      
                      return (
                        <Grid item xs={12} sm={6} key={ticker}>
                          <StockCard trend={trend}>
                            <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                              <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
                                <Box sx={{ flex: 1 }}>
                                  <Typography variant="h6" fontWeight="bold" color="primary">
                                    {ticker}
                                  </Typography>
                                  
                                  {stockPrice && !stockPrice.error ? (
                                    <Stack spacing={0.5} sx={{ mt: 1 }}>
                                      <Typography variant="h5" fontWeight="bold">
                                        ${stockPrice.price?.toFixed(2) || 'N/A'}
                                      </Typography>
                                      
                                      {stockPrice.change_percent !== null && (
                                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                          {trend === 'up' ? (
                                            <TrendingUp sx={{ 
                                              fontSize: 16, 
                                              color: '#4caf50' 
                                            }} />
                                          ) : (
                                            <TrendingDown sx={{ 
                                              fontSize: 16, 
                                              color: '#f44336' 
                                            }} />
                                          )}
                                          
                                          <Typography 
                                            variant="body2" 
                                            fontWeight="medium"
                                            sx={{ 
                                              color: trend === 'up' ? '#4caf50' : '#f44336'
                                            }}
                                          >
                                            {trend === 'up' ? '+' : ''}{stockPrice.change_percent.toFixed(2)}%
                                          </Typography>
                                          
                                          <Typography variant="caption" color="text.secondary">
                                            (${stockPrice.change?.toFixed(2) || '0.00'})
                                          </Typography>
                                        </Box>
                                      )}
                                      
                                      <Typography variant="caption" color="text.secondary">
                                        Live Price
                                      </Typography>
                                    </Stack>
                                  ) : (
                                    <Stack spacing={0.5} sx={{ mt: 1 }}>
                                      <Typography variant="body2" color="text.secondary">
                                        {stockPrice?.error || 'Loading price...'}
                                      </Typography>
                                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                        <CircularProgress size={12} />
                                        <Typography variant="caption" color="text.secondary">
                                          Fetching data
                                        </Typography>
                                      </Box>
                                    </Stack>
                                  )}
                                </Box>
                                
                                <IconButton 
                                  onClick={() => removeFromPortfolio(ticker)}
                                  size="small"
                                  sx={{ 
                                    color: 'text.secondary',
                                    '&:hover': {
                                      color: 'error.main',
                                      backgroundColor: alpha(theme.palette.error.main, 0.1)
                                    }
                                  }}
                                >
                                  <Delete fontSize="small" />
                                </IconButton>
                              </Stack>
                              
                              {/* Performance indicator */}
                              {stockPrice && !stockPrice.error && stockPrice.change_percent !== null && (
                                <Box sx={{ 
                                  mt: 2,
                                  p: 1,
                                  borderRadius: 1,
                                  background: trend === 'up' 
                                    ? alpha('#4caf50', 0.1)
                                    : alpha('#f44336', 0.1)
                                }}>
                                  <Typography variant="caption" sx={{ 
                                    color: trend === 'up' ? '#4caf50' : '#f44336',
                                    fontWeight: 'medium'
                                  }}>
                                    {trend === 'up' ? '📈 Gaining' : '📉 Declining'} today
                                  </Typography>
                                </Box>
                              )}
                            </CardContent>
                          </StockCard>
                        </Grid>
                      );
                    })}
                  </Grid>
                )}
              </Box>
              
              {/* Action Button */}
              <Button
                fullWidth
                variant="contained"
                size="large"
                onClick={runAnalysis}
                disabled={isAnalyzing || portfolio.length === 0}
                startIcon={isAnalyzing ? <CircularProgress size={20} /> : <Analytics />}
                sx={{ 
                  mt: 3, 
                  borderRadius: 3,
                  textTransform: 'none',
                  background: 'linear-gradient(45deg, #1976d2 30%, #64b5f6 90%)'
                }}
              >
                {isAnalyzing ? 'Analyzing...' : 'Run Portfolio Analysis'}
              </Button>
            </CardContent>
          </GlassCard>
        </Grid>

        {/* Portfolio Visualization */}
        <Grid item xs={12} lg={8}>
          <Grid container spacing={3}>
            {/* Asset Allocation Chart */}
            <Grid item xs={12} md={6}>
              <GlassCard sx={{ height: 400 }}>
                <CardHeader
                  title={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <PieIcon color="primary" />
                      <Typography variant="h6" fontWeight="bold">
                        Asset Allocation
                      </Typography>
                    </Box>
                  }
                />
                <CardContent>
                  {analysisLoading ? (
                    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 250 }}>
                      <CircularProgress />
                    </Box>
                  ) : (
                    <>
                      <ResponsiveContainer width="100%" height={200}>
                        <PieChart>
                          <Pie
                            data={preparePieChartData()}
                            cx="50%"
                            cy="50%"
                            outerRadius={70}
                            dataKey="value"
                          >
                            {preparePieChartData().map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={entry.fill} />
                            ))}
                          </Pie>
                          <ChartTooltip content={<CustomTooltip />} />
                          <Legend />
                        </PieChart>
                      </ResponsiveContainer>
                      
                      {/* Strategy Name */}
                      {portfolioAnalysis?.comparison?.best_performer && (
                        <Box sx={{ mt: 2, textAlign: 'center' }}>
                          <Typography variant="body2" color="text.secondary" gutterBottom>
                            Strategy:
                          </Typography>
                          <Chip 
                            label={portfolioAnalysis.comparison.best_performer}
                            size="small"
                            sx={{ 
                              background: 'linear-gradient(45deg, #2196f3 30%, #4caf50 90%)',
                              color: 'white',
                              fontWeight: 'bold'
                            }}
                          />
                        </Box>
                      )}
                    </>
                  )}
                </CardContent>
              </GlassCard>
            </Grid>

            {/* Performance Metrics */}
            <Grid item xs={12} md={6}>
              <GlassCard sx={{ height: 400 }}>
                <CardHeader
                  title={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <ShowChart color="primary" />
                      <Typography variant="h6" fontWeight="bold">
                        Performance Metrics
                      </Typography>
                    </Box>
                  }
                  action={
                    portfolioAnalysis?.strategies && portfolioAnalysis.strategies.length > 0 && (
                      <Button
                        size="small"
                        variant="outlined"
                        startIcon={<Info />}
                        onClick={() => setMetricDetailsOpen(true)}
                        sx={{
                          borderRadius: 2,
                          textTransform: 'none',
                          fontSize: '0.75rem'
                        }}
                      >
                        Metric Details
                      </Button>
                    )
                  }
                />
                <CardContent>
                  {analysisLoading ? (
                    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 250 }}>
                      <CircularProgress />
                    </Box>
                  ) : portfolioAnalysis?.strategies && portfolioAnalysis.strategies.length > 0 ? (
                    <Stack spacing={3}>
                      {portfolioAnalysis.strategies.map((strategy, index) => (
                        <Box key={index}>
                          <Typography variant="h6" color="primary" gutterBottom>
                            {strategy.name}
                          </Typography>
                          <Grid container spacing={2}>
                            <Grid item xs={4}>
                              <Typography variant="body2" color="text.secondary" gutterBottom>
                                Annualized Return
                              </Typography>
                              <Typography variant="h6" fontWeight="bold" color="success.main">
                                {strategy.metrics.annualized_return ? 
                                  (strategy.metrics.annualized_return * 100).toFixed(2) + '%' :
                                  ((Math.pow(1 + strategy.metrics.total_return, 1/strategy.metrics.years_analyzed) - 1) * 100).toFixed(2) + '%'
                                }
                              </Typography>
                            </Grid>
                            <Grid item xs={4}>
                              <Typography variant="body2" color="text.secondary" gutterBottom>
                                Volatility
                              </Typography>
                              <Typography variant="h6" fontWeight="bold" color="warning.main">
                                {(strategy.metrics.volatility * 100).toFixed(2)}%
                              </Typography>
                            </Grid>
                            <Grid item xs={4}>
                              <Typography variant="body2" color="text.secondary" gutterBottom>
                                Sharpe Ratio
                              </Typography>
                              <Typography variant="h6" fontWeight="bold" color="info.main">
                                {strategy.metrics.sharpe_ratio.toFixed(3)}
                              </Typography>
                            </Grid>
                          </Grid>
                          {index < portfolioAnalysis.strategies.length - 1 && <Divider sx={{ mt: 2 }} />}
                        </Box>
                      ))}
                      
                      {portfolioAnalysis.comparison && (
                        <Box sx={{ mt: 3, p: 2, bgcolor: 'background.paper', borderRadius: 2 }}>
                          <Typography variant="subtitle2" color="primary" gutterBottom>
                            Recommendation: {portfolioAnalysis.comparison.best_performer}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {portfolioAnalysis.comparison.recommendation}
                          </Typography>
                        </Box>
                      )}
                    </Stack>
                  ) : (
                    <Box sx={{ textAlign: 'center', py: 4 }}>
                      <Typography variant="body1" color="text.secondary">
                        Run analysis to see performance metrics
                      </Typography>
                    </Box>
                  )}
                </CardContent>
              </GlassCard>
            </Grid>

            {/* Financial Literacy Tips */}
            <Grid item xs={12}>
              <GlassCard>
                <CardHeader
                  title={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <SignalCellularAlt color="primary" />
                      <Typography variant="h6" fontWeight="bold">
                        Financial Literacy Insights
                      </Typography>
                    </Box>
                  }
                />
                <CardContent>
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={4}>
                      <Box sx={{ textAlign: 'center', p: 2 }}>
                        <Avatar sx={{ bgcolor: theme.palette.success.main, mx: 'auto', mb: 2 }}>
                          <TrendingUp />
                        </Avatar>
                        <Typography variant="h6" fontWeight="bold" gutterBottom>
                          Diversification
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Spread risk across different assets and sectors to optimize your portfolio's risk-return profile.
                        </Typography>
                      </Box>
                    </Grid>
                    
                    <Grid item xs={12} md={4}>
                      <Box sx={{ textAlign: 'center', p: 2 }}>
                        <Avatar sx={{ bgcolor: theme.palette.info.main, mx: 'auto', mb: 2 }}>
                          <Analytics />
                        </Avatar>
                        <Typography variant="h6" fontWeight="bold" gutterBottom>
                          Risk Management
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Understanding volatility and using metrics like Sharpe ratio helps make informed investment decisions.
                        </Typography>
                      </Box>
                    </Grid>
                    
                    <Grid item xs={12} md={4}>
                      <Box sx={{ textAlign: 'center', p: 2 }}>
                        <Avatar sx={{ bgcolor: theme.palette.warning.main, mx: 'auto', mb: 2 }}>
                          <ShowChart />
                        </Avatar>
                        <Typography variant="h6" fontWeight="bold" gutterBottom>
                          Long-term Thinking
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Focus on long-term growth rather than short-term market fluctuations for better investment outcomes.
                        </Typography>
                      </Box>
                    </Grid>
                  </Grid>
                </CardContent>
              </GlassCard>
            </Grid>
          </Grid>
        </Grid>
      </Grid>

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

      {/* Metric Details Modal */}
      <Dialog
        open={metricDetailsOpen}
        onClose={() => setMetricDetailsOpen(false)}
        maxWidth="lg"
        fullWidth
        PaperProps={{
          sx: {
            borderRadius: 3,
            background: theme.palette.mode === 'dark'
              ? 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)'
              : 'linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%)',
            backdropFilter: 'blur(20px)',
          }
        }}
        TransitionComponent={Fade}
        TransitionProps={{ timeout: 300 }}
      >
        <DialogTitle>
          <Stack direction="row" alignItems="center" justifyContent="space-between">
            <Stack direction="row" alignItems="center" spacing={2}>
              <Avatar sx={{ 
                bgcolor: 'primary.main', 
                background: 'linear-gradient(45deg, #2196f3 30%, #4caf50 90%)' 
              }}>
                <Analytics />
              </Avatar>
              <Box>
                <Typography variant="h5" fontWeight="bold">
                  Portfolio Analysis Report
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Detailed metrics and performance comparison
                </Typography>
              </Box>
            </Stack>
            <IconButton onClick={() => setMetricDetailsOpen(false)}>
              <Close />
            </IconButton>
          </Stack>
        </DialogTitle>
        
        <DialogContent dividers>
          {portfolioAnalysis?.strategies && portfolioAnalysis.strategies.length > 0 ? (
            <Stack spacing={4}>
              {/* Market Conditions */}
              <Paper elevation={0} sx={{ p: 3, borderRadius: 2, background: alpha(theme.palette.primary.main, 0.05) }}>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <TrendingUp color="primary" />
                  Market Conditions
                </Typography>
                <Grid container spacing={3}>
                  <Grid item xs={12} md={3}>
                    <Typography variant="caption" color="text.secondary">MARKET STATUS</Typography>
                    <Typography variant="h6" sx={{ 
                      color: portfolioAnalysis.metadata?.market_conditions?.condition === 'bull' ? 'success.main' : 
                             portfolioAnalysis.metadata?.market_conditions?.condition === 'bear' ? 'error.main' : 'warning.main',
                      textTransform: 'capitalize',
                      fontWeight: 'bold'
                    }}>
                      {portfolioAnalysis.metadata?.market_conditions?.description || 'Analyzing...'}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} md={3}>
                    <Typography variant="caption" color="text.secondary">ANALYSIS PERIOD</Typography>
                    <Typography variant="h6" fontWeight="bold">
                      {portfolioAnalysis.strategies[0]?.metrics?.years_analyzed?.toFixed(1) || '13'} Years
                    </Typography>
                  </Grid>
                  <Grid item xs={12} md={3}>
                    <Typography variant="caption" color="text.secondary">DATA POINTS</Typography>
                    <Typography variant="h6" fontWeight="bold">
                      {portfolioAnalysis.strategies[0]?.portfolio_return?.length || '3,000+'} Days
                    </Typography>
                  </Grid>
                  <Grid item xs={12} md={3}>
                    <Typography variant="caption" color="text.secondary">TIMESTAMP</Typography>
                    <Typography variant="h6" fontWeight="bold">
                      {portfolioAnalysis.metadata?.timestamp ? 
                        new Date(portfolioAnalysis.metadata.timestamp).toLocaleDateString() : 'Today'
                      }
                    </Typography>
                  </Grid>
                </Grid>
              </Paper>

              {/* Portfolio Returns Chart */}
              <Paper elevation={0} sx={{ p: 3, borderRadius: 2 }}>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <ShowChart color="primary" />
                  Portfolio Returns Comparison
                </Typography>
                <Box sx={{ width: '100%', height: 400, mt: 2 }}>
                  <ResponsiveContainer>
                    <LineChart
                      data={prepareReturnChartData(portfolioAnalysis.strategies)}
                      margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
                      <XAxis 
                        dataKey="day" 
                        label={{ value: 'Time Period (Last 30 Days)', position: 'insideBottom', offset: -5 }}
                      />
                      <YAxis 
                        label={{ value: 'Returns (%)', angle: -90, position: 'insideLeft' }}
                      />
                      <ChartTooltip 
                        contentStyle={{
                          backgroundColor: 'rgba(0, 0, 0, 0.8)',
                          border: '1px solid rgba(255, 255, 255, 0.2)',
                          borderRadius: '8px',
                          padding: '10px'
                        }}
                        labelStyle={{ 
                          color: 'white',
                          fontWeight: 'bold',
                          marginBottom: '5px'
                        }}
                      />
                      <Legend />
                      <Line 
                        type="monotone" 
                        dataKey="Mean Variance Criterion" 
                        stroke="#2196f3" 
                        strokeWidth={3}
                        dot={false}
                        activeDot={{ r: 6 }}
                      />
                      <Line 
                        type="monotone" 
                        dataKey="Sharpe Ratio Criterion" 
                        stroke="#4caf50" 
                        strokeWidth={3}
                        dot={false}
                        activeDot={{ r: 6 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </Box>
              </Paper>

              {/* Strategy Metrics Comparison */}
              <Grid container spacing={3}>
                {portfolioAnalysis.strategies.map((strategy, index) => (
                  <Grid item xs={12} md={6} key={index}>
                    <StrategyCard>
                      <CardHeader
                        title={
                          <Stack direction="row" alignItems="center" spacing={2}>
                            <AutoGraph sx={{ color: index === 0 ? '#2196f3' : '#4caf50' }} />
                            <Typography variant="h6" fontWeight="bold">
                              {strategy.name}
                            </Typography>
                          </Stack>
                        }
                        sx={{ pb: 0 }}
                      />
                      <CardContent>
                        <Divider sx={{ mb: 3 }} />
                        
                        <Grid container spacing={2}>
                          <Grid item xs={6}>
                            <Typography variant="caption" color="text.secondary">
                              TOTAL RETURN (13 YEARS)
                            </Typography>
                            <Typography variant="h6" sx={{ 
                              color: strategy.metrics?.total_return > 0 ? 'success.main' : 'error.main',
                              fontWeight: 'bold'
                            }}>
                              {(strategy.metrics?.total_return * 100).toFixed(2)}%
                            </Typography>
                          </Grid>
                          <Grid item xs={6}>
                            <Typography variant="caption" color="text.secondary">
                              ANNUALIZED RETURN
                            </Typography>
                            <Typography variant="h6" sx={{ 
                              color: (strategy.metrics?.annualized_return || 
                                     (Math.pow(1 + strategy.metrics?.total_return, 1/strategy.metrics?.years_analyzed) - 1)) > 0 
                                     ? 'success.main' : 'error.main',
                              fontWeight: 'bold'
                            }}>
                              {strategy.metrics?.annualized_return ? 
                                `${(strategy.metrics.annualized_return * 100).toFixed(2)}%` :
                                `${((Math.pow(1 + strategy.metrics?.total_return, 1/strategy.metrics?.years_analyzed) - 1) * 100).toFixed(2)}%`
                              }
                            </Typography>
                          </Grid>
                          <Grid item xs={6}>
                            <Typography variant="caption" color="text.secondary">
                              AVG DAILY RETURN
                            </Typography>
                            <Typography variant="h6" fontWeight="bold">
                              {(strategy.metrics?.avg_daily_return * 100).toFixed(4)}%
                            </Typography>
                          </Grid>
                          <Grid item xs={6}>
                            <Typography variant="caption" color="text.secondary">
                              DAILY VOLATILITY
                            </Typography>
                            <Typography variant="h6" fontWeight="bold" color="warning.main">
                              {(strategy.metrics?.volatility * 100).toFixed(4)}%
                            </Typography>
                          </Grid>
                          <Grid item xs={6}>
                            <Typography variant="caption" color="text.secondary">
                              SHARPE RATIO (ANN.)
                            </Typography>
                            <Typography variant="h6" sx={{ 
                              color: strategy.metrics?.sharpe_ratio > 1 
                                ? 'success.main' 
                                : strategy.metrics?.sharpe_ratio > 0.5 
                                ? 'warning.main' 
                                : 'error.main',
                              fontWeight: 'bold'
                            }}>
                              {strategy.metrics?.sharpe_ratio?.toFixed(4)}
                            </Typography>
                          </Grid>
                          <Grid item xs={6}>
                            <Typography variant="caption" color="text.secondary">
                              ANALYSIS PERIOD
                            </Typography>
                            <Typography variant="h6" fontWeight="bold">
                              {strategy.metrics?.years_analyzed?.toFixed(1) || '13'} years
                            </Typography>
                          </Grid>
                        </Grid>

                        {/* Allocation Breakdown */}
                        <Box sx={{ mt: 3 }}>
                          <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                            ALLOCATION BREAKDOWN
                          </Typography>
                          {Object.entries(strategy.ticker_allocation || {})
                            .filter(([_, weight]) => weight > 0)
                            .sort(([,a], [,b]) => b - a)
                            .map(([ticker, weight]) => (
                              <Box key={ticker} sx={{ mb: 1 }}>
                                <Stack direction="row" justifyContent="space-between" alignItems="center">
                                  <Typography variant="body2" fontWeight="medium">{ticker}</Typography>
                                  <Typography variant="body2" fontWeight="bold">
                                    {(weight * 100).toFixed(2)}%
                                  </Typography>
                                </Stack>
                                <LinearProgress 
                                  variant="determinate" 
                                  value={weight * 100} 
                                  sx={{ 
                                    height: 6, 
                                    borderRadius: 3,
                                    backgroundColor: 'rgba(0,0,0,0.1)',
                                    '& .MuiLinearProgress-bar': {
                                      borderRadius: 3,
                                      background: index === 0 
                                        ? 'linear-gradient(90deg, #2196f3 0%, #64b5f6 100%)'
                                        : 'linear-gradient(90deg, #4caf50 0%, #81c784 100%)',
                                    }
                                  }}
                                />
                              </Box>
                            ))}
                        </Box>

                        {/* Performance Note */}
                        <Alert 
                          severity="info" 
                          icon={<TipsAndUpdates />}
                          sx={{ mt: 2, fontSize: '0.875rem' }}
                        >
                          Returns reflect historical performance from 2012-present, including major market cycles
                        </Alert>
                      </CardContent>
                    </StrategyCard>
                  </Grid>
                ))}
              </Grid>

              {/* Recommendations */}
              <Paper elevation={0} sx={{ 
                p: 3, 
                borderRadius: 2, 
                background: alpha(theme.palette.success.main, 0.05),
                border: `1px solid ${alpha(theme.palette.success.main, 0.2)}`
              }}>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <CheckCircle color="success" />
                  Algorithm Recommendation
                </Typography>
                <Typography variant="body1" sx={{ mb: 2 }}>
                  Based on risk-adjusted returns and current market conditions:
                </Typography>
                <Chip 
                  label={`Recommended: ${portfolioAnalysis.comparison?.best_performer || 'Mean Variance Criterion'}`}
                  sx={{ 
                    fontWeight: 'bold',
                    background: 'linear-gradient(45deg, #2196f3 30%, #4caf50 90%)',
                    color: 'white',
                    px: 2,
                    py: 0.5,
                    fontSize: '1rem'
                  }}
                />
                <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                  {portfolioAnalysis.comparison?.recommendation || 
                   'This strategy provides optimal risk-adjusted returns based on historical performance.'}
                </Typography>
              </Paper>
            </Stack>
          ) : (
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <Analytics sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
              <Typography variant="h6" color="text.secondary">
                No analysis data available
              </Typography>
            </Box>
          )}
        </DialogContent>
        
        <DialogActions sx={{ p: 3 }}>
          <Button
            variant="outlined"
            onClick={() => setMetricDetailsOpen(false)}
            sx={{ borderRadius: 2, textTransform: 'none' }}
          >
            Close
          </Button>
        </DialogActions>
      </Dialog>

      {/* Stock Detail Modal */}
      <Modal 
        open={stockModalOpen} 
        onClose={handleStockModalClose}
        aria-labelledby="stock-modal-title" 
        aria-describedby="stock-modal-description"
      >
        <Fade in={stockModalOpen}>
          <ModalBox>
            {selectedStock && (
              <>
                <Stack direction="row" justifyContent="space-between" alignItems="flex-start" mb={3}>
                  <Box>
                    <Typography variant="h5" component="h2" fontWeight="bold">
                      {selectedStock.name}
                    </Typography>
                    <Typography variant="subtitle1" color="primary" fontWeight="medium">
                      {selectedStock.ticker}
                    </Typography>
                  </Box>
                  <Stack direction="row" spacing={1}>
                    <Chip 
                      label="STOCK"
                      size="small"
                      sx={{ 
                        background: 'linear-gradient(45deg, #2196f3 30%, #64b5f6 90%)',
                        color: 'white',
                        fontWeight: 'bold'
                      }}
                    />
                    <IconButton 
                      onClick={handleStockModalClose}
                      size="small"
                      sx={{ 
                        color: 'text.secondary',
                        '&:hover': {
                          backgroundColor: alpha(theme.palette.error.main, 0.1),
                          color: 'error.main'
                        }
                      }}
                    >
                      <Close />
                    </IconButton>
                  </Stack>
                </Stack>
                
                <Divider sx={{ mb: 3 }} />
                
                <Typography variant="body1" sx={{ mb: 3, lineHeight: 1.8 }}>
                  {selectedStock.detail || `${selectedStock.name} is a publicly traded company listed under the ticker symbol ${selectedStock.ticker}. This stock represents ownership in the company and can be added to your investment portfolio for analysis and optimization.`}
                </Typography>
                
                <Box sx={{ 
                  p: 2, 
                  background: theme.palette.mode === 'dark'
                    ? 'rgba(255,255,255,0.05)'
                    : 'rgba(0,0,0,0.05)',
                  borderRadius: 2,
                  mb: 3
                }}>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="caption" color="text.secondary">
                        SYMBOL
                      </Typography>
                      <Typography variant="body2" fontWeight="bold">
                        {selectedStock.ticker}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="caption" color="text.secondary">
                        SECTOR
                      </Typography>
                      <Typography variant="body2" fontWeight="bold">
                        {selectedStock.sector || 'Technology'}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="caption" color="text.secondary">
                        EXCHANGE
                      </Typography>
                      <Typography variant="body2" fontWeight="bold">
                        {selectedStock.exchange || 'NASDAQ'}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="caption" color="text.secondary">
                        STATUS
                      </Typography>
                      <Typography variant="body2" fontWeight="bold" color="success.main">
                        Active
                      </Typography>
                    </Grid>
                  </Grid>
                </Box>
                
                {/* Current price info if available */}
                {stockPrices[selectedStock.ticker] && (
                  <Box sx={{ 
                    p: 2, 
                    background: alpha(theme.palette.primary.main, 0.05),
                    borderRadius: 2,
                    mb: 3,
                    border: `1px solid ${alpha(theme.palette.primary.main, 0.2)}`
                  }}>
                    <Typography variant="caption" color="text.secondary" gutterBottom display="block">
                      CURRENT MARKET DATA
                    </Typography>
                    <Grid container spacing={2}>
                      <Grid item xs={4}>
                        <Typography variant="h6" fontWeight="bold">
                          ${stockPrices[selectedStock.ticker].price?.toFixed(2)}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Current Price
                        </Typography>
                      </Grid>
                      <Grid item xs={4}>
                        <Typography 
                          variant="body2" 
                          fontWeight="bold"
                          color={stockPrices[selectedStock.ticker].change_percent >= 0 ? 'success.main' : 'error.main'}
                        >
                          {stockPrices[selectedStock.ticker].change_percent >= 0 ? '+' : ''}
                          {stockPrices[selectedStock.ticker].change_percent?.toFixed(2)}%
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Daily Change
                        </Typography>
                      </Grid>
                      <Grid item xs={4}>
                        <Typography variant="body2" fontWeight="bold">
                          Live
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Data Status
                        </Typography>
                      </Grid>
                    </Grid>
                  </Box>
                )}
                
                <Stack direction="row" spacing={2}>
                  <Button 
                    variant="contained" 
                    fullWidth
                    onClick={() => {
                      addToPortfolio(selectedStock);
                      handleStockModalClose();
                    }}
                    startIcon={<Add />}
                    sx={{ 
                      borderRadius: 2,
                      textTransform: 'none',
                      py: 1.5,
                      background: 'linear-gradient(45deg, #2196f3 30%, #64b5f6 90%)',
                      '&:hover': {
                        background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)',
                      }
                    }}
                  >
                    Add to Portfolio
                  </Button>
                  <Button 
                    variant="outlined" 
                    fullWidth
                    onClick={handleStockModalClose}
                    sx={{ 
                      borderRadius: 2,
                      textTransform: 'none',
                      py: 1.5,
                    }}
                  >
                    Cancel
                  </Button>
                </Stack>
              </>
            )}
          </ModalBox>
        </Fade>
      </Modal>
    </StyledContainer>
  );
};

export default Investment;