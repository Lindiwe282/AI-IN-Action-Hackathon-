import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  LinearProgress,
  Alert,
  Paper,
  Grid,
  TextField
} from '@mui/material';
import { Security, UploadFile } from '@mui/icons-material';
import axios from 'axios';

const FraudCheck = () => {
  const [pdfFile, setPdfFile] = useState(null);
  const [amount, setAmount] = useState('');
  const [interestRate, setInterestRate] = useState('');
  const [promisedReturn, setPromisedReturn] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setPdfFile(file);
    setResult(null);
  };

  const handleSubmit = async () => {
    if (!pdfFile) {
      alert('Please upload a PDF file.');
      return;
    }

    const formData = new FormData();
    formData.append('pdf', pdfFile);
    formData.append('amount', amount || 0);
    formData.append('interest_rate', interestRate || 0);
    formData.append('promised_return', promisedReturn || 0);

    setLoading(true);
    try {
      const res = await axios.post(
        'http://localhost:5000/api/fraud/detect',
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' }, timeout: 30000 }
      );
      setResult(res.data);
    } catch (error) {
      console.error(error);
      alert('Error analyzing the PDF. Make sure backend is running.');
    }
    setLoading(false);
  };

  const resetForm = () => {
    setPdfFile(null);
    setAmount('');
    setInterestRate('');
    setPromisedReturn('');
    setResult(null);
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 6 }}>
      {/* Header */}
      <Paper elevation={3} sx={{ p: 4, mb: 4, textAlign: 'center' }}>
        <Security sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
        <Typography variant="h4" gutterBottom>
          Investment Fraud Detection
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Upload an investment document and optionally enter financial details for AI-powered fraud analysis
        </Typography>
      </Paper>

      <Grid container spacing={4}>
        {/* Upload Section */}
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>1. Upload Document</Typography>
            <Button
              variant="outlined"
              component="label"
              startIcon={<UploadFile />}
              fullWidth
              sx={{ mb: 2, py: 2 }}
            >
              Choose PDF File
              <input type="file" accept="application/pdf" hidden onChange={handleFileChange} />
            </Button>
            {pdfFile && (
              <Alert severity="success" sx={{ mt: 2 }}>
                Selected: {pdfFile.name} ({(pdfFile.size / 1024 / 1024).toFixed(2)} MB)
              </Alert>
            )}
          </Paper>
        </Grid>

        {/* Financial Details Section (optional) */}
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>2. Financial Details (Optional)</Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <TextField
                label="Investment Amount (ZAR)"
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                fullWidth
              />
              <TextField
                label="Interest Rate (%)"
                type="number"
                value={interestRate}
                onChange={(e) => setInterestRate(e.target.value)}
                fullWidth
              />
              <TextField
                label="Promised Return (%)"
                type="number"
                value={promisedReturn}
                onChange={(e) => setPromisedReturn(e.target.value)}
                fullWidth
              />
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {/* Action Buttons */}
      <Box sx={{ mt: 4, display: 'flex', gap: 2, justifyContent: 'center' }}>
        <Button
          variant="contained"
          size="large"
          onClick={handleSubmit}
          disabled={loading || !pdfFile}
          sx={{ minWidth: 200 }}
        >
          {loading ? 'Analyzing...' : 'Analyze for Fraud'}
        </Button>
        <Button variant="outlined" size="large" onClick={resetForm} disabled={loading}>
          Reset
        </Button>
      </Box>

      {loading && (
        <Box sx={{ mt: 3 }}>
          <LinearProgress />
          <Typography variant="body2" align="center" sx={{ mt: 1 }}>
            Analyzing your document for potential fraud indicators...
          </Typography>
        </Box>
      )}

      {/* Results Section */}
      {result && (
        <Paper elevation={3} sx={{ mt: 4, p: 4 }}>
          <Typography variant="h5" gutterBottom>Analysis Results</Typography>
          <Alert severity={result.is_fraud ? 'error' : 'success'} sx={{ mb: 3 }}>
            Fraud Risk: {(result.fraud_probability * 100).toFixed(1)}%<br />
            Assessment: {result.is_fraud ? '⚠️ High Risk - Potentially Fraudulent' : '✅ Low Risk - Appears Legitimate'}
          </Alert>
          {result.red_flags && result.red_flags.length > 0 && (
            <Box>
              <Typography variant="h6" color="error">Red Flags Detected:</Typography>
              <ul>
                {result.red_flags.map((flag, i) => (
                  <li key={i}><Typography variant="body2" color="error">{flag}</Typography></li>
                ))}
              </ul>
            </Box>
          )}
        </Paper>
      )}
    </Container>
  );
};

export default FraudCheck;
