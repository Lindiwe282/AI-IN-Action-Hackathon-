import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  IconButton,
  Link,
  Divider,
  Alert,
  CircularProgress,
  Chip,
} from '@mui/material';
import {
  Close,
  OpenInNew,
  Download,
  AccountBalance,
  TrendingUp,
  Public,
  LocationOn,
} from '@mui/icons-material';
import { styled } from '@mui/material/styles';
import axios from 'axios';

const StyledCard = styled(Card)(({ theme }) => ({
  height: '100%',
  transition: 'all 0.2s ease-in-out',
  cursor: 'pointer',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: theme.shadows[8],
  },
}));

const FlagIcon = styled('img')({
  width: 24,
  height: 16,
  borderRadius: 2,
  marginRight: 8,
});

const BrokerDialog = ({ open, onClose }) => {
  const [downloading, setDownloading] = useState(false);
  const [downloadStatus, setDownloadStatus] = useState('');

  // South African brokers
  const southAfricanBrokers = [
    {
      name: 'Standard Bank',
      url: 'https://www.standardbank.co.za/southafrica/personal/products-and-services/bank-with-us/investment-and-insurance-solutions/webtrader',
      description: 'Leading South African bank with comprehensive trading platform',
      type: 'Full Service Bank',
    },
    {
      name: 'Nedbank',
      url: 'https://www.nedbank.co.za/content/nedbank/desktop/gt/en/personal/invest/shares-and-investments.html',
      description: 'Major South African bank offering investment services',
      type: 'Full Service Bank',
    },
    {
      name: 'FNB Securities',
      url: 'https://www.fnb.co.za/ways-to-bank/online-banking/investec-online-share-trading.html',
      description: 'FNB\'s dedicated securities trading platform',
      type: 'Bank Securities',
    },
    {
      name: 'Easy Equities',
      url: 'https://www.easyequities.co.za/',
      description: 'Popular South African online trading platform',
      type: 'Online Broker',
    },
    {
      name: 'Investec',
      url: 'https://www.investec.com/en_za/focus/investing.html',
      description: 'Premium investment and wealth management services',
      type: 'Investment Bank',
    },
    {
      name: 'Sanlam iTrade',
      url: 'https://www.sanlamitrade.co.za/',
      description: 'Sanlam\'s online share trading platform',
      type: 'Insurance & Investment',
    },
  ];

  // American brokers
  const americanBrokers = [
    {
      name: 'Charles Schwab',
      url: 'https://www.schwab.com/',
      description: 'Full-service brokerage with excellent research tools',
      type: 'Full Service Broker',
    },
    {
      name: 'Fidelity',
      url: 'https://www.fidelity.com/',
      description: 'Leading investment firm with zero-fee trading',
      type: 'Full Service Broker',
    },
    {
      name: 'TD Ameritrade',
      url: 'https://www.tdameritrade.com/',
      description: 'Comprehensive trading platform with advanced tools',
      type: 'Full Service Broker',
    },
    {
      name: 'E*TRADE',
      url: 'https://us.etrade.com/home',
      description: 'Popular online broker with user-friendly platform',
      type: 'Online Broker',
    },
    {
      name: 'Interactive Brokers',
      url: 'https://www.interactivebrokers.com/',
      description: 'Professional-grade trading platform with global access',
      type: 'Professional Broker',
    },
    {
      name: 'Robinhood',
      url: 'https://robinhood.com/',
      description: 'Commission-free trading with mobile-first approach',
      type: 'Mobile Broker',
    },
  ];

  const handleDownloadPortfolios = async () => {
    setDownloading(true);
    setDownloadStatus('');

    try {
      // Get investment portfolio
      const investmentResponse = await axios.get('http://localhost:5000/api/investment/portfolio');
      let investmentPortfolio = [];
      
      if (investmentResponse.data && investmentResponse.data.portfolio) {
        investmentPortfolio = investmentResponse.data.portfolio.map(item => ({
          Symbol: item.symbol || item.ticker,
          'Current Price': item.current_price || item.price || 0,
          Date: new Date().toLocaleDateString('en-US'),
          Quantity: item.quantity || item.shares || 0,
          Source: 'Investment'
        }));
      }

      // Get hedge portfolio
      let hedgePortfolio = [];
      try {
        const hedgeResponse = await axios.get('http://localhost:5000/api/hedge/portfolio');
        if (hedgeResponse.data && hedgeResponse.data.portfolio) {
          hedgePortfolio = hedgeResponse.data.portfolio.map(item => ({
            Symbol: item.symbol || item.ticker,
            'Current Price': item.current_price || item.price || 0,
            Date: new Date().toLocaleDateString('en-US'),
            Quantity: item.quantity || item.shares || 0,
            Source: 'Hedge'
          }));
        }
      } catch (hedgeError) {
        console.log('Hedge portfolio not available:', hedgeError.message);
      }

      // If no portfolios found, create sample data
      let combinedPortfolio = [...investmentPortfolio, ...hedgePortfolio];
      
      if (combinedPortfolio.length === 0) {
        combinedPortfolio = [
          { Symbol: 'AAPL', 'Current Price': 255.460, Date: '9/27/2025', Quantity: 48.56, Source: 'Sample' },
          { Symbol: 'AMZN', 'Current Price': 219.780, Date: '9/27/2025', Quantity: 20.79, Source: 'Sample' },
          { Symbol: 'GOOGL', 'Current Price': 246.540, Date: '9/27/2025', Quantity: 52.47, Source: 'Sample' },
          { Symbol: 'JPM', 'Current Price': 316.060, Date: '9/27/2025', Quantity: 116.37, Source: 'Sample' },
          { Symbol: 'MCD', 'Current Price': 305.240, Date: '9/27/2025', Quantity: 41.37, Source: 'Sample' },
          { Symbol: 'MSFT', 'Current Price': 511.460, Date: '9/27/2025', Quantity: 15.06, Source: 'Sample' },
          { Symbol: 'NVDA', 'Current Price': 178.190, Date: '9/27/2025', Quantity: 72.84, Source: 'Sample' },
        ];
      }

      // Convert to CSV
      const headers = ['Symbol', 'Current Price', 'Date', 'Quantity'];
      const csvContent = [
        headers.join(','),
        ...combinedPortfolio.map(item => 
          headers.map(header => item[header]).join(',')
        )
      ].join('\n');

      // Create and download the file
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      link.setAttribute('download', `portfolio_${new Date().toISOString().split('T')[0]}.csv`);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      setDownloadStatus(`Successfully downloaded portfolio with ${combinedPortfolio.length} holdings`);
    } catch (error) {
      console.error('Error downloading portfolios:', error);
      setDownloadStatus('Error downloading portfolios. Please try again.');
    } finally {
      setDownloading(false);
    }
  };

  const BrokerCard = ({ broker, country }) => (
    <StyledCard>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          {country === 'SA' ? (
            <FlagIcon src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAyNCAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjI0IiBoZWlnaHQ9IjE2IiBmaWxsPSIjRkZGRkZGIi8+CjxwYXRoIGQ9Ik0wIDBIMjRWNkg0TDBaIiBmaWxsPSIjMDBBMDM5Ii8+CjxwYXRoIGQ9Ik0wIDEwSDI0VjE2SDRMMTBaIiBmaWxsPSIjMDBBMDM5Ii8+CjxwYXRoIGQ9Ik0wIDZIMjRWMTBIMFY2WiIgZmlsbD0iI0ZGRjMwMCIvPgo8L3N2Zz4K" alt="South Africa" />
          ) : (
            <FlagIcon src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAyNCAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjI0IiBoZWlnaHQ9IjE2IiBmaWxsPSIjQjIyMjM0Ii8+CjxyZWN0IHdpZHRoPSIyNCIgaGVpZ2h0PSIxLjIzIiBmaWxsPSIjRkZGRkZGIi8+CjxyZWN0IHk9IjIuNDYiIHdpZHRoPSIyNCIgaGVpZ2h0PSIxLjIzIiBmaWxsPSIjRkZGRkZGIi8+Cjwvc3ZnPgo=" alt="United States" />
          )}
          <Typography variant="h6" component="h3" sx={{ fontWeight: 'bold' }}>
            {broker.name}
          </Typography>
        </Box>
        
        <Chip 
          label={broker.type} 
          size="small" 
          color="primary" 
          sx={{ mb: 1 }}
        />
        
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          {broker.description}
        </Typography>
        
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Link
            href={broker.url}
            target="_blank"
            rel="noopener noreferrer"
            sx={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }}
          >
            <Button
              variant="outlined"
              size="small"
              startIcon={<OpenInNew />}
            >
              Visit Site
            </Button>
          </Link>
        </Box>
      </CardContent>
    </StyledCard>
  );

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="lg"
      fullWidth
      PaperProps={{
        sx: {
          borderRadius: 3,
          minHeight: '80vh',
        }
      }}
    >
      <DialogTitle sx={{ pb: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h4" component="h2" sx={{ fontWeight: 'bold' }}>
            Choose Your Broker
          </Typography>
          <IconButton onClick={onClose} size="large">
            <Close />
          </IconButton>
        </Box>
        <Typography variant="body1" color="text.secondary">
          Select from trusted brokers to start your investment journey
        </Typography>
      </DialogTitle>

      <DialogContent sx={{ px: 3 }}>
        {/* South African Brokers */}
        <Box sx={{ mb: 4 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <LocationOn sx={{ mr: 1, color: 'primary.main' }} />
            <Typography variant="h5" component="h3" sx={{ fontWeight: 'bold' }}>
              South African Brokers
            </Typography>
          </Box>
          
          <Grid container spacing={2}>
            {southAfricanBrokers.map((broker, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <BrokerCard broker={broker} country="SA" />
              </Grid>
            ))}
          </Grid>
        </Box>

        <Divider sx={{ my: 3 }} />

        {/* American Brokers */}
        <Box sx={{ mb: 4 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Public sx={{ mr: 1, color: 'primary.main' }} />
            <Typography variant="h5" component="h3" sx={{ fontWeight: 'bold' }}>
              American Brokers
            </Typography>
          </Box>
          
          <Grid container spacing={2}>
            {americanBrokers.map((broker, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <BrokerCard broker={broker} country="US" />
              </Grid>
            ))}
          </Grid>
        </Box>

        <Divider sx={{ my: 3 }} />

        {/* Portfolio Download Section */}
        {/* <Box sx={{ textAlign: 'center', p: 3, bgcolor: 'background.paper', borderRadius: 2 }}>
          <TrendingUp sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
          <Typography variant="h6" component="h3" gutterBottom>
            Download Your Recommended Portfolio
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Get your personalized investment and hedge fund recommendations as a CSV file
          </Typography>
          
          <Button
            variant="contained"
            size="large"
            startIcon={downloading ? <CircularProgress size={20} /> : <Download />}
            onClick={handleDownloadPortfolios}
            disabled={downloading}
            sx={{ px: 4, py: 1.5 }}
          >
            {downloading ? 'Downloading...' : 'Download Portfolio CSV'}
          </Button>

          {downloadStatus && (
            <Alert 
              severity={downloadStatus.includes('Error') ? 'error' : 'success'} 
              sx={{ mt: 2, maxWidth: 600, mx: 'auto' }}
            >
              {downloadStatus}
            </Alert>
          )}
        </Box> */}
      </DialogContent>

      <DialogActions sx={{ px: 3, pb: 3 }}>
        <Button onClick={onClose} variant="outlined" size="large">
          Close
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default BrokerDialog;