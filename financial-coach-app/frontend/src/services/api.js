import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth tokens (if needed)
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const apiEndpoints = {
  // Health check
  health: () => api.get('/health'),
  
  // Financial Planning
  createPlan: (data) => api.post('/planner/create', data),
  getRecommendations: (userId) => api.get(`/planner/recommendations/${userId}`),
  updatePlan: (planId, data) => api.put(`/planner/update/${planId}`, data),
  
  // Investment
  getInvestmentSuggestions: (data) => api.post('/investment/suggestions', data),
  analyzePortfolio: (data) => api.post('/investment/analyze', data),
  getMarketInsights: () => api.get('/investment/insights'),
  
  // Loan
  checkAffordability: (data) => api.post('/loan/affordability', data),
  calculateLoan: (data) => api.post('/loan/calculate', data),
  getLoanRecommendations: (data) => api.post('/loan/recommendations', data),
  
  // Financial Literacy
  getTips: (params) => api.get('/literacy/tips', { params }),
  takeQuiz: (data) => api.post('/literacy/quiz', data),
  getResources: (params) => api.get('/literacy/resources', { params }),
  
  // Fraud Detection
  detectFraud: (data) => api.post('/fraud/detect', data),
  analyzePatterns: (data) => api.post('/fraud/analyze-patterns', data),
  getSecurityRecommendations: (data) => api.post('/fraud/security-recommendations', data),
};

export default api;