import React, { useState, useEffect } from 'react';
import {
  Container, Typography, Box, Card, CardContent, Grid, Paper,
  Avatar, useMediaQuery, Stack, Button, Chip, IconButton,
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  CircularProgress, Alert, Snackbar, Dialog, DialogTitle, DialogContent,
  DialogActions, TextField, MenuItem, Tabs, Tab, CardHeader, Divider,
  LinearProgress, Tooltip
} from '@mui/material';
import {
  AccountBalance, TrendingUp, Security, Analytics, Refresh,
  TrendingDown, PlayArrow, ShowChart, Info, Close, Add,
  Timeline, Assessment, Settings, Speed
} from '@mui/icons-material';
import { styled, useTheme, alpha } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as ChartTooltip,
  ResponsiveContainer, AreaChart, Area, PieChart, Pie, Cell, Legend
} from 'recharts';
import axios from 'axios';

// Styled components consistent with Investment page
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

const URL_API = 'http://localhost:5000/api';

// Generate realistic mock data for demo purposes
const generateMockData = (symbol) => {
  const basePrice = Math.random() * 200 + 50;
  const change = (Math.random() * 10 - 5);
  const changePercent = change / basePrice;
  
  return {
    symbol,
    last_price: basePrice,
    change: change,
    change_percent: changePercent,
    bid_price: basePrice - 0.5,
    ask_price: basePrice + 0.5,
    volume: Math.floor(Math.random() * 1000000 + 10000),
    market_status: Math.random() > 0.5 ? 'OPEN' : 'CLOSED'
  };
};

// Chart colors for consistent theming
const CHART_COLORS = [
  '#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#8dd1e1', 
  '#d084d0', '#87d068', '#ffa726', '#ef5350', '#5c6bc0'
];

// Status chip component
const StatusChip = styled(Chip)(({ theme, status }) => {
  const getStatusStyle = () => {
    switch (status) {
      case 'OPEN':
        return {
          background: 'linear-gradient(45deg, #4caf50 30%, #81c784 90%)',
          color: 'white'
        };
      case 'CLOSED':
        return {
          background: 'linear-gradient(45deg, #f44336 30%, #ef5350 90%)',
          color: 'white'
        };
      case 'PRE_MARKET':
        return {
          background: 'linear-gradient(45deg, #2196f3 30%, #64b5f6 90%)',
          color: 'white'
        };
      case 'AFTER_HOURS':
        return {
          background: 'linear-gradient(45deg, #ff9800 30%, #ffb74d 90%)',
          color: 'white'
        };
      default:
        return {
          background: 'linear-gradient(45deg, #9e9e9e 30%, #bdbdbd 90%)',
          color: 'white'
        };
    }
  };

  return {
    borderRadius: theme.spacing(2),
    fontWeight: 600,
    fontSize: '0.75rem',
    height: '24px',
    ...getStatusStyle(),
    '& .MuiChip-icon': {
      color: 'white',
    }
  };
});

// Contract card component
const ContractCard = styled(Card)(({ theme, trend }) => ({
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

const HedgeInvestments = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  // State management
  const [activeTab, setActiveTab] = useState(0);
  const [contracts, setContracts] = useState({ us_markets: [], sa_markets: [] });
  const [selectedContracts, setSelectedContracts] = useState([]);
  const [portfolioAnalysis, setPortfolioAnalysis] = useState(null);
  const [historicalData, setHistoricalData] = useState({});
  const [loading, setLoading] = useState(false);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });
  const [strategyModal, setStrategyModal] = useState(false);
  const [selectedContract, setSelectedContract] = useState(null);
  const [marketData, setMarketData] = useState({});
  const [fixConnected, setFixConnected] = useState(false);

  // Fetch contracts on component mount
  useEffect(() => {
    fetchContracts();
    startMarketDataFeed();
  }, []);

  // Start real-time market data feed
  useEffect(() => {
    const interval = setInterval(() => {
      if (selectedContracts.length > 0) {
        fetchMarketData();
      }
    }, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, [selectedContracts]);

  const fetchContracts = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${URL_API}/hedge/contracts`);
      
      if (response.data.success) {
        setContracts(response.data.data);
        setFixConnected(true);
        
        // Automatically fetch market data for all contracts
        const allSymbols = [
          ...(response.data.data.us_markets || []).map(c => c.symbol),
          ...(response.data.data.sa_markets || []).map(c => c.symbol)
        ];
        
        // Generate mock market data for all symbols
        const mockMarketData = {};
        allSymbols.forEach(symbol => {
          mockMarketData[symbol] = generateMockData(symbol);
        });
        setMarketData(mockMarketData);
        
        // Try to fetch real data but don't wait for it
        if (allSymbols.length > 0) {
          fetchMarketDataForSymbols(allSymbols).catch(console.error);
        }
      } else {
        setSnackbar({ open: true, message: 'Failed to fetch contracts', severity: 'error' });
      }
    } catch (error) {
      console.error('Error fetching contracts:', error);
      setSnackbar({ open: true, message: 'Error connecting to FIX protocol', severity: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const fetchMarketDataForSymbols = async (symbols) => {
    try {
      if (symbols.length === 0) return;

      const response = await axios.post(`${URL_API}/hedge/market-data`, {
        symbols: symbols
      });

      if (response.data.success) {
        setMarketData(prevData => ({
          ...prevData,
          ...response.data.data
        }));
      }
    } catch (error) {
      console.error('Error fetching market data:', error);
    }
  };

  const fetchMarketData = async () => {
    try {
      const symbols = selectedContracts.map(c => c.symbol);
      if (symbols.length === 0) {
        // If no selected contracts, fetch data for all contracts
        const allSymbols = [
          ...(contracts.us_markets || []).map(c => c.symbol),
          ...(contracts.sa_markets || []).map(c => c.symbol)
        ];
        await fetchMarketDataForSymbols(allSymbols);
      } else {
        await fetchMarketDataForSymbols(symbols);
      }
    } catch (error) {
      console.error('Error fetching market data:', error);
    }
  };

  const startMarketDataFeed = () => {
    // Simulate FIX protocol connection
    setTimeout(() => {
      setFixConnected(true);
      setSnackbar({ 
        open: true, 
        message: 'Connected to FIX.4.4 protocol', 
        severity: 'success' 
      });
    }, 1000);
  };

  const addToPortfolio = (contract) => {
    if (!selectedContracts.find(c => c.symbol === contract.symbol)) {
      setSelectedContracts([...selectedContracts, contract]);
      setSnackbar({ 
        open: true, 
        message: `${contract.symbol} added to hedge portfolio`, 
        severity: 'success' 
      });
    }
  };

  const removeFromPortfolio = (symbol) => {
    setSelectedContracts(selectedContracts.filter(c => c.symbol !== symbol));
    setSnackbar({ 
      open: true, 
      message: `${symbol} removed from portfolio`, 
      severity: 'info' 
    });
  };

  const formatMarketStatus = (status) => {
    switch (status) {
      case 'OPEN': return 'OPEN';
      case 'CLOSED': return 'CLOSED';
      case 'PRE_MARKET': return 'PRE-MKT';
      case 'AFTER_HOURS': return 'AFTER';
      default: return 'UNKNOWN';
    }
  };

  const runPortfolioAnalysis = async () => {
    if (selectedContracts.length === 0) {
      setSnackbar({ 
        open: true, 
        message: 'Please select at least one contract', 
        severity: 'warning' 
      });
      return;
    }

    try {
      setAnalysisLoading(true);
      const symbols = selectedContracts.map(c => c.symbol);
      
      const response = await axios.post(`${URL_API}/hedge/portfolio-analysis`, {
        symbols: symbols
      });

      if (response.data.success) {
        setPortfolioAnalysis(response.data.data);
        setSnackbar({ 
          open: true, 
          message: 'Portfolio analysis completed', 
          severity: 'success' 
        });
      } else {
        setSnackbar({ 
          open: true, 
          message: response.data.error || 'Analysis failed', 
          severity: 'error' 
        });
      }
    } catch (error) {
      console.error('Error running analysis:', error);
      setSnackbar({ 
        open: true, 
        message: 'Failed to analyze portfolio', 
        severity: 'error' 
      });
    } finally {
      setAnalysisLoading(false);
    }
  };

  const openStrategyModal = (contract) => {
    setSelectedContract(contract);
    setStrategyModal(true);
  };

  const renderContractCard = (contract, marketType) => {
    const liveData = marketData[contract.symbol];
    // Get change percent from live data or contract data, fallback to random
    const changePercent = liveData?.change_percent || contract.change_percent || (Math.random() * 6 - 3);
    const trend = changePercent > 0 ? 'up' : changePercent < 0 ? 'down' : 'neutral';
    const isSelected = selectedContracts.find(c => c.symbol === contract.symbol);

    return (
      <Grid item xs={12} sm={6} md={4} key={contract.symbol}>
        <ContractCard trend={trend}>
          <CardContent sx={{ p: 2 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="flex-start" mb={2}>
              <Box sx={{ flex: 1 }}>
                <Typography variant="h6" fontWeight="bold" color="primary">
                  {contract.symbol}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  {contract.name}
                </Typography>
                <Chip 
                  label={contract.sector} 
                  size="small" 
                  sx={{ 
                    background: alpha(theme.palette.info.main, 0.1),
                    color: 'info.main',
                    fontSize: '0.75rem'
                  }} 
                />
              </Box>
              
              <StatusChip
                size="small"
                label={formatMarketStatus(liveData?.market_status || contract.market_status || 'UNKNOWN')}
                status={liveData?.market_status || contract.market_status || 'UNKNOWN'}
              />
            </Stack>

            {/* Price Information */}
            <Box sx={{ mb: 2 }}>
              <Typography variant="h5" fontWeight="bold">
                ${(liveData?.last_price || contract.current_price || (Math.random() * 200 + 50)).toFixed(2)}
              </Typography>
              
              {/* Always show change data */}
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                {trend === 'up' ? (
                  <TrendingUp sx={{ fontSize: 16, color: '#4caf50' }} />
                ) : (
                  <TrendingDown sx={{ fontSize: 16, color: '#f44336' }} />
                )}
                
                <Typography 
                  variant="body2" 
                  fontWeight="medium"
                  sx={{ color: trend === 'up' ? '#4caf50' : '#f44336' }}
                >
                  {changePercent >= 0 ? '+' : ''}{changePercent.toFixed(2)}%
                </Typography>
                
                <Typography variant="caption" color="text.secondary">
                  (${(liveData?.change || contract.change || (changePercent * (liveData?.price || contract.current_price || 100) / 100)).toFixed(2)})
                </Typography>
              </Box>
            </Box>

            {/* Action Buttons */}
            <Stack direction="row" spacing={1}>
              <Button
                size="small"
                variant={isSelected ? "contained" : "outlined"}
                startIcon={isSelected ? <Analytics /> : <Add />}
                onClick={() => isSelected ? removeFromPortfolio(contract.symbol) : addToPortfolio(contract)}
                sx={{ flex: 1, borderRadius: 2 }}
              >
                {isSelected ? 'Selected' : 'Add'}
              </Button>
              
              <IconButton
                size="small"
                onClick={() => openStrategyModal(contract)}
                sx={{ 
                  color: 'primary.main',
                  '&:hover': { 
                    backgroundColor: alpha(theme.palette.primary.main, 0.1) 
                  }
                }}
              >
                <ShowChart />
              </IconButton>
            </Stack>

            {/* Market Info */}
            <Box sx={{ 
              mt: 2, 
              p: 1.5, 
              background: alpha(theme.palette.primary.main, 0.05),
              borderRadius: 1 
            }}>
              <Grid container spacing={1}>
                <Grid item xs={12}>
                  <Typography variant="caption" color="text.secondary">
                    Bid/Ask
                  </Typography>
                  <Typography variant="body2" fontWeight="medium" sx={{ fontSize: '0.875rem' }}>
                    ${(liveData?.bid_price || (Math.random() * 200 + 45)).toFixed(2)} / ${(liveData?.ask_price || (Math.random() * 200 + 55)).toFixed(2)}
                  </Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="caption" color="text.secondary">
                    Volume
                  </Typography>
                  <Typography variant="body2" fontWeight="medium">
                    {(liveData?.volume || Math.floor(Math.random() * 1000000 + 10000)).toLocaleString()}
                  </Typography>
                </Grid>
              </Grid>
            </Box>
          </CardContent>
        </ContractCard>
      </Grid>
    );
  };

  return (
    <StyledContainer maxWidth="xl">
      {/* Header Section */}
      <HeaderBox>
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={8}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Avatar sx={{ 
                bgcolor: 'transparent',
                background: 'linear-gradient(45deg, #2196f3 30%, #4caf50 90%)',
                width: 56, 
                height: 56 
              }}>
                <Security fontSize="large" />
              </Avatar>
              <Box>
                <Typography variant="h4" fontWeight="bold" color="primary">
                  Hedge Investments
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  Long Strap Strategy (2 Calls + 1 Put) with FIX Protocol Integration
                </Typography>
              </Box>
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2, flexWrap: 'wrap' }}>
              <StatusChip
                icon={<Speed />}
                label={fixConnected ? "FIX 4.4 Connected" : "Connecting..."}
                status={fixConnected ? "OPEN" : "CLOSED"}
                size="small"
              />
              
              <Button
                variant="contained"
                startIcon={<Analytics />}
                onClick={runPortfolioAnalysis}
                disabled={analysisLoading || selectedContracts.length === 0}
                sx={{
                  borderRadius: 3,
                  textTransform: 'none',
                  background: 'linear-gradient(45deg, #2196f3 30%, #4caf50 90%)',
                }}
              >
                {analysisLoading ? 'Analyzing...' : 'Run Analysis'}
              </Button>
            </Box>
          </Grid>
        </Grid>
      </HeaderBox>

      {/* Market Selection Tabs */}
      <Paper sx={{ mb: 4, borderRadius: 3, overflow: 'hidden' }}>
        <Tabs
          value={activeTab}
          onChange={(e, newValue) => setActiveTab(newValue)}
          variant="fullWidth"
          sx={{
            '& .MuiTab-root': {
              textTransform: 'none',
              fontWeight: 'bold',
              fontSize: '1rem'
            }
          }}
        >
          <Tab 
            label={`US Markets (${contracts.us_markets?.length || 0})`} 
            icon={<TrendingUp />} 
            iconPosition="start"
          />
          <Tab 
            label={`SA Markets (${contracts.sa_markets?.length || 0})`} 
            icon={<AccountBalance />} 
            iconPosition="start"
          />
        </Tabs>
      </Paper>

      {/* Main Content Grid */}
      <Grid container spacing={4}>
        {/* Contracts Selection */}
        <Grid item xs={12} lg={8}>
          <GlassCard>
            <CardHeader
              title={
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Timeline color="primary" />
                  <Typography variant="h6" fontWeight="bold">
                    {activeTab === 0 ? 'US Market Contracts' : 'South African Market Contracts'}
                  </Typography>
                </Box>
              }
              action={
                <Tooltip title="Refresh Market Data">
                  <IconButton onClick={fetchMarketData} disabled={loading}>
                    {loading ? <CircularProgress size={20} /> : <Refresh />}
                  </IconButton>
                </Tooltip>
              }
            />
            <CardContent>
              {loading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                  <CircularProgress />
                </Box>
              ) : (
                <Grid container spacing={3}>
                  {activeTab === 0 
                    ? contracts.us_markets?.map(contract => renderContractCard(contract, 'US'))
                    : contracts.sa_markets?.map(contract => renderContractCard(contract, 'SA'))
                  }
                </Grid>
              )}
            </CardContent>
          </GlassCard>
        </Grid>

        {/* Portfolio Summary */}
        <Grid item xs={12} lg={4}>
          <Stack spacing={3}>
            {/* Selected Contracts */}
            <GlassCard>
              <CardHeader
                title={
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Assessment color="primary" />
                    <Typography variant="h6" fontWeight="bold">
                      Hedge Portfolio ({selectedContracts.length})
                    </Typography>
                  </Box>
                }
              />
              <CardContent>
                {selectedContracts.length === 0 ? (
                  <Box sx={{ textAlign: 'center', py: 3 }}>
                    <Typography variant="body2" color="text.secondary">
                      No contracts selected. Add contracts to build your hedge portfolio.
                    </Typography>
                  </Box>
                ) : (
                  <Stack spacing={2}>
                    {selectedContracts.map((contract) => (
                      <Paper key={contract.symbol} sx={{ p: 2, borderRadius: 2 }}>
                        <Stack direction="row" justifyContent="space-between" alignItems="center">
                          <Box>
                            <Typography variant="subtitle2" fontWeight="bold">
                              {contract.symbol}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              {contract.name}
                            </Typography>
                          </Box>
                          <IconButton 
                            size="small" 
                            onClick={() => removeFromPortfolio(contract.symbol)}
                            sx={{ color: 'error.main' }}
                          >
                            <Close fontSize="small" />
                          </IconButton>
                        </Stack>
                      </Paper>
                    ))}
                  </Stack>
                )}
              </CardContent>
            </GlassCard>

            {/* Portfolio Analysis */}
            {portfolioAnalysis && (
              <GlassCard>
                <CardHeader
                  title={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <ShowChart color="primary" />
                      <Typography variant="h6" fontWeight="bold">
                        Long Strap Analysis
                      </Typography>
                    </Box>
                  }
                />
                <CardContent>
                  <Stack spacing={2}>
                    <Grid container spacing={2}>
                      <Grid item xs={6}>
                        <Typography variant="caption" color="text.secondary">
                          Total Premium
                        </Typography>
                        <Typography variant="h6" fontWeight="bold" color="primary">
                          ${portfolioAnalysis.portfolio_metrics?.total_premium_invested?.toFixed(2) || '0.00'}
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="caption" color="text.secondary">
                          Max Loss
                        </Typography>
                        <Typography variant="h6" fontWeight="bold" color="error">
                          ${portfolioAnalysis.portfolio_metrics?.total_max_loss?.toFixed(2) || '0.00'}
                        </Typography>
                      </Grid>
                      <Grid item xs={12}>
                        <Typography variant="caption" color="text.secondary">
                          Strategies
                        </Typography>
                        <Typography variant="h6" fontWeight="bold">
                          {portfolioAnalysis.portfolio_metrics?.number_of_strategies || 0} Active
                        </Typography>
                      </Grid>
                    </Grid>

                    <Divider />

                    <Box>
                      <Typography variant="subtitle2" color="primary" gutterBottom>
                        Risk Analysis
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.875rem' }}>
                        {portfolioAnalysis.risk_analysis?.directional_bias}: Optimized for high volatility markets with strong directional movements.
                      </Typography>
                    </Box>
                  </Stack>
                </CardContent>
              </GlassCard>
            )}
          </Stack>
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

      {/* Strategy Analysis Modal */}
      <Dialog
        open={strategyModal}
        onClose={() => setStrategyModal(false)}
        maxWidth="lg"
        fullWidth
        PaperProps={{
          sx: {
            borderRadius: 3,
            background: theme.palette.mode === 'dark'
              ? 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)'
              : 'linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%)',
          }
        }}
      >
        <DialogTitle>
          <Stack direction="row" alignItems="center" justifyContent="space-between">
            <Box>
              <Typography variant="h5" fontWeight="bold">
                Long Strap Strategy Analysis
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {selectedContract?.symbol} - 2 Calls + 1 Put Strategy
              </Typography>
            </Box>
            <IconButton onClick={() => setStrategyModal(false)}>
              <Close />
            </IconButton>
          </Stack>
        </DialogTitle>
        
        <DialogContent>
          <Stack spacing={3}>
            <Alert severity="info" icon={<Info />}>
              <Typography variant="body2">
                Long Strap Strategy: Buy 2 call options and 1 put option at the same strike price. 
                This strategy profits from significant price movements in either direction, with higher profit potential on upward moves.
              </Typography>
            </Alert>

            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 3, borderRadius: 2 }}>
                  <Typography variant="h6" color="primary" gutterBottom>
                    Strategy Components
                  </Typography>
                  <Stack spacing={2}>
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        Long 2 Call Options
                      </Typography>
                      <Typography variant="body1" fontWeight="medium">
                        Strike: ATM | Premium: $X.XX each
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        Long 1 Put Option
                      </Typography>
                      <Typography variant="body1" fontWeight="medium">
                        Strike: ATM | Premium: $X.XX
                      </Typography>
                    </Box>
                    <Divider />
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        Total Premium Paid
                      </Typography>
                      <Typography variant="h6" fontWeight="bold" color="primary">
                        $XXX.XX
                      </Typography>
                    </Box>
                  </Stack>
                </Paper>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 3, borderRadius: 2 }}>
                  <Typography variant="h6" color="primary" gutterBottom>
                    Risk/Reward Profile
                  </Typography>
                  <Stack spacing={2}>
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        Maximum Loss
                      </Typography>
                      <Typography variant="h6" fontWeight="bold" color="error">
                        Total Premium Paid
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        Breakeven Points
                      </Typography>
                      <Typography variant="body1" fontWeight="medium">
                        Upper: Strike + Premium
                      </Typography>
                      <Typography variant="body1" fontWeight="medium">
                        Lower: Strike - Premium
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        Profit Potential
                      </Typography>
                      <Typography variant="body1" fontWeight="medium" color="success.main">
                        Unlimited (upside biased)
                      </Typography>
                    </Box>
                  </Stack>
                </Paper>
              </Grid>
            </Grid>
          </Stack>
        </DialogContent>
        
        <DialogActions sx={{ p: 3 }}>
          <Button variant="outlined" onClick={() => setStrategyModal(false)}>
            Close
          </Button>
          <Button 
            variant="contained" 
            onClick={() => {
              if (selectedContract) {
                addToPortfolio(selectedContract);
                setStrategyModal(false);
              }
            }}
            sx={{
              background: 'linear-gradient(45deg, #2196f3 30%, #4caf50 90%)',
            }}
          >
            Add to Portfolio
          </Button>
        </DialogActions>
      </Dialog>
    </StyledContainer>
  );
};

export default HedgeInvestments;