import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Container,
} from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Dashboard as DashboardIcon,
  AccountBalance as PlannerIcon,
  TrendingUp as InvestmentIcon,
  Money as LoanIcon,
  School as LiteracyIcon,
  Security as FraudIcon,
} from '@mui/icons-material';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    { label: 'Dashboard', path: '/dashboard', icon: DashboardIcon },
    { label: 'Planner', path: '/planner', icon: PlannerIcon },
    { label: 'Investment', path: '/investment', icon: InvestmentIcon },
    { label: 'Loan', path: '/loan', icon: LoanIcon },
    { label: 'Literacy', path: '/literacy', icon: LiteracyIcon },
    { label: 'Fraud Check', path: '/fraud-check', icon: FraudIcon },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <AppBar position="fixed" sx={{ zIndex: 1201 }}>
      <Container maxWidth="xl">
        <Toolbar>
          <Typography
            variant="h6"
            component="div"
            sx={{ flexGrow: 1, fontWeight: 'bold', cursor: 'pointer' }}
            onClick={() => navigate('/')}
          >
            💰 Financial Coach
          </Typography>
          
          <Box sx={{ display: { xs: 'none', md: 'flex' }, gap: 1 }}>
            {menuItems.map((item) => {
              const IconComponent = item.icon;
              return (
                <Button
                  key={item.path}
                  color="inherit"
                  onClick={() => navigate(item.path)}
                  startIcon={<IconComponent />}
                  sx={{
                    minWidth: 'auto',
                    px: 2,
                    borderRadius: 2,
                    backgroundColor: isActive(item.path) ? 'rgba(255,255,255,0.1)' : 'transparent',
                    '&:hover': {
                      backgroundColor: 'rgba(255,255,255,0.1)',
                    },
                  }}
                >
                  {item.label}
                </Button>
              );
            })}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navbar;