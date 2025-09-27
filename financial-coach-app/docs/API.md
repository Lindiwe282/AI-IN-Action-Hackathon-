# API Documentation

## Base URL
- Development: `http://localhost:5000/api`
- Production: `https://api.financialcoach.com/api`

## Authentication
Currently, the API does not require authentication. Future versions will implement JWT-based authentication.

## Common Response Format
```json
{
  "success": true,
  "data": {},
  "message": "Success message",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Error Response Format
```json
{
  "error": "Error type",
  "message": "Detailed error message",
  "details": [],
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Endpoints

### Health Check

#### GET /
Basic health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "Financial Coach API is running!",
  "version": "1.0.0"
}
```

#### GET /api/health
Detailed health status.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "services": ["planner", "investment", "loan", "literacy", "fraud"]
}
```

### Financial Planning

#### POST /api/planner/create
Create a new financial plan.

**Request Body:**
```json
{
  "monthly_income": 5000,
  "monthly_expenses": 3500,
  "current_savings": 10000,
  "total_debt": 15000,
  "age": 30,
  "dependents": 1,
  "risk_tolerance": "medium",
  "financial_goals": ["retirement", "house"]
}
```

**Response:**
```json
{
  "success": true,
  "plan": {
    "user_id": 1,
    "budget_allocation": {
      "needs": 2500,
      "wants": 1500,
      "savings": 1000,
      "percentages": {
        "needs": 50,
        "wants": 30,
        "savings": 20
      }
    },
    "savings_goals": [...],
    "recommendations": [...],
    "risk_assessment": {...},
    "timeline": [...],
    "emergency_fund": {...}
  }
}
```

#### GET /api/planner/recommendations/{user_id}
Get recommendations for a specific user.

**Response:**
```json
{
  "recommendations": [
    {
      "type": "investment",
      "message": "Consider increasing investment allocation",
      "priority": "medium"
    }
  ]
}
```

### Investment Advisory

#### POST /api/investment/suggestions
Get investment suggestions based on user profile.

**Request Body:**
```json
{
  "investment_amount": 10000,
  "age": 30,
  "risk_tolerance": "medium",
  "investment_timeline": 10,
  "investment_experience": "beginner",
  "monthly_income": 5000
}
```

**Response:**
```json
{
  "success": true,
  "suggestions": {
    "risk_profile": {...},
    "portfolio_allocation": {...},
    "specific_recommendations": [...],
    "expected_returns": {...},
    "investment_timeline": [...]
  }
}
```

### Loan Analysis

#### POST /api/loan/affordability
Check loan affordability.

**Request Body:**
```json
{
  "monthly_income": 5000,
  "loan_amount": 200000,
  "interest_rate": 6.5,
  "loan_term_months": 360,
  "monthly_debt_payments": 500,
  "credit_score": 750,
  "employment_years": 5
}
```

**Response:**
```json
{
  "loan_amount": 200000,
  "monthly_payment": 1264.14,
  "debt_to_income_ratio": 0.35,
  "affordability_score": 85,
  "approval_likelihood": "High",
  "recommendations": [...],
  "risk_factors": [...]
}
```

### Fraud Detection

#### POST /api/fraud/detect
Detect potential fraud in a transaction.

**Request Body:**
```json
{
  "amount": 1500,
  "hour": 23,
  "merchant_category": "online",
  "location": "unknown"
}
```

**Response:**
```json
{
  "success": true,
  "fraud_detection": {
    "is_fraud": false,
    "fraud_probability": 0.35,
    "risk_level": "Medium",
    "risk_factors": [...],
    "recommendations": [...]
  }
}
```

## Status Codes

- `200` - Success
- `400` - Bad Request (validation errors)
- `404` - Not Found
- `500` - Internal Server Error

## Rate Limiting

- Development: No rate limiting
- Production: 100 requests per minute per IP

## Data Validation

All endpoints validate input data. Common validation rules:
- Monetary amounts must be non-negative
- Age must be between 16-100
- Percentages must be 0-100
- Required fields must be present