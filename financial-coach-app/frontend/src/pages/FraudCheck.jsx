import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import { Security } from '@mui/icons-material';

const FraudCheck = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ textAlign: 'center' }}>
        <Security sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
        <Typography variant="h4" component="h1" gutterBottom>
          Fraud Detection & Security
        </Typography>
        <Typography variant="body1" color="text.secondary">
          AI-powered fraud detection and security analysis coming soon...
        </Typography>
      </Box>
    </Container>
  );
};

export default FraudCheck;