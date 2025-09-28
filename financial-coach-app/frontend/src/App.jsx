import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Planner from './pages/Planner';
import Investment from './pages/Investment';
import NewsAnalyzer from './pages/NewsAnalyzer';
import Loan from './pages/Loan';
import Literacy from './pages/Literacy';
import FraudCheck from './pages/FraudCheck';
import './assets/styles.css';

// Create Material-UI theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
    h5: {
      fontWeight: 500,
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <box>
          
        </box>
        <div className="App">
          <Navbar />
          <main style={{ paddingTop: '80px', minHeight: '100vh' }}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/planner" element={<Planner />} />
              <Route path="/investment" element={<Investment />} />
              <Route path="/news-analyzer" element={<NewsAnalyzer />} />
              <Route path="/loan" element={<Loan />} />
              <Route path="/literacy" element={<Literacy />} />
              <Route path="/fraud-check" element={<FraudCheck />} />
            </Routes>
          </main>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;