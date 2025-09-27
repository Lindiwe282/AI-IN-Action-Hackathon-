import React, { useState } from 'react';
import {
  Container,
  Typography,
  Grid,
  Paper,
  TextField,
  Button,
  Box,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Alert,
} from '@mui/material';
import { AccountBalance, TrendingUp, Savings } from '@mui/icons-material';
import { apiEndpoints } from '../services/api';

const Planner = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    monthly_income: '',
    monthly_expenses: '',
    current_savings: '',
    total_debt: '',
    age: '',
    dependents: '',
    risk_tolerance: 'medium',
    financial_goals: [],
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Convert string values to numbers
      const data = {
        ...formData,
        monthly_income: parseFloat(formData.monthly_income) || 0,
        monthly_expenses: parseFloat(formData.monthly_expenses) || 0,
        current_savings: parseFloat(formData.current_savings) || 0,
        total_debt: parseFloat(formData.total_debt) || 0,
        age: parseInt(formData.age) || 30,
        dependents: parseInt(formData.dependents) || 0,
        user_id: 1, // Demo user ID
      };

      const response = await apiEndpoints.createPlan(data);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create financial plan');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        <AccountBalance sx={{ mr: 2, verticalAlign: 'middle' }} />
        AI Financial Planner
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Get personalized financial recommendations based on your current situation and goals.
      </Typography>

      <Grid container spacing={4}>
        {/* Input Form */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Your Financial Information
            </Typography>
            
            <Box component="form" onSubmit={handleSubmit}>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Monthly Income"
                    name="monthly_income"
                    type="number"
                    value={formData.monthly_income}
                    onChange={handleInputChange}
                    required
                    InputProps={{ inputProps: { min: 0 } }}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Monthly Expenses"
                    name="monthly_expenses"
                    type="number"
                    value={formData.monthly_expenses}
                    onChange={handleInputChange}
                    required
                    InputProps={{ inputProps: { min: 0 } }}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Current Savings"
                    name="current_savings"
                    type="number"
                    value={formData.current_savings}
                    onChange={handleInputChange}
                    InputProps={{ inputProps: { min: 0 } }}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Total Debt"
                    name="total_debt"
                    type="number"
                    value={formData.total_debt}
                    onChange={handleInputChange}
                    InputProps={{ inputProps: { min: 0 } }}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Age"
                    name="age"
                    type="number"
                    value={formData.age}
                    onChange={handleInputChange}
                    InputProps={{ inputProps: { min: 16, max: 100 } }}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Number of Dependents"
                    name="dependents"
                    type="number"
                    value={formData.dependents}
                    onChange={handleInputChange}
                    InputProps={{ inputProps: { min: 0 } }}
                  />
                </Grid>
                <Grid item xs={12}>
                  <FormControl fullWidth>
                    <InputLabel>Risk Tolerance</InputLabel>
                    <Select
                      name="risk_tolerance"
                      value={formData.risk_tolerance}
                      onChange={handleInputChange}
                      label="Risk Tolerance"
                    >
                      <MenuItem value="low">Conservative (Low Risk)</MenuItem>
                      <MenuItem value="medium">Moderate (Medium Risk)</MenuItem>
                      <MenuItem value="high">Aggressive (High Risk)</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
              </Grid>

              <Button
                type="submit"
                variant="contained"
                size="large"
                fullWidth
                disabled={loading}
                sx={{ mt: 3 }}
              >
                {loading ? <CircularProgress size={24} /> : 'Create Financial Plan'}
              </Button>
            </Box>
          </Paper>
        </Grid>

        {/* Results */}
        <Grid item xs={12} md={6}>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {result && (
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Your Personalized Financial Plan
              </Typography>

              {/* Budget Allocation */}
              {result.plan?.budget_allocation && (
                <Card sx={{ mb: 2 }}>
                  <CardContent>
                    <Typography variant="subtitle1" gutterBottom>
                      <Savings sx={{ mr: 1, verticalAlign: 'middle' }} />
                      Recommended Budget Allocation
                    </Typography>
                    <Grid container spacing={2}>
                      <Grid item xs={4}>
                        <Typography variant="body2" color="text.secondary">Needs</Typography>
                        <Typography variant="h6">
                          ${result.plan.budget_allocation.needs?.toFixed(0)}
                        </Typography>
                        <Typography variant="caption">
                          ({result.plan.budget_allocation.percentages?.needs?.toFixed(1)}%)
                        </Typography>
                      </Grid>
                      <Grid item xs={4}>
                        <Typography variant="body2" color="text.secondary">Wants</Typography>
                        <Typography variant="h6">
                          ${result.plan.budget_allocation.wants?.toFixed(0)}
                        </Typography>
                        <Typography variant="caption">
                          ({result.plan.budget_allocation.percentages?.wants?.toFixed(1)}%)
                        </Typography>
                      </Grid>
                      <Grid item xs={4}>
                        <Typography variant="body2" color="text.secondary">Savings</Typography>
                        <Typography variant="h6">
                          ${result.plan.budget_allocation.savings?.toFixed(0)}
                        </Typography>
                        <Typography variant="caption">
                          ({result.plan.budget_allocation.percentages?.savings?.toFixed(1)}%)
                        </Typography>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              )}

              {/* Risk Assessment */}
              {result.plan?.risk_assessment && (
                <Card sx={{ mb: 2 }}>
                  <CardContent>
                    <Typography variant="subtitle1" gutterBottom>
                      Risk Assessment
                    </Typography>
                    <Typography variant="h6" color={
                      result.plan.risk_assessment.level === 'Low' ? 'success.main' :
                      result.plan.risk_assessment.level === 'Medium' ? 'warning.main' : 'error.main'
                    }>
                      {result.plan.risk_assessment.level} Risk
                    </Typography>
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      Score: {result.plan.risk_assessment.score}/10
                    </Typography>
                    {result.plan.risk_assessment.factors?.length > 0 && (
                      <Box sx={{ mt: 1 }}>
                        <Typography variant="body2" fontWeight="bold">Risk Factors:</Typography>
                        {result.plan.risk_assessment.factors.map((factor, index) => (
                          <Typography key={index} variant="body2" color="text.secondary">
                            • {factor}
                          </Typography>
                        ))}
                      </Box>
                    )}
                  </CardContent>
                </Card>
              )}

              {/* Recommendations */}
              {result.plan?.recommendations && result.plan.recommendations.length > 0 && (
                <Card sx={{ mb: 2 }}>
                  <CardContent>
                    <Typography variant="subtitle1" gutterBottom>
                      <TrendingUp sx={{ mr: 1, verticalAlign: 'middle' }} />
                      AI Recommendations
                    </Typography>
                    {result.plan.recommendations.map((rec, index) => (
                      <Box key={index} sx={{ mb: 2, p: 2, backgroundColor: 'grey.50', borderRadius: 1 }}>
                        <Typography variant="body2" fontWeight="bold" color={
                          rec.priority === 'critical' ? 'error.main' :
                          rec.priority === 'high' ? 'warning.main' : 'info.main'
                        }>
                          {rec.priority?.toUpperCase()} PRIORITY
                        </Typography>
                        <Typography variant="body2" sx={{ mt: 0.5 }}>
                          {rec.message}
                        </Typography>
                        {rec.suggested_action && (
                          <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                            Action: {rec.suggested_action}
                          </Typography>
                        )}
                      </Box>
                    ))}
                  </CardContent>
                </Card>
              )}

              {/* Emergency Fund */}
              {result.plan?.emergency_fund && (
                <Card>
                  <CardContent>
                    <Typography variant="subtitle1" gutterBottom>
                      Emergency Fund Goal
                    </Typography>
                    <Typography variant="body2">
                      Target Amount: ${result.plan.emergency_fund.target_amount?.toFixed(0)}
                    </Typography>
                    <Typography variant="body2">
                      Current Amount: ${result.plan.emergency_fund.current_amount?.toFixed(0)}
                    </Typography>
                    <Typography variant="body2" color={
                      result.plan.emergency_fund.shortfall > 0 ? 'warning.main' : 'success.main'
                    }>
                      {result.plan.emergency_fund.shortfall > 0 
                        ? `Shortfall: $${result.plan.emergency_fund.shortfall.toFixed(0)}`
                        : 'Goal achieved! ✅'
                      }
                    </Typography>
                  </CardContent>
                </Card>
              )}
            </Paper>
          )}

          {!result && !error && !loading && (
            <Paper sx={{ p: 3, textAlign: 'center', backgroundColor: 'grey.50' }}>
              <Typography variant="body1" color="text.secondary">
                Fill out the form to get your personalized financial plan
              </Typography>
            </Paper>
          )}
        </Grid>
      </Grid>
    </Container>
  );
};

export default Planner;