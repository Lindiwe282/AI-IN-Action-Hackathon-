import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import { MonetizationOn } from '@mui/icons-material';

const Loan = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ textAlign: 'center' }}>
        <MonetizationOn sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
        <Typography variant="h4" component="h1" gutterBottom>
          Loan Affordability Checker
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Smart loan analysis and recommendations coming soon...
        </Typography>
      </Box>
    </Container>
  );
};

export default Loan;