# ZeTheta FinArcade API Documentation

Complete API endpoint documentation with request/response examples.

## Base URL

```
http://localhost:5000/api
```

## Authentication

All endpoints (except `/api/auth/register` and `/api/auth/login`) require JWT authentication.

Include the JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## Endpoints

### Authentication Endpoints

#### POST /api/auth/register
Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "9876543210"
}
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "9876543210",
    "is_verified": false,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### POST /api/auth/login
Login with email and password.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "user": { ... },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### POST /api/auth/logout
Logout and blacklist token.

**Response (200):**
```json
{
  "message": "Logged out successfully"
}
```

#### GET /api/auth/profile
Get current user profile.

**Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "9876543210",
  "is_verified": false,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

#### PUT /api/auth/profile
Update user profile.

**Request Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "phone": "9876543211"
}
```

### Risk Profiling Endpoints

#### POST /api/risk-profiling/questionnaire
Submit questionnaire answers for Q-Score calculation.

**Request Body:**
```json
{
  "answers": {
    "question_1": 3,
    "question_2": 4,
    "question_3": 2,
    ...
  }
}
```

**Response (200):**
```json
{
  "q_score": 65.5,
  "risk_score": null,
  "message": "Questionnaire submitted successfully"
}
```

#### POST /api/risk-profiling/demographics
Submit demographic data for cultural modifiers.

**Request Body:**
```json
{
  "region": "north",
  "age": 35,
  "income": 750000,
  "occupation": "engineer",
  "joint_family_status": true,
  "language_preference": "hindi",
  "religious_event_participation": 0.7,
  "festival_spending": 50000,
  "gold_investment_ratio": 0.15,
  "real_estate_allocation": 0.40
}
```

**Response (200):**
```json
{
  "base_modifier": 1.0,
  "regional_factor": 0.95,
  "demographic_factor": 1.0,
  "tradition_factor": 0.98,
  "cultural_modifier": 0.931
}
```

#### POST /api/risk-profiling/calculate
Calculate comprehensive risk profile.

**Response (200):**
```json
{
  "risk_score": 62.5,
  "risk_category": "moderate",
  "confidence": 0.85,
  "factors": {
    "q_score": 65.0,
    "g_score": 60.0,
    "b_score": 55.0,
    "cultural_modifier": 0.931,
    "base_score": 60.75
  }
}
```

### Portfolio Management Endpoints

#### GET /api/portfolio/:user_id
Get user's portfolio with holdings.

**Response (200):**
```json
{
  "portfolio": {
    "id": 1,
    "user_id": 1,
    "total_value": 1000000.00,
    "total_gain_loss": 50000.00,
    "total_gain_loss_percent": 5.25,
    "last_updated": "2024-01-01T00:00:00",
    "holdings_count": 5
  },
  "holdings": [
    {
      "id": 1,
      "asset_type": "equity",
      "asset_name": "RELIANCE",
      "quantity": 100.0,
      "current_price": 2500.00,
      "purchase_price": 2400.00,
      "allocation": 25.0,
      "current_value": 250000.00,
      "gain_loss": 10000.00,
      "gain_loss_percent": 4.17
    }
  ],
  "performance": {
    "total_value": 1000000.00,
    "total_cost": 950000.00,
    "total_gain_loss": 50000.00,
    "total_gain_loss_percent": 5.26
  }
}
```

#### POST /api/portfolio/optimize
Optimize portfolio allocation.

**Request Body:**
```json
{
  "user_id": 1,
  "risk_category": "moderate",
  "investment_amount": 500000,
  "goals": [
    {
      "goal_name": "Retirement",
      "years_to_goal": 20,
      "target_amount": 5000000
    }
  ]
}
```

**Response (200):**
```json
{
  "allocation": {
    "equity": 0.50,
    "debt": 0.30,
    "gold": 0.10,
    "international": 0.10
  },
  "expected_return": 0.095,
  "risk_metrics": {
    "volatility": 0.20,
    "sharpe_ratio": 0.633,
    "max_drawdown": 0.15
  },
  "behavioral_adjustments": {
    "equity_reduction": 0.0,
    "debt_increase": 0.0
  },
  "investment_amount": 500000.0
}
```

### Market Data Endpoints

#### GET /api/market/indices
Get current market indices.

**Response (200):**
```json
{
  "nifty_50": {
    "value": 24500.50,
    "change": 125.30,
    "change_percent": 0.51,
    "timestamp": "2024-01-01T00:00:00"
  },
  "sensex": {
    "value": 80500.75,
    "change": 450.20,
    "change_percent": 0.56,
    "timestamp": "2024-01-01T00:00:00"
  },
  "nifty_bank": {
    "value": 52000.25,
    "change": 280.50,
    "change_percent": 0.54,
    "timestamp": "2024-01-01T00:00:00"
  }
}
```

#### GET /api/market/sentiment
Get aggregated market sentiment.

**Response (200):**
```json
{
  "overall_sentiment": "positive",
  "confidence": 0.75,
  "news_count": 150,
  "daily_sentiment_score": 0.45
}
```

#### GET /api/market/predictions/:symbol
Get market predictions for a symbol.

**Response (200):**
```json
{
  "symbol": "RELIANCE",
  "expected_return": 0.12,
  "volatility": 0.20,
  "prediction_confidence": 0.75,
  "time_horizon_days": 30,
  "technical_indicators": {
    "rsi": 55.5,
    "macd": 2.3,
    "sma_50": 24500.0,
    "sma_200": 24000.0
  }
}
```

### Behavioral Analytics Endpoints

#### GET /api/behavioral/metrics/:user_id
Get user behavioral metrics.

**Response (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "portfolio_check_frequency": 3,
  "portfolio_turnover_rate": 0.25,
  "trade_volume_last_week": 50000.00,
  "major_life_event_occurred": false,
  "sentiment_avg": 0.65,
  "sentiment_variance": 0.15,
  "email_tone_positive_ratio": 0.70,
  "calendar_stress_events_count": 2,
  "nudge_acceptance_rate": 0.80,
  "reaction_to_market_volatility": "moderate"
}
```

#### GET /api/behavioral/insights/:user_id
Get behavioral insights and recommendations.

**Response (200):**
```json
{
  "insights": [
    {
      "type": "info",
      "message": "Your portfolio check frequency is optimal.",
      "severity": "low"
    }
  ],
  "recommendations": [
    {
      "action": "maintain_current_strategy",
      "reason": "Behavioral metrics indicate stable investment behavior",
      "priority": "low"
    }
  ],
  "risk_adjustments": {}
}
```

### Goals & Planning Endpoints

#### POST /api/goals/create
Create a new goal.

**Request Body:**
```json
{
  "user_id": 1,
  "goal_name": "Retirement Fund",
  "target_amount": 5000000,
  "target_date": "2044-01-01",
  "goal_type": "retirement",
  "priority": "high"
}
```

#### GET /api/goals/progress/:user_id
Get goal progress with Monte Carlo simulations.

**Response (200):**
```json
{
  "goals": [
    {
      "id": 1,
      "goal_name": "Retirement Fund",
      "target_amount": 5000000.00,
      "current_amount": 500000.00,
      "progress_percent": 10.0,
      "achievement_probability": 0.85
    }
  ],
  "achievement_probability": 0.85,
  "recommended_allocations": {
    "equity": 0.50,
    "debt": 0.30,
    "gold": 0.10,
    "international": 0.10
  }
}
```

### AI Insights Endpoints

#### POST /api/ai/recommendations
Get personalized investment recommendations.

**Request Body:**
```json
{
  "user_id": 1
}
```

**Response (200):**
```json
{
  "recommendations": [
    {
      "type": "portfolio_diversification",
      "title": "Consider Diversifying Your Portfolio",
      "content": "Your portfolio could benefit from better diversification...",
      "confidence": 0.75,
      "priority": "medium",
      "action_items": [
        "Consider adding international equities",
        "Review debt allocation"
      ]
    }
  ],
  "confidence_scores": {
    "portfolio_analysis": 0.80,
    "market_analysis": 0.70,
    "behavioral_analysis": 0.75
  },
  "reasoning": {
    "portfolio_factor": "Based on current portfolio composition",
    "market_factor": "Based on current market conditions",
    "behavioral_factor": "Based on user behavioral patterns"
  }
}
```

## Error Responses

All endpoints may return the following error responses:

**400 Bad Request:**
```json
{
  "error": "Missing required field: email"
}
```

**401 Unauthorized:**
```json
{
  "error": "Token is missing or invalid"
}
```

**403 Forbidden:**
```json
{
  "error": "Unauthorized"
}
```

**404 Not Found:**
```json
{
  "error": "User not found"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Internal server error"
}
```

## Rate Limiting

API endpoints are rate-limited to prevent abuse. Default limits:
- Authentication endpoints: 5 requests per minute
- Other endpoints: 100 requests per minute

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1609459200
```

## Pagination

List endpoints support pagination via query parameters:
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)

Example:
```
GET /api/transactions/1?page=2&per_page=10
```

## Filtering

Some endpoints support filtering via query parameters:
- `type`: Filter by type
- `status`: Filter by status
- `date`: Filter by date

Example:
```
GET /api/transactions/1?type=buy&status=completed
```

