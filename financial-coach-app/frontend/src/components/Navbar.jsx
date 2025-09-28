import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Container,
  IconButton,
  Menu,
  MenuItem,
  useMediaQuery,
  useTheme,
  Avatar,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  AccountBalance as PlannerIcon,
  TrendingUp as InvestmentIcon,
  Money as LoanIcon,
  School as LiteracyIcon,
  Security as FraudIcon,
  AccountBalanceWallet,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import BrokerDialog from './BrokerDialog';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [anchorEl, setAnchorEl] = React.useState(null);
  const [brokerDialogOpen, setBrokerDialogOpen] = React.useState(false);

  const menuItems = [
    { label: 'Dashboard', path: '/dashboard', icon: DashboardIcon },
    { label: 'Planner', path: '/planner', icon: PlannerIcon },
    { label: 'Investment', path: '/investment', icon: InvestmentIcon },
    // { label: 'Loan', path: '/loan', icon: LoanIcon },
    { label: 'Literacy', path: '/literacy', icon: LiteracyIcon },
    { label: 'Security', path: '/fraud-check', icon: FraudIcon },
  ];

  const isActive = (path) => location.pathname === path;

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleNavigate = (path) => {
    navigate(path);
    handleMenuClose();
  };

  return (
    <AppBar 
      position="fixed" 
      sx={{ 
        zIndex: 1201,
        background: 'linear-gradient(135deg, rgba(248, 250, 252, 0.95) 0%, rgba(226, 232, 240, 0.98) 100%)',
        backdropFilter: 'blur(10px)',
        borderBottom: '1px solid rgba(135, 169, 107, 0.2)',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
      }}
    >
      <Container maxWidth="xl">
        <Toolbar sx={{ py: 1 }}>
          {/* Logo/Brand */}
          <Box 
            sx={{ 
              display: 'flex', 
              alignItems: 'center', 
              cursor: 'pointer',
              '&:hover': {
                transform: 'scale(1.02)',
                transition: 'transform 0.2s ease'
              }
            }}
            onClick={() => navigate('/')}
          >
            <Avatar
              sx={{
                background: 'linear-gradient(135deg, #87a96b 0%, #6b8e47 100%)',
                mr: 2,
                width: 40,
                height: 40,
              }}
            >
              <AccountBalanceWallet sx={{ color: 'white' }} />
            </Avatar>
            <Box>
              <Typography
                variant="h5"
                component="div"
                sx={{ 
                  fontWeight: 'bold',
                  color: '#1e293b',
                  lineHeight: 1,
                  fontSize: { xs: '1.2rem', md: '1.5rem' }
                }}
              >
                Financial Coach
              </Typography>
              <Typography
                variant="caption"
                sx={{ 
                  color: '#64748b',
                  fontSize: '0.75rem',
                  display: { xs: 'none', sm: 'block' }
                }}
              >
                Your Financial Future, Secured
              </Typography>
            </Box>
          </Box>
          
          <Box sx={{ flexGrow: 1 }} />

          {/* Desktop Navigation */}
          {!isMobile ? (
            <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
              {menuItems.map((item) => {
                const IconComponent = item.icon;
                const active = isActive(item.path);
                return (
                  <Button
                    key={item.path}
                    color="inherit"
                    onClick={() => navigate(item.path)}
                    startIcon={React.createElement(IconComponent, { sx: { fontSize: '1.1rem' } })}
                    sx={{
                      minWidth: 'auto',
                      px: 2.5,
                      py: 1,
                      borderRadius: 3,
                      textTransform: 'none',
                      fontSize: '0.95rem',
                      fontWeight: active ? 'bold' : 'medium',
                      color: active ? '#6b8e47' : '#475569',
                      backgroundColor: active 
                        ? 'rgba(135, 169, 107, 0.1)' 
                        : 'transparent',
                      border: active 
                        ? '1px solid rgba(135, 169, 107, 0.3)' 
                        : '1px solid transparent',
                      '&:hover': {
                        backgroundColor: 'rgba(135, 169, 107, 0.08)',
                        transform: 'translateY(-1px)',
                        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
                      },
                      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                    }}
                  >
                    {item.label}
                  </Button>
                );
              })}
              
              {/* Optional: Profile/Settings Button */}
              <Button
                variant="outlined"
                onClick={() => setBrokerDialogOpen(true)}
                sx={{
                  ml: 2,
                  borderColor: '#87a96b',
                  color: '#6b8e47',
                  borderRadius: 3,
                  textTransform: 'none',
                  px: 3,
                  fontWeight: 'medium',
                  '&:hover': {
                    borderColor: '#6b8e47',
                    backgroundColor: 'rgba(135, 169, 107, 0.08)',
                  },
                }}
              >
                Get Started
              </Button>
            </Box>
          ) : (
            // Mobile Navigation
            <>
              <IconButton
                color="inherit"
                onClick={handleMenuOpen}
                sx={{
                  backgroundColor: 'rgba(135, 169, 107, 0.1)',
                  color: '#6b8e47',
                  '&:hover': {
                    backgroundColor: 'rgba(135, 169, 107, 0.15)',
                  },
                }}
              >
                <MenuIcon />
              </IconButton>
              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleMenuClose}
                PaperProps={{
                  sx: {
                    background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)',
                    color: '#1e293b',
                    mt: 1,
                    minWidth: 200,
                    borderRadius: 2,
                    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
                    border: '1px solid rgba(135, 169, 107, 0.2)',
                  },
                }}
              >
                {menuItems.map((item) => {
                  const IconComponent = item.icon;
                  const active = isActive(item.path);
                  return (
                    <MenuItem
                      key={item.path}
                      onClick={() => handleNavigate(item.path)}
                      sx={{
                        py: 1.5,
                        px: 2,
                        backgroundColor: active 
                          ? 'rgba(135, 169, 107, 0.1)' 
                          : 'transparent',
                        '&:hover': {
                          backgroundColor: 'rgba(135, 169, 107, 0.08)',
                        },
                      }}
                    >
                      {React.createElement(IconComponent, { sx: { mr: 2, fontSize: '1.2rem' } })}
                      <Typography sx={{ fontWeight: active ? 'bold' : 'normal', color: active ? '#6b8e47' : '#475569' }}>
                        {item.label}
                      </Typography>
                    </MenuItem>
                  );
                })}
                <MenuItem
                  onClick={() => handleNavigate('/get-started')}
                  sx={{
                    py: 1.5,
                    px: 2,
                    borderTop: '1px solid rgba(135, 169, 107, 0.2)',
                    mt: 1,
                    '&:hover': {
                      backgroundColor: 'rgba(135, 169, 107, 0.08)',
                    },
                  }}
                >
                  
                </MenuItem>
              </Menu>
            </>
          )}
        </Toolbar>
      </Container>

      {/* Broker Dialog */}
      <BrokerDialog 
        open={brokerDialogOpen} 
        onClose={() => setBrokerDialogOpen(false)} 
      />
    </AppBar>
  );
};

export default Navbar;