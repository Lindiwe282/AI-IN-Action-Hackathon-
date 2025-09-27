import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import { School } from '@mui/icons-material';

const Literacy = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ textAlign: 'center' }}>
        <School sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
        <Typography variant="h4" component="h1" gutterBottom>
          Financial Literacy Hub
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Educational content and financial tips coming soon...
        </Typography>
      </Box>
    </Container>
  );
};

export default Literacy;