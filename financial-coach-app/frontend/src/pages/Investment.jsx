import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import { TrendingUp } from '@mui/icons-material';

const Investment = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ textAlign: 'center' }}>
        <TrendingUp sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
        <Typography variant="h4" component="h1" gutterBottom>
          Investment Advisory
        </Typography>
        <Typography variant="body1" color="text.secondary">
          AI-powered investment recommendations coming soon...
        </Typography>
      </Box>
    </Container>
  );
};

export default Investment;