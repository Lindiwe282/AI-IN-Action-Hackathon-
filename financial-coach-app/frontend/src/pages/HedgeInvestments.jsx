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
  Timeline, Assessment, Settings, Speed, CheckCircle, Error
} from '@mui/icons-material';
import { styled, useTheme, alpha } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as ChartTooltip,
  ResponsiveContainer, AreaChart, Area, PieChart, Pie, Cell, Legend
} from 'recharts';
import axios from 'axios';

const URL_API = 'http://localhost:5000/api';

// Currency formatting utility
const formatCurrency = (amount, currency = 'USD', symbol = null) => {
  const currencySymbols = {
    'USD': '$',
    'ZAR': 'R'
  };
  
  // If symbol is provided (e.g., from contract), override currency for South African markets
  if (symbol && symbol.endsWith('.JO')) {
    return `R${amount.toFixed(2)}`;
  }
  
  const currencySymbol = currencySymbols[currency] || '$';
  return `${currencySymbol}${amount.toFixed(2)}`;
};

// Generate realistic mock data for demo purposes
const generateMockData = (symbol) => {
  const basePrice = Math.random() * 200 + 50;
  const change = (Math.random() * 10 - 5);
  const changePercent = change / basePrice;
  
  // Determine currency based on symbol (South African stocks end with .JO)
  const currency = symbol.endsWith('.JO') ? 'ZAR' : 'USD';
  
  return {
    symbol,
    last_price: basePrice,
    change: change,
    change_percent: changePercent,
    bid_price: basePrice - 0.5,
    ask_price: basePrice + 0.5,
    volume: Math.floor(Math.random() * 1000000 + 10000),
    market_status: Math.random() > 0.5 ? 'OPEN' : 'CLOSED',
    currency: currency
  };
};

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

const StatusChip = styled(Chip)(({ theme, status }) => ({
  borderRadius: theme.spacing(2),
  fontWeight: 600,
  background: status === 'connected' || status === 'OPEN'
    ? 'linear-gradient(45deg, #4caf50 30%, #81c784 90%)'
    : status === 'running'
    ? 'linear-gradient(45deg, #2196f3 30%, #64b5f6 90%)'
    : 'linear-gradient(45deg, #f44336 30%, #ef5350 90%)',
  color: 'white',
  '& .MuiChip-icon': {
    color: 'white',
  }
}));

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
  const [contracts, setContracts] = useState({ us_markets: [], sa_markets: [] });
  const [selectedContracts, setSelectedContracts] = useState([]);
  const [marketData, setMarketData] = useState({});
  const [loading, setLoading] = useState(false);
  const [fixConnected, setFixConnected] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });
  const [currentTab, setCurrentTab] = useState(0);
  const [portfolioAnalysis, setPortfolioAnalysis] = useState(null);
  
  // Dialog state
  const [contractDialog, setContractDialog] = useState({ open: false, contract: null });
  const [optionsData, setOptionsData] = useState(null);
  const [loadingOptions, setLoadingOptions] = useState(false);
  const [analysisDialog, setAnalysisDialog] = useState({ open: false, analysis: null });
  const [loadingAnalysis, setLoadingAnalysis] = useState(false);

  // Initialize and fetch data
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

      const response = await axios.post(`${URL_API}/hedge/fix-market-data`, {
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

  // Dialog handlers
  const handleContractClick = async (contract) => {
    setContractDialog({ open: true, contract });
    setLoadingOptions(true);
    
    try {
      const response = await axios.post(`${URL_API}/hedge/options-chain`, {
        symbol: contract.symbol
      });
      
      if (response.data.success) {
        setOptionsData(response.data.data);
      } else {
        setSnackbar({ open: true, message: 'Failed to load options data', severity: 'error' });
      }
    } catch (error) {
      console.error('Error fetching options data:', error);
      setSnackbar({ open: true, message: 'Error loading options data', severity: 'error' });
    } finally {
      setLoadingOptions(false);
    }
  };

  const handleAnalysisClick = async () => {
    if (selectedContracts.length === 0) {
      setSnackbar({ open: true, message: 'Please select contracts for analysis', severity: 'warning' });
      return;
    }

    setLoadingAnalysis(true);
    
    try {
      const symbols = selectedContracts.map(c => c.symbol);
      const response = await axios.post(`${URL_API}/hedge/portfolio-analysis`, {
        symbols: symbols
      });
      
      if (response.data.success) {
        setAnalysisDialog({ open: true, analysis: response.data.data });
      } else {
        setSnackbar({ open: true, message: 'Failed to analyze portfolio', severity: 'error' });
      }
    } catch (error) {
      console.error('Error analyzing portfolio:', error);
      setSnackbar({ open: true, message: 'Error analyzing portfolio', severity: 'error' });
    } finally {
      setLoadingAnalysis(false);
    }
  };

  const closeContractDialog = () => {
    setContractDialog({ open: false, contract: null });
    setOptionsData(null);
  };

  const closeAnalysisDialog = () => {
    setAnalysisDialog({ open: false, analysis: null });
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
      setSnackbar({ open: true, message: `${contract.symbol} added to portfolio`, severity: 'success' });
    }
  };

  const removeFromPortfolio = (symbol) => {
    setSelectedContracts(selectedContracts.filter(c => c.symbol !== symbol));
    setSnackbar({ open: true, message: `${symbol} removed from portfolio`, severity: 'info' });
  };

  const formatMarketStatus = (status) => {
    switch (status?.toUpperCase()) {
      case 'OPEN': return 'OPEN';
      case 'CLOSED': return 'CLOSED';
      case 'PRE_MARKET': return 'PRE-MKT';
      case 'AFTER_HOURS': return 'AFTER-HRS';
      default: return 'LIVE';
    }
  };

  const renderContractCard = (contract, marketType) => {
    const changePercent = contract.change_percent || (Math.random() * 6 - 3);
    const trend = changePercent > 0 ? 'up' : changePercent < 0 ? 'down' : 'neutral';
    const liveData = marketData[contract.symbol];
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
                label={formatMarketStatus(liveData?.market_status || contract.market_status)}
                status={liveData?.market_status || contract.market_status || 'UNKNOWN'}
              />
            </Stack>

            {/* Price Information */}
            <Box sx={{ mb: 2 }}>
              <Typography variant="h5" fontWeight="bold">
                {formatCurrency(
                  liveData?.last_price || contract.current_price || (Math.random() * 200 + 50),
                  contract.currency || (liveData?.currency) || 'USD',
                  contract.symbol
                )}
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
                  {trend === 'up' ? '+' : ''}{(
                    liveData?.change_percent || contract.change_percent || (Math.random() * 6 - 3)
                  ).toFixed(2)}%
                </Typography>
                
                <Typography variant="caption" color="text.secondary">
                  ({formatCurrency(
                    liveData?.change || contract.change || (Math.random() * 10 - 5),
                    contract.currency || (liveData?.currency) || 'USD',
                    contract.symbol
                  )})
                </Typography>
              </Box>
            </Box>

            {/* Action Buttons */}
            <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
              <Button
                size="small"
                variant={isSelected ? "contained" : "outlined"}
                startIcon={isSelected ? <Analytics /> : <Add />}
                onClick={() => isSelected ? removeFromPortfolio(contract.symbol) : addToPortfolio(contract)}
                sx={{ flex: 1, borderRadius: 2 }}
              >
                {isSelected ? 'Selected' : 'Add'}
              </Button>
              <Button
                size="small"
                variant="outlined"
                startIcon={<ShowChart />}
                onClick={() => handleContractClick(contract)}
                sx={{ borderRadius: 2, minWidth: 'auto' }}
              >
                Options
              </Button>
            </Stack>

            {/* Market Info */}
            <Box sx={{ 
              mt: 2, 
              p: 1.5, 
              background: alpha(theme.palette.primary.main, 0.05),
              borderRadius: 1 
            }}>
              <Grid container spacing={1}>
                <Grid item xs={6}>
                  <Typography variant="caption" color="text.secondary">
                    Bid/Ask
                  </Typography>
                  <Typography variant="body2" fontWeight="medium" sx={{ fontSize: '0.75rem' }}>
                    {formatCurrency(
                      liveData?.bid_price || (Math.random() * 200 + 45),
                      contract.currency || (liveData?.currency) || 'USD',
                      contract.symbol
                    )}/{formatCurrency(
                      liveData?.ask_price || (Math.random() * 200 + 55),
                      contract.currency || (liveData?.currency) || 'USD',
                      contract.symbol
                    )}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="caption" color="text.secondary">
                    Volume
                  </Typography>
                  <Typography variant="body2" fontWeight="medium" sx={{ fontSize: '0.75rem' }}>
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
                  FIX Protocol 4.4 - Long Strap Options Strategy (2 Calls + 1 Put)
                </Typography>
              </Box>
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2, alignItems: 'center' }}>
              <Button
                variant="contained"
                startIcon={loadingAnalysis ? <CircularProgress size={16} /> : <Analytics />}
                onClick={handleAnalysisClick}
                disabled={loadingAnalysis || selectedContracts.length === 0}
                sx={{
                  background: 'linear-gradient(45deg, #4caf50 30%, #81c784 90%)',
                  borderRadius: 2,
                  textTransform: 'none',
                  fontWeight: 600
                }}
              >
                {loadingAnalysis ? 'Analyzing...' : `Analyze Portfolio (${selectedContracts.length})`}
              </Button>
              <StatusChip
                icon={fixConnected ? <CheckCircle /> : <Error />}
                label={fixConnected ? "FIX Connected" : "Connecting..."}
                status={fixConnected ? "connected" : "error"}
              />
              <IconButton onClick={fetchMarketData} disabled={loading}>
                {loading ? <CircularProgress size={20} /> : <Refresh />}
              </IconButton>
            </Box>
          </Grid>
        </Grid>
      </HeaderBox>

      {/* Main Content */}
      <Grid container spacing={4}>
        {/* Market Selection Tabs */}
        <Grid item xs={12}>
          <GlassCard>
            <CardHeader
              title={
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Timeline color="primary" />
                  <Typography variant="h6" fontWeight="bold">
                    Options Contracts - Live Market Data
                  </Typography>
                </Box>
              }
            />
            <CardContent>
              <Tabs 
                value={currentTab} 
                onChange={(e, newValue) => setCurrentTab(newValue)}
                sx={{ mb: 3 }}
              >
                <Tab 
                  label={`US Markets (${contracts.us_markets?.length || 0})`}
                  icon={<ShowChart />}
                />
                <Tab 
                  label={`SA Markets (${contracts.sa_markets?.length || 0})`}
                  icon={<Assessment />}
                />
              </Tabs>

              {loading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                  <CircularProgress />
                </Box>
              ) : (
                <Grid container spacing={3}>
                  {currentTab === 0
                    ? contracts.us_markets?.map(contract => renderContractCard(contract, 'US'))
                    : contracts.sa_markets?.map(contract => renderContractCard(contract, 'SA'))
                  }
                </Grid>
              )}
            </CardContent>
          </GlassCard>
        </Grid>

        {/* Strategy Information */}
        <Grid item xs={12} md={6}>
          <GlassCard>
            <CardHeader
              title={
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Security color="primary" />
                  <Typography variant="h6" fontWeight="bold">
                    Long Strap Strategy
                  </Typography>
                </Box>
              }
            />
            <CardContent>
              <Typography variant="body1" paragraph>
                Long Strap Strategy: Buy 2 call options and 1 put option at the same strike price. 
                This strategy profits from significant price movements in either direction, with higher profit potential on upward moves.
              </Typography>
              
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" gutterBottom>Key Features:</Typography>
                <Stack spacing={1}>
                  <Typography variant="body2">• Bullish bias with unlimited upside potential</Typography>
                  <Typography variant="body2">• Limited downside profit potential</Typography>
                  <Typography variant="body2">• Time decay risk (Theta negative)</Typography>
                  <Typography variant="body2">• High volatility sensitivity (Vega positive)</Typography>
                </Stack>
              </Box>
            </CardContent>
          </GlassCard>
        </Grid>

        {/* Selected Portfolio */}
        <Grid item xs={12} md={6}>
          <GlassCard>
            <CardHeader
              title={
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Analytics color="primary" />
                  <Typography variant="h6" fontWeight="bold">
                    Selected Portfolio ({selectedContracts.length})
                  </Typography>
                </Box>
              }
            />
            <CardContent>
              {selectedContracts.length === 0 ? (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <Typography variant="body1" color="text.secondary">
                    No contracts selected. Add contracts from the markets above to start building your hedge portfolio.
                  </Typography>
                </Box>
              ) : (
                <Stack spacing={2}>
                  {selectedContracts.map(contract => (
                    <Box 
                      key={contract.symbol}
                      sx={{ 
                        p: 2, 
                        borderRadius: 2, 
                        border: '1px solid',
                        borderColor: 'divider',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center'
                      }}
                    >
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
                    </Box>
                  ))}
                </Stack>
              )}
            </CardContent>
          </GlassCard>
        </Grid>
      </Grid>

      {/* Contract Options Dialog */}
      <Dialog
        open={contractDialog.open}
        onClose={closeContractDialog}
        maxWidth="lg"
        fullWidth
        PaperProps={{
          sx: {
            borderRadius: 3,
            background: theme.palette.mode === 'dark'
              ? 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)'
              : 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)',
          }
        }}
      >
        <DialogTitle sx={{ pb: 1 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Avatar sx={{ bgcolor: 'primary.main' }}>
                <ShowChart />
              </Avatar>
              <Box>
                <Typography variant="h5" fontWeight="bold">
                  {contractDialog.contract?.symbol} Options Chain
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Real-time options data with premiums for calls and puts
                </Typography>
              </Box>
            </Box>
            <IconButton onClick={closeContractDialog}>
              <Close />
            </IconButton>
          </Box>
        </DialogTitle>
        
        <DialogContent>
          {loadingOptions ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
              <CircularProgress />
            </Box>
          ) : optionsData ? (
            <Grid container spacing={3}>
              {/* Current Stock Price */}
              <Grid item xs={12}>
                <GlassCard>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>Current Stock Price</Typography>
                    <Typography variant="h4" color="primary" fontWeight="bold">
                      {optionsData.current_price ? formatCurrency(optionsData.current_price, optionsData.currency || 'USD', optionsData.symbol) : 'N/A'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Last updated: {new Date(optionsData.timestamp || Date.now()).toLocaleTimeString()}
                    </Typography>
                  </CardContent>
                </GlassCard>
              </Grid>

              {/* Calls Options */}
              <Grid item xs={12} md={6}>
                <GlassCard>
                  <CardHeader
                    title={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <TrendingUp color="success" />
                        <Typography variant="h6" fontWeight="bold">Call Options</Typography>
                      </Box>
                    }
                  />
                  <CardContent>
                    <TableContainer>
                      <Table size="small">
                        <TableHead>
                          <TableRow>
                            <TableCell>Strike</TableCell>
                            <TableCell>Premium</TableCell>
                            <TableCell>IV</TableCell>
                            <TableCell>Delta</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {optionsData.calls?.map((option, index) => (
                            <TableRow key={index}>
                              <TableCell>{formatCurrency(option.strike, optionsData.currency || 'USD', optionsData.symbol)}</TableCell>
                              <TableCell>{formatCurrency(option.premium, optionsData.currency || 'USD', optionsData.symbol)}</TableCell>
                              <TableCell>{(option.implied_volatility * 100).toFixed(1)}%</TableCell>
                              <TableCell>{option.delta.toFixed(3)}</TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
                  </CardContent>
                </GlassCard>
              </Grid>

              {/* Puts Options */}
              <Grid item xs={12} md={6}>
                <GlassCard>
                  <CardHeader
                    title={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <TrendingDown color="error" />
                        <Typography variant="h6" fontWeight="bold">Put Options</Typography>
                      </Box>
                    }
                  />
                  <CardContent>
                    <TableContainer>
                      <Table size="small">
                        <TableHead>
                          <TableRow>
                            <TableCell>Strike</TableCell>
                            <TableCell>Premium</TableCell>
                            <TableCell>IV</TableCell>
                            <TableCell>Delta</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {optionsData.puts?.map((option, index) => (
                            <TableRow key={index}>
                              <TableCell>{formatCurrency(option.strike, optionsData.currency || 'USD', optionsData.symbol)}</TableCell>
                              <TableCell>{formatCurrency(option.premium, optionsData.currency || 'USD', optionsData.symbol)}</TableCell>
                              <TableCell>{(option.implied_volatility * 100).toFixed(1)}%</TableCell>
                              <TableCell>{option.delta.toFixed(3)}</TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
                  </CardContent>
                </GlassCard>
              </Grid>

              {/* Long Strap Strategy Info */}
              <Grid item xs={12}>
                <GlassCard>
                  <CardHeader
                    title={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Analytics color="primary" />
                        <Typography variant="h6" fontWeight="bold">Long Strap Strategy</Typography>
                      </Box>
                    }
                  />
                  <CardContent>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      Strategy: Buy 2 Call Options + 1 Put Option at the same strike price
                    </Typography>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={4}>
                        <Box sx={{ textAlign: 'center', p: 2, bgcolor: 'success.main', color: 'success.contrastText', borderRadius: 2 }}>
                          <Typography variant="h6" fontWeight="bold">2 Calls</Typography>
                          <Typography variant="body2">Long Position</Typography>
                        </Box>
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Box sx={{ textAlign: 'center', p: 2, bgcolor: 'error.main', color: 'error.contrastText', borderRadius: 2 }}>
                          <Typography variant="h6" fontWeight="bold">1 Put</Typography>
                          <Typography variant="body2">Long Position</Typography>
                        </Box>
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Box sx={{ textAlign: 'center', p: 2, bgcolor: 'info.main', color: 'info.contrastText', borderRadius: 2 }}>
                          <Typography variant="h6" fontWeight="bold">Bullish</Typography>
                          <Typography variant="body2">Market Outlook</Typography>
                        </Box>
                      </Grid>
                    </Grid>
                  </CardContent>
                </GlassCard>
              </Grid>
            </Grid>
          ) : (
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <Typography variant="body1" color="text.secondary">
                No options data available
              </Typography>
            </Box>
          )}
        </DialogContent>
      </Dialog>

      {/* Portfolio Analysis Dialog */}
      <Dialog
        open={analysisDialog.open}
        onClose={closeAnalysisDialog}
        maxWidth="xl"
        fullWidth
        PaperProps={{
          sx: {
            borderRadius: 3,
            background: theme.palette.mode === 'dark'
              ? 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)'
              : 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)',
            minHeight: '70vh',
          }
        }}
      >
        <DialogTitle sx={{ pb: 1 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Avatar sx={{ bgcolor: 'primary.main' }}>
                <Analytics />
              </Avatar>
              <Box>
                <Typography variant="h5" fontWeight="bold">
                  Portfolio Performance Analysis
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Long Strap Strategy Performance, Risk Metrics & Returns
                </Typography>
              </Box>
            </Box>
            <IconButton onClick={closeAnalysisDialog}>
              <Close />
            </IconButton>
          </Box>
        </DialogTitle>
        
        <DialogContent>
          {analysisDialog.analysis ? (
            <Grid container spacing={3}>
              {/* Performance Summary */}
              <Grid item xs={12} md={4}>
                <GlassCard>
                  <CardHeader title="Performance Summary" />
                  <CardContent>
                    <Stack spacing={2}>
                      <Box>
                        <Typography variant="body2" color="text.secondary">Total Return</Typography>
                        <Typography variant="h5" color={analysisDialog.analysis.total_return >= 0 ? 'success.main' : 'error.main'} fontWeight="bold">
                          {analysisDialog.analysis.total_return >= 0 ? '+' : ''}{analysisDialog.analysis.total_return?.toFixed(2)}%
                        </Typography>
                      </Box>
                      <Box>
                        <Typography variant="body2" color="text.secondary">Annualized Return</Typography>
                        <Typography variant="h6" color={analysisDialog.analysis.annualized_return >= 0 ? 'success.main' : 'error.main'} fontWeight="bold">
                          {analysisDialog.analysis.annualized_return >= 0 ? '+' : ''}{analysisDialog.analysis.annualized_return?.toFixed(2)}%
                        </Typography>
                      </Box>
                      <Box>
                        <Typography variant="body2" color="text.secondary">Win Rate</Typography>
                        <Typography variant="h6" fontWeight="bold">
                          {analysisDialog.analysis.win_rate?.toFixed(1)}%
                        </Typography>
                      </Box>
                    </Stack>
                  </CardContent>
                </GlassCard>
              </Grid>

              {/* Risk Metrics */}
              <Grid item xs={12} md={4}>
                <GlassCard>
                  <CardHeader title="Risk Metrics" />
                  <CardContent>
                    <Stack spacing={2}>
                      <Box>
                        <Typography variant="body2" color="text.secondary">Sharpe Ratio</Typography>
                        <Typography variant="h5" color={analysisDialog.analysis.sharpe_ratio >= 1 ? 'success.main' : analysisDialog.analysis.sharpe_ratio >= 0.5 ? 'warning.main' : 'error.main'} fontWeight="bold">
                          {analysisDialog.analysis.sharpe_ratio?.toFixed(3)}
                        </Typography>
                      </Box>
                      <Box>
                        <Typography variant="body2" color="text.secondary">Volatility</Typography>
                        <Typography variant="h6" fontWeight="bold">
                          {analysisDialog.analysis.volatility?.toFixed(2)}%
                        </Typography>
                      </Box>
                      <Box>
                        <Typography variant="body2" color="text.secondary">Max Drawdown</Typography>
                        <Typography variant="h6" color="error.main" fontWeight="bold">
                          {analysisDialog.analysis.max_drawdown?.toFixed(2)}%
                        </Typography>
                      </Box>
                    </Stack>
                  </CardContent>
                </GlassCard>
              </Grid>

              {/* Strategy Info */}
              <Grid item xs={12} md={4}>
                <GlassCard>
                  <CardHeader title="Strategy Details" />
                  <CardContent>
                    <Stack spacing={2}>
                      <Box>
                        <Typography variant="body2" color="text.secondary">Strategy Type</Typography>
                        <Typography variant="h6" fontWeight="bold">Long Strap</Typography>
                      </Box>
                      <Box>
                        <Typography variant="body2" color="text.secondary">Positions</Typography>
                        <Typography variant="body1">2 Calls + 1 Put</Typography>
                      </Box>
                      <Box>
                        <Typography variant="body2" color="text.secondary">Market Outlook</Typography>
                        <Chip label="Bullish" color="success" size="small" />
                      </Box>
                      <Box>
                        <Typography variant="body2" color="text.secondary">Contracts</Typography>
                        <Typography variant="body1">{selectedContracts.length} Assets</Typography>
                      </Box>
                    </Stack>
                  </CardContent>
                </GlassCard>
              </Grid>

              {/* Individual Contract Performance */}
              <Grid item xs={12}>
                <GlassCard>
                  <CardHeader title="Individual Contract Performance" />
                  <CardContent>
                    <TableContainer>
                      <Table>
                        <TableHead>
                          <TableRow>
                            <TableCell>Symbol</TableCell>
                            <TableCell>Current Price</TableCell>
                            <TableCell>Return</TableCell>
                            <TableCell>Risk Level</TableCell>
                            <TableCell>Sharpe Ratio</TableCell>
                            <TableCell>Contribution</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {analysisDialog.analysis.contracts?.map((contract, index) => (
                            <TableRow key={index}>
                              <TableCell>
                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                  <strong>{contract.symbol}</strong>
                                </Box>
                              </TableCell>
                              <TableCell>{formatCurrency(contract.current_price, contract.currency || 'USD', contract.symbol)}</TableCell>
                              <TableCell>
                                <Typography color={contract.return >= 0 ? 'success.main' : 'error.main'} fontWeight="medium">
                                  {contract.return >= 0 ? '+' : ''}{contract.return?.toFixed(2)}%
                                </Typography>
                              </TableCell>
                              <TableCell>
                                <Chip 
                                  label={contract.risk_level} 
                                  color={contract.risk_level === 'Low' ? 'success' : contract.risk_level === 'Medium' ? 'warning' : 'error'}
                                  size="small"
                                />
                              </TableCell>
                              <TableCell>{contract.sharpe_ratio?.toFixed(3)}</TableCell>
                              <TableCell>{contract.portfolio_weight?.toFixed(1)}%</TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
                  </CardContent>
                </GlassCard>
              </Grid>
            </Grid>
          ) : (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
              <CircularProgress />
            </Box>
          )}
        </DialogContent>
      </Dialog>

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
    </StyledContainer>
  );
};

export default HedgeInvestments;