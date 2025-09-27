import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Paper,
  Box,
  Card,
  CardContent,
  Button,
  CircularProgress,
} from '@mui/material';
import {
  TrendingUp,
  AccountBalance,
  Security,
  School,
  Assessment,
  MonetizationOn,
} from '@mui/icons-material';
import { apiEndpoints } from '../services/api';

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [healthStatus, setHealthStatus] = useState(null);

  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      const response = await apiEndpoints.health();
      setHealthStatus(response.data);
    } catch (error) {
      console.error('API health check failed:', error);
      setHealthStatus({ status: 'error', message: 'API not available' });
    } finally {
      setLoading(false);
    }
  };

  const features = [
    {
      title: 'Financial Planning',
      description: 'AI-powered personalized financial plans tailored to your goals',
      icon: AccountBalance,
      color: '#1976d2',
      path: '/planner',
    },
    {
      title: 'Investment Advice',
      description: 'Smart investment suggestions based on your risk profile',
      icon: TrendingUp,
      color: '#4caf50',
      path: '/investment',
    },
    {
      title: 'Loan Analysis',
      description: 'Check loan affordability and get the best rates',
      icon: MonetizationOn,
      color: '#ff9800',
      path: '/loan',
    },
    {
      title: 'Financial Literacy',
      description: 'Learn and improve your financial knowledge',
      icon: School,
      color: '#9c27b0',
      path: '/literacy',
    },
    {
      title: 'Fraud Detection',
      description: 'AI-powered fraud detection and security recommendations',
      icon: Security,
      color: '#f44336',
      path: '/fraud-check',
    },
    {
      title: 'Reports & Analytics',
      description: 'Detailed insights into your financial health',
      icon: Assessment,
      color: '#607d8b',
      path: '/reports',
    },
  ];

  const stats = [
    { label: 'Users Helped', value: '10K+', color: '#1976d2' },
    { label: 'Plans Created', value: '25K+', color: '#4caf50' },
    { label: 'Fraud Prevented', value: '$2M+', color: '#f44336' },
    { label: 'Savings Generated', value: '$50M+', color: '#ff9800' },
  ];

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4, textAlign: 'center' }}>
        <CircularProgress size={60} />
        <Typography variant="h6" sx={{ mt: 2 }}>
          Loading Dashboard...
        </Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4, textAlign: 'center' }}>
        <Typography variant="h3" component="h1" gutterBottom fontWeight="bold">
          Welcome to Financial Coach
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ mb: 2 }}>
          Your AI-powered personal finance assistant
        </Typography>
        
        {/* API Status */}
        <Paper
          sx={{
            p: 2,
            backgroundColor: healthStatus?.status === 'healthy' ? '#e8f5e8' : '#ffebee',
            border: `1px solid ${healthStatus?.status === 'healthy' ? '#4caf50' : '#f44336'}`,
            maxWidth: 400,
            mx: 'auto',
          }}
        >
          <Typography variant="body2">
            API Status: {healthStatus?.status === 'healthy' ? '🟢 Online' : '🔴 Offline'}
          </Typography>
          {healthStatus?.message && (
            <Typography variant="body2" color="text.secondary">
              {healthStatus.message}
            </Typography>
          )}
        </Paper>
      </Box>

      {/* Stats */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card
              sx={{
                textAlign: 'center',
                background: `linear-gradient(135deg, ${stat.color}22, ${stat.color}11)`,
                border: `1px solid ${stat.color}`,
              }}
            >
              <CardContent>
                <Typography variant="h4" fontWeight="bold" color={stat.color}>
                  {stat.value}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {stat.label}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Features */}
      <Typography variant="h4" component="h2" gutterBottom sx={{ mb: 3 }}>
        Financial Tools & Services
      </Typography>
      
      <Grid container spacing={3}>
        {features.map((feature, index) => {
          const IconComponent = feature.icon;
          return (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 4,
                  },
                }}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <IconComponent
                      sx={{ fontSize: 40, color: feature.color, mr: 2 }}
                    />
                    <Typography variant="h6" component="h3" fontWeight="bold">
                      {feature.title}
                    </Typography>
                  </Box>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {feature.description}
                  </Typography>
                  <Button
                    variant="contained"
                    fullWidth
                    sx={{
                      backgroundColor: feature.color,
                      '&:hover': {
                        backgroundColor: feature.color,
                        filter: 'brightness(0.9)',
                      },
                    }}
                    href={feature.path}
                  >
                    Get Started
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          );
        })}
      </Grid>

      {/* Quick Actions */}
      <Box sx={{ mt: 6, textAlign: 'center' }}>
        <Typography variant="h5" component="h2" gutterBottom>
          Quick Actions
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
          <Button variant="outlined" size="large" href="/planner">
            Create Financial Plan
          </Button>
          <Button variant="outlined" size="large" href="/investment">
            Get Investment Advice
          </Button>
          <Button variant="outlined" size="large" href="/loan">
            Check Loan Options
          </Button>
          <Button variant="outlined" size="large" href="/literacy">
            Learn Finance Basics
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default Dashboard;