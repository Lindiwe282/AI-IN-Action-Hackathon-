import React, { useState, useEffect, useMemo } from 'react';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  CircularProgress,
  Chip,
  Avatar,
  Fade,
  Grow,
  Paper,
  Box,
  useTheme,
  useMediaQuery,
  Divider,
  IconButton
} from '@mui/material';
import {
  TrendingUp,
  AccountBalance,
  Security,
  School,
  Assessment,
  MonetizationOn,
  Star,
  CheckCircle,
  Shield,
  ArrowForward,
  PlayArrow,
  Lock,
  VerifiedUser,
  Verified,
  AutoAwesome,
  Timeline,
  Analytics,
  Lightbulb,
  Close
} from '@mui/icons-material';

// Enhanced constants with better structure
const FEATURES = [
  {
    title: 'Smart Financial Planner',
    description: 'AI-powered budgeting with personalized insights and automated goal tracking for optimal financial growth',
    icon: AccountBalance,
    gradient: 'linear-gradient(135deg, rgba(135, 169, 107, 0.8) 0%, rgba(107, 142, 71, 0.9) 100%)',
    path: '/planner',
    badge: 'AI-Powered',
    accent: '#4ade80',
    features: ['Auto-categorization', 'Goal tracking', 'Smart alerts']
  },
  {
    title: 'Investment Analytics',
    description: 'Advanced portfolio analysis with real-time market data, risk assessment, and performance optimization',
    icon: TrendingUp,
    gradient: 'linear-gradient(135deg, rgba(164, 195, 115, 0.8) 0%, rgba(135, 169, 107, 0.9) 100%)',
    path: '/investment',
    badge: 'Pro Analytics',
    accent: '#22c55e',
    features: ['Real-time data', 'Risk analysis', 'ROI tracking']
  },
  {
    title: 'Loan Optimizer',
    description: 'Intelligent loan comparison with payment scenarios, refinancing opportunities, and debt optimization',
    icon: MonetizationOn,
    gradient: 'linear-gradient(135deg, rgba(184, 212, 126, 0.8) 0%, rgba(164, 195, 115, 0.9) 100%)',
    path: '/loan',
    badge: 'Smart Compare',
    accent: '#16a34a',
    features: ['Rate comparison', 'Payment calc', 'Refinance alerts']
  },
  {
    title: 'Interactive Learning',
    description: 'Gamified financial education with personalized learning paths, quizzes, and achievement tracking',
    icon: School,
    gradient: 'linear-gradient(135deg, rgba(194, 216, 138, 0.8) 0%, rgba(184, 212, 126, 0.9) 100%)',
    path: '/literacy',
    badge: 'Gamified',
    accent: '#15803d',
    features: ['Learning paths', 'Achievements', 'Progress tracking']
  },
  {
    title: 'Fraud Protection',
    description: 'Advanced threat detection with ML-powered monitoring, instant alerts, and security recommendations',
    icon: Security,
    gradient: 'linear-gradient(135deg, rgba(135, 169, 107, 0.8) 0%, rgba(107, 142, 71, 0.9) 100%)',
    path: '/fraud-check',
    badge: 'AI Security',
    accent: '#166534',
    features: ['Threat detection', 'Instant alerts', 'Security tips']
  },
  {
    title: 'Advanced Insights',
    description: 'Comprehensive analytics dashboard with predictive modeling, trend analysis, and custom reports',
    icon: Assessment,
    gradient: 'linear-gradient(135deg, rgba(164, 195, 115, 0.8) 0%, rgba(135, 169, 107, 0.9) 100%)',
    path: '/reports',
    badge: 'Premium',
    accent: '#14532d',
    features: ['Predictive models', 'Custom reports', 'Trend analysis']
  },
];

const FINANCIAL_FACTS = [
  {
    fact: 'Simple Interest: Calculated only on the principal. SI = P × R × T.',
    category: 'Basic Concepts',
    difficulty: 'Beginner',
    icon: '💰'
  },
  {
    fact: 'Compound Interest: Calculated on principal + accumulated interest. CI = P × (1 + R/n)^(n×T) - P.',
    category: 'Investing',
    difficulty: 'Intermediate',
    icon: '📈'
  },
  {
    fact: 'Compounding Periods: Defines how often interest is applied: annually, quarterly, monthly, etc.',
    category: 'Investing',
    difficulty: 'Intermediate',
    icon: '⏰'
  },
  {
    fact: 'Investment: Putting money to work to earn more money, balancing safety and growth potential.',
    category: 'Investing',
    difficulty: 'Beginner',
    icon: '🎯'
  },
  {
    fact: 'Savings Account: Low-risk, bank-provided account that earns interest steadily.',
    category: 'Banking',
    difficulty: 'Beginner',
    icon: '🏦'
  },
  {
    fact: 'Government Bonds: Loans to the government with fixed interest, very safe for conservative investors.',
    category: 'Investing',
    difficulty: 'Intermediate',
    icon: '🛡️'
  },
  {
    fact: 'The Rule of 72: Divide 72 by your interest rate to estimate how long it takes your money to double.',
    category: 'Investing',
    difficulty: 'Beginner',
    icon: '🧮'
  },
  {
    fact: 'Diversification: Spreading investments across different assets to reduce risk.',
    category: 'Risk Management',
    difficulty: 'Intermediate',
    icon: '🌐'
  },
  {
    fact: 'Emergency Fund: 3-6 months of living expenses saved for unexpected events.',
    category: 'Planning',
    difficulty: 'Beginner',
    icon: '🆘'
  },
  {
    fact: 'Credit Score: A number between 300-850 that represents your creditworthiness.',
    category: 'Credit',
    difficulty: 'Beginner',
    icon: '📊'
  }
];

const TESTIMONIALS = [
  { 
    name: 'Sarah Mitchell', 
    role: 'Marketing Manager', 
    rating: 5, 
    text: 'The AI-powered insights helped me optimize my investments and achieve 22% better returns while learning along the way!',
    avatar: 'SM',
    achievement: 'Saved $15K in first year',
    timeframe: '8 months ago'
  },
  { 
    name: 'David Chen', 
    role: 'Software Engineer', 
    rating: 5, 
    text: 'Security features gave me confidence to invest more. The fraud detection caught two suspicious transactions!',
    avatar: 'DC',
    achievement: 'Portfolio grew 35%',
    timeframe: '6 months ago'
  },
  { 
    name: 'Lisa Rodriguez', 
    role: 'Teacher', 
    rating: 5, 
    text: 'Gamified learning made complex topics simple. My whole family now uses the platform for financial planning!',
    avatar: 'LR',
    achievement: 'Paid off student loans',
    timeframe: '4 months ago'
  }
];

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [healthStatus, setHealthStatus] = useState(null);
  const [visibleCards, setVisibleCards] = useState([]);
  const [hoveredCard, setHoveredCard] = useState(null);
  const [currentFact, setCurrentFact] = useState(null);
  const [factHistory, setFactHistory] = useState([]);
  const [showDailyInsight, setShowDailyInsight] = useState(true);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isSmallMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const backgroundStyles = useMemo(() => ({
    heroBackground: {
      background: `
        linear-gradient(135deg, rgba(135, 169, 107, 0.15) 0%, rgba(107, 142, 71, 0.2) 100%),
        url("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80")
      `,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
      backgroundAttachment: isMobile ? 'scroll' : 'fixed',
      position: 'relative',
      overflow: 'hidden',
      minHeight: '100vh'
    },
    decorativeElements: {
      '&::before': {
        content: '""',
        position: 'absolute',
        top: 0,
        right: 0,
        width: '400px',
        height: '400px',
        background: 'radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%)',
        borderRadius: '50%',
        transform: 'translate(50%, -50%)',
        pointerEvents: 'none'
      },
      '&::after': {
        content: '""',
        position: 'absolute',
        bottom: 0,
        left: 0,
        width: '300px',
        height: '300px',
        background: 'radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 60%)',
        borderRadius: '50%',
        transform: 'translate(-30%, 30%)',
        pointerEvents: 'none'
      }
    }
  }), [isMobile]);

  const getRandomFact = () => {
    const unusedFacts = FINANCIAL_FACTS.filter(fact => 
      !factHistory.some(historyFact => historyFact.fact === fact.fact)
    );
    
    const availableFacts = unusedFacts.length > 0 ? unusedFacts : FINANCIAL_FACTS;
    const randomIndex = Math.floor(Math.random() * availableFacts.length);
    const newFact = availableFacts[randomIndex];
    
    setFactHistory(prev => [...prev.slice(-4), newFact]); // Keep last 5 facts
    return newFact;
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'Beginner': return '#22c55e';
      case 'Intermediate': return '#f59e0b';
      case 'Advanced': return '#ef4444';
      default: return '#6b7280';
    }
  };

  useEffect(() => {
    const initializeDashboard = async () => {
      await checkApiHealth();
      
      // Set initial random fact
      setCurrentFact(getRandomFact());
      
      // Stagger card animations with more natural timing
      const timer = setTimeout(() => {
        setVisibleCards(Array.from({ length: FEATURES.length }, (_, i) => i));
      }, 400);
      
      return () => clearTimeout(timer);
    };

    initializeDashboard();
  }, []);

  useEffect(() => {
    // Rotate facts every 30 seconds
    const factInterval = setInterval(() => {
      setCurrentFact(getRandomFact());
    }, 30000);

    return () => clearInterval(factInterval);
  }, [factHistory]);

  const checkApiHealth = async () => {
    try {
      await new Promise(resolve => setTimeout(resolve, 1800));
      setHealthStatus({ status: 'healthy', message: 'All systems operational' });
    } catch (error) {
      setHealthStatus({ status: 'error', message: 'Service temporarily unavailable' });
    } finally {
      setLoading(false);
    }
  };

  const handleNextFact = () => {
    setCurrentFact(getRandomFact());
  };

  const handleCloseDailyInsight = () => {
    setShowDailyInsight(false);
  };

  const LoadingScreen = () => (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        background: 'linear-gradient(135deg, rgba(135, 169, 107, 0.3) 0%, rgba(107, 142, 71, 0.4) 100%)',
        color: 'white',
        position: 'relative',
        overflow: 'hidden'
      }}
    >
      {/* Animated background elements */}
      <Box sx={{
        position: 'absolute',
        width: '200px',
        height: '200px',
        borderRadius: '50%',
        background: 'rgba(255,255,255,0.1)',
        top: '20%',
        right: '10%',
        animation: 'float 6s ease-in-out infinite'
      }} />
      <Box sx={{
        position: 'absolute',
        width: '150px',
        height: '150px',
        borderRadius: '50%',
        background: 'rgba(255,255,255,0.08)',
        bottom: '20%',
        left: '15%',
        animation: 'float 8s ease-in-out infinite reverse'
      }} />

      <Box sx={{ position: 'relative', display: 'inline-flex', mb: 4 }}>
        <CircularProgress 
          size={100} 
          thickness={2}
          sx={{ 
            color: 'rgba(255,255,255,0.2)',
            position: 'absolute',
          }} 
        />
        <CircularProgress 
          size={100} 
          thickness={4}
          sx={{ 
            color: 'white',
            animationDuration: '1.5s',
          }} 
        />
        <Box sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
        }}>
          <VerifiedUser sx={{ fontSize: 40, opacity: 0.9 }} />
        </Box>
      </Box>
      
      <Typography variant="h5" sx={{ mb: 2, fontWeight: 600, textAlign: 'center' }}>
        Initializing Secure Platform
      </Typography>
      <Typography variant="body1" sx={{ opacity: 0.8, textAlign: 'center', maxWidth: 400 }}>
        Loading your personalized financial dashboard with enterprise-grade security
      </Typography>
      
      <Box sx={{ mt: 4, display: 'flex', gap: 1 }}>
        {[0, 1, 2].map((i) => (
          <Box
            key={i}
            sx={{
              width: 8,
              height: 8,
              borderRadius: '50%',
              backgroundColor: 'rgba(255,255,255,0.7)',
              animation: `pulse 1.5s ease-in-out ${i * 0.2}s infinite`
            }}
          />
        ))}
      </Box>

      <style jsx>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-20px); }
        }
        @keyframes pulse {
          0%, 100% { opacity: 0.7; transform: scale(1); }
          50% { opacity: 1; transform: scale(1.2); }
        }
      `}</style>
    </Box>
  );

  if (loading) {
    return <LoadingScreen />;
  }

  return (
    <Box 
      sx={{
        minHeight: '100vh',
        position: 'relative',
        '&::before': {
          content: '""',
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          backgroundImage: 'url("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80")',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat',
          zIndex: -2,
          opacity: 1
        },
        '&::after': {
          content: '""',
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          background: 'linear-gradient(135deg, rgba(135, 169, 107, 0.15) 0%, rgba(107, 142, 71, 0.2) 100%)',
          zIndex: -1
        }
      }}
    >
      {/* Enhanced Hero Section */}
      <Box sx={{ ...backgroundStyles.heroBackground, ...backgroundStyles.decorativeElements, py: { xs: 10, md: 15 }, px: 2 }}>
        <Container maxWidth="lg">
          <Fade in timeout={1200}>
            <Box sx={{ textAlign: 'center', color: 'white', position: 'relative', zIndex: 1 }}>
              <Typography
                variant={isSmallMobile ? "h3" : isMobile ? "h2" : "h1"}
                sx={{
                  fontWeight: 800,
                  mb: 3,
                  lineHeight: 1.1,
                  textShadow: '0 4px 20px rgba(0,0,0,0.3)',
                  letterSpacing: '-0.02em'
                }}
              >
                Master Your
                <Box
                  component="span"
                  sx={{
                    background: 'linear-gradient(45deg, #86efac, #bbf7d0, #dcfce7)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    display: 'block',
                    mt: 1,
                    position: 'relative',
                    '&::after': {
                      content: '""',
                      position: 'absolute',
                      bottom: -8,
                      left: '50%',
                      transform: 'translateX(-50%)',
                      width: 120,
                      height: 4,
                      background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent)',
                      borderRadius: 2
                    }
                  }}
                >
                  Financial Future
                </Box>
              </Typography>

              <Typography
                variant={isMobile ? "h6" : "h5"}
                sx={{
                  maxWidth: '750px',
                  mx: 'auto',
                  mb: 6,
                  opacity: 0.95,
                  lineHeight: 1.6,
                  fontWeight: 400,
                  textShadow: '0 2px 10px rgba(0,0,0,0.2)'
                }}
              >
                Transform your relationship with money through secure, AI-powered education. 
                Build wealth confidently with personalized insights and enterprise-grade protection.
              </Typography>

              <Box sx={{ 
                display: 'flex', 
                justifyContent: 'center', 
                gap: 3, 
                flexWrap: 'wrap',
                flexDirection: isSmallMobile ? 'column' : 'row',
                mb: 8
              }}>
                <Button
                  variant="contained"
                  size="large"
                  endIcon={<Timeline />}
                  sx={{
                    background: 'linear-gradient(135deg, rgba(34, 197, 94, 0.9) 0%, rgba(22, 163, 74, 0.9) 100%)',
                    color: 'white',
                    px: 5,
                    py: 2,
                    fontWeight: 700,
                    fontSize: '1.1rem',
                    borderRadius: 3,
                    boxShadow: '0 8px 32px rgba(34, 197, 94, 0.4)',
                    textTransform: 'none',
                    minHeight: 56,
                    backdropFilter: 'blur(10px)',
                    '&:hover': { 
                      transform: 'translateY(-3px)', 
                      boxShadow: '0 16px 48px rgba(34, 197, 94, 0.6)',
                      background: 'linear-gradient(135deg, rgba(22, 163, 74, 0.9) 0%, rgba(21, 128, 61, 0.9) 100%)'
                    },
                    transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                    minWidth: isSmallMobile ? '100%' : 'auto'
                  }}
                  href="/start-journey"
                >
                  Start Learning Journey
                </Button>
              </Box>
            </Box>
          </Fade>
        </Container>
      </Box>

      {/* Daily Financial Insight Section - Integrated seamlessly */}
      {currentFact && showDailyInsight && (
        <Container maxWidth="lg" sx={{ py: 4, mt: -6, position: 'relative', zIndex: 2 }}>
          <Grow in timeout={1500}>
            <Paper
              elevation={8}
              sx={{
                background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.98) 100%)',
                backdropFilter: 'blur(20px)',
                borderRadius: 4,
                p: 3,
                border: '1px solid rgba(135, 169, 107, 0.2)',
                position: 'relative',
                overflow: 'hidden',
                '&::before': {
                  content: '""',
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '4px',
                  background: 'linear-gradient(90deg, #87a96b, #6b8e47, #87a96b)',
                }
              }}
            >
              <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 3 }}>
                <Box sx={{ 
                  background: 'linear-gradient(135deg, #87a96b, #6b8e47)', 
                  borderRadius: 3, 
                  p: 2,
                  minWidth: 60,
                  height: 60,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  boxShadow: '0 4px 12px rgba(135, 169, 107, 0.3)'
                }}>
                  <Lightbulb sx={{ fontSize: 32, color: 'white' }} />
                </Box>
                
                <Box sx={{ flex: 1 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1.5, flexWrap: 'wrap', gap: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flexWrap: 'wrap' }}>
                      <Typography variant="h6" fontWeight="700" color="text.primary">
                        Daily Financial Insight
                      </Typography>
                      <Chip
                        label={currentFact.category}
                        size="small"
                        sx={{ 
                          background: 'rgba(135, 169, 107, 0.1)', 
                          color: '#87a96b', 
                          fontWeight: 600,
                          border: '1px solid rgba(135, 169, 107, 0.3)'
                        }}
                      />
                      <Chip
                        label={currentFact.difficulty}
                        size="small"
                        sx={{ 
                          background: `${getDifficultyColor(currentFact.difficulty)}15`, 
                          color: getDifficultyColor(currentFact.difficulty),
                          fontWeight: 600,
                          border: `1px solid ${getDifficultyColor(currentFact.difficulty)}30`
                        }}
                      />
                    </Box>
                    <IconButton
                      size="small"
                      onClick={handleCloseDailyInsight}
                      sx={{
                        color: '#6b7280',
                        '&:hover': {
                          background: 'rgba(107, 114, 128, 0.1)'
                        }
                      }}
                    >
                      <Close />
                    </IconButton>
                  </Box>
                  
                  <Typography variant="body1" sx={{ 
                    lineHeight: 1.6, 
                    color: 'text.secondary',
                    fontSize: '1.1rem',
                    mb: 2
                  }}>
                    {currentFact.fact}
                  </Typography>
                  
                  <Button
                    variant="outlined"
                    size="small"
                    onClick={handleNextFact}
                    startIcon={<AutoAwesome />}
                    sx={{
                      borderColor: '#87a96b',
                      color: '#87a96b',
                      fontWeight: 600,
                      borderRadius: 2,
                      textTransform: 'none',
                      '&:hover': {
                        background: 'rgba(135, 169, 107, 0.1)',
                        borderColor: '#6b8e47'
                      }
                    }}
                  >
                    Next Insight
                  </Button>
                </Box>
              </Box>
            </Paper>
          </Grow>
        </Container>
      )}

      {/* Enhanced Features Section */}
      <Container maxWidth="lg" sx={{ py: 10 }}>
        <Box sx={{ textAlign: 'center', mb: 10 }}>
          <Chip
            label="Powered by AI"
            sx={{
              background: 'linear-gradient(135deg, rgba(135, 169, 107, 0.9), rgba(107, 142, 71, 0.9))',
              color: 'white',
              fontWeight: 700,
              mb: 3,
              px: 3,
              py: 1,
              backdropFilter: 'blur(10px)'
            }}
            icon={<Analytics />}
          />
          <Typography 
            variant={isMobile ? "h3" : "h2"} 
            fontWeight="800" 
            sx={{ 
              mb: 3, 
              color: 'white',
              textShadow: '0 2px 10px rgba(0,0,0,0.3)',
              letterSpacing: '-0.01em'
            }}
          >
            Intelligent Financial Tools
          </Typography>
          <Typography 
            variant="h6" 
            sx={{ 
              color: 'rgba(255,255,255,0.9)', 
              maxWidth: '700px', 
              mx: 'auto',
              lineHeight: 1.6,
              fontWeight: 400,
              textShadow: '0 1px 5px rgba(0,0,0,0.2)'
            }}
          >
            Experience next-generation financial management with AI-powered insights, 
            advanced security, and personalized learning paths tailored to your goals.
          </Typography>
        </Box>

        <Grid container spacing={4}>
          {FEATURES.map((feature, index) => {
            const IconComponent = feature.icon;
            const isHovered = hoveredCard === index;
            
            return (
              <Grid item xs={12} sm={6} lg={4} key={index}>
                <Grow in={visibleCards.includes(index)} timeout={800 + index * 150}>
                  <Card
                    onMouseEnter={() => setHoveredCard(index)}
                    onMouseLeave={() => setHoveredCard(null)}
                    sx={{
                      height: '100%',
                      display: 'flex',
                      flexDirection: 'column',
                      borderRadius: 5,
                      overflow: 'hidden',
                      transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                      background: 'rgba(255, 255, 255, 0.1)',
                      backdropFilter: 'blur(20px)',
                      boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
                      border: '1px solid rgba(255,255,255,0.2)',
                      position: 'relative',
                      '&:hover': { 
                        transform: 'translateY(-16px) scale(1.02)', 
                        boxShadow: '0 32px 80px rgba(0,0,0,0.2)',
                        background: 'rgba(255, 255, 255, 0.15)',
                        '& .feature-badge': {
                          transform: 'scale(1.1)'
                        },
                        '& .feature-icon': {
                          transform: 'scale(1.1) rotate(5deg)'
                        }
                      }
                    }}
                  >
                    <Box sx={{ 
                      background: feature.gradient, 
                      p: 4, 
                      color: 'white',
                      position: 'relative',
                      overflow: 'hidden',
                      '&::before': {
                        content: '""',
                        position: 'absolute',
                        top: 0,
                        right: 0,
                        width: '100px',
                        height: '100px',
                        background: 'radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 60%)',
                        borderRadius: '50%',
                        transform: 'translate(40px, -40px)'
                      }
                    }}>
                      <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', mb: 3 }}>
                        <Avatar 
                          className="feature-icon"
                          sx={{ 
                            background: 'rgba(255,255,255,0.2)', 
                            width: 70, 
                            height: 70,
                            backdropFilter: 'blur(20px)',
                            border: '2px solid rgba(255,255,255,0.3)',
                            transition: 'all 0.3s ease'
                          }}
                        >
                          <IconComponent sx={{ fontSize: 36 }} />
                        </Avatar>
                        <Chip
                          className="feature-badge"
                          label={feature.badge}
                          size="small"
                          sx={{ 
                            background: 'rgba(255,255,255,0.25)', 
                            color: 'white', 
                            fontWeight: 700,
                            backdropFilter: 'blur(20px)',
                            border: '1px solid rgba(255,255,255,0.3)',
                            transition: 'all 0.3s ease'
                          }}
                        />
                      </Box>
                      
                      <Typography variant="h5" fontWeight="700" sx={{ mb: 2, lineHeight: 1.3 }}>
                        {feature.title}
                      </Typography>
                    </Box>
                    
                    <CardContent sx={{ p: 4, flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
                      <Typography 
                        variant="body1" 
                        sx={{ 
                          mb: 3, 
                          lineHeight: 1.7, 
                          color: 'rgba(255,255,255,0.9)', 
                          flexGrow: 1,
                          fontSize: '0.95rem'
                        }}
                      >
                        {feature.description}
                      </Typography>
                      
                      {/* Feature highlights */}
                      <Box sx={{ mb: 3 }}>
                        {feature.features.map((item, idx) => (
                          <Box key={idx} sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                            <CheckCircle sx={{ fontSize: 16, color: feature.accent }} />
                            <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)', fontWeight: 500 }}>
                              {item}
                            </Typography>
                          </Box>
                        ))}
                      </Box>
                      
                      <Button
                        variant="outlined"
                        size="large"
                        endIcon={<ArrowForward />}
                        sx={{ 
                          alignSelf: 'flex-start',
                          borderColor: 'rgba(255,255,255,0.5)',
                          color: 'white',
                          fontWeight: 700,
                          borderRadius: 3,
                          px: 3,
                          py: 1.5,
                          borderWidth: 2,
                          textTransform: 'none',
                          backdropFilter: 'blur(10px)',
                          '&:hover': { 
                            backgroundColor: 'rgba(255,255,255,0.1)',
                            color: 'white',
                            transform: 'translateX(4px)',
                            borderColor: 'white'
                          },
                          transition: 'all 0.3s ease'
                        }}
                        href={feature.path}
                      >
                        Explore Tool
                      </Button>
                    </CardContent>
                  </Card>
                </Grow>
              </Grid>
            );
          })}
        </Grid>
      </Container>

      <style jsx global>{`
        @keyframes float {
          0%, 100% { 
            transform: translateY(0px) rotate(0deg); 
          }
          50% { 
            transform: translateY(-20px) rotate(2deg); 
          }
        }
        @keyframes pulse {
          0%, 100% { 
            opacity: 0.7; 
            transform: scale(1); 
          }
          50% { 
            opacity: 1; 
            transform: scale(1.2); 
          }
        }
        @keyframes slideInUp {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </Box>
  );
};

export default Dashboard;