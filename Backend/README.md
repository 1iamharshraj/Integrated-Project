# ZeTheta FinArcade - Flask REST API Backend

India's first fully autonomous AI-driven investment advisory platform. This backend combines features from Project 25 and Project 29, providing comprehensive investment advisory services with AI-powered insights, risk profiling, portfolio management, and behavioral analytics.

## Features

### Core Functionality

- **User Authentication & Authorization** - JWT-based authentication with secure password hashing
- **Risk Profiling** - Comprehensive risk assessment combining:
  - Q-Score (40%) - Questionnaire-based risk tolerance
  - G-Score (35%) - Goal-based risk assessment
  - B-Score (25%) - Behavioral risk assessment
  - Cultural Modifiers - Regional, demographic, and traditional factors
- **Portfolio Management** - Modern Portfolio Theory-based optimization with behavioral constraints
- **Market Data & Predictions** - Real-time market data, technical indicators, and AI-powered predictions
- **Behavioral Analytics** - User behavior tracking and insights
- **AI Insights** - Personalized investment recommendations using CatBoost and RoBERTa models
- **Goals Planning** - Financial goals tracking with Monte Carlo simulations
- **KYC Management** - Document upload and verification
- **Sentiment Analysis** - FinBERT-based news sentiment analysis
- **Education Progress** - Track user's financial education journey

## Technology Stack

- **Framework**: Flask 2.3+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Flask-JWT-Extended
- **Caching**: Redis (optional)
- **Background Tasks**: Celery (optional)
- **Validation**: Marshmallow
- **AI/ML**: Transformers, PyTorch, scikit-learn

## Project Structure

```
Backend/
├── app.py                 # Main application entry point
├── config.py              # Configuration settings
├── extensions.py          # Flask extensions initialization
├── requirements.txt       # Python dependencies
├── models/                # Database models
│   ├── user.py
│   ├── risk_profile.py
│   ├── portfolio.py
│   ├── behavioral_metrics.py
│   └── ...
├── api/                   # API endpoints (blueprints)
│   ├── auth.py
│   ├── risk_profiling.py
│   ├── portfolio.py
│   ├── market.py
│   ├── behavioral.py
│   ├── goals.py
│   ├── ai_insights.py
│   ├── kyc.py
│   ├── transactions.py
│   ├── education.py
│   └── news.py
├── services/              # Business logic services
│   ├── risk_profiling_service.py
│   ├── portfolio_service.py
│   ├── market_service.py
│   ├── behavioral_service.py
│   ├── ai_service.py
│   └── sentiment_service.py
└── utils/                 # Utility functions
    ├── auth.py
    ├── cache.py
    ├── validators.py
    └── errors.py
```

## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Redis (optional, for caching)
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository and navigate to the backend directory**

```bash
cd "Integrated Projects/Backend"
```

2. **Create and activate virtual environment**

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**

**Core dependencies (required):**
```bash
pip install -r requirements.txt
```

**AI/ML dependencies (optional - for model integration):**
```bash
# Note: On Windows, sentencepiece may have installation issues
# See INSTALLATION_WINDOWS.md for troubleshooting
pip install -r requirements-ai.txt
```

**Windows Users**: If you encounter installation errors (especially with `sentencepiece`), see `INSTALLATION_WINDOWS.md` for detailed troubleshooting steps.

4. **Set up environment variables**

A `.env` file has been created with the Supabase database connection. You need to generate and add security keys:

**Generate Secret Keys:**
```bash
python generate_secrets.py
```

This will generate secure random keys. Copy the output and add them to your `.env` file:

```env
SECRET_KEY=<generated-secret-key>
JWT_SECRET_KEY=<generated-jwt-secret-key>
DATABASE_URL=postgresql://postgres:ZeThetha#$1@db.bzwpbznefkiypvsbcoio.supabase.co:5432/postgres
REDIS_URL=redis://localhost:6379/0
FLASK_ENV=development
```

**What are these keys?**
- **SECRET_KEY**: Used by Flask for session management and CSRF protection
- **JWT_SECRET_KEY**: Used to sign and verify JWT tokens for authentication

**Important Security Notes:**
- These keys are randomly generated - never share them publicly
- Use different keys for development and production environments
- If keys are compromised, regenerate them immediately
- The `.env` file is already in `.gitignore` to prevent accidental commits

5. **Initialize the database**

The database connection is already configured to use Supabase PostgreSQL. You can initialize the database tables using one of these methods:

**Option 1: Using Flask-Migrate (Recommended)**
```bash
# Initialize migrations (first time only)
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migration to Supabase database
flask db upgrade
```

**Option 2: Using setup script (Quick start)**
```bash
python setup.py
```

This will create all database tables directly using SQLAlchemy. Note: Flask-Migrate is recommended for production as it provides version control for database schema changes.

6. **Run the application**

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile
- `POST /api/auth/refresh` - Refresh access token

### Risk Profiling

- `POST /api/risk-profiling/questionnaire` - Submit questionnaire (Q-Score)
- `POST /api/risk-profiling/demographics` - Submit demographics (Cultural modifiers)
- `POST /api/risk-profiling/life-events` - Submit life events
- `POST /api/risk-profiling/behavioral` - Submit behavioral data (B-Score)
- `POST /api/risk-profiling/calculate` - Calculate comprehensive risk profile
- `GET /api/risk-profiling/profile/:user_id` - Get user's risk profile

### Portfolio Management

- `GET /api/portfolio/:user_id` - Get user's portfolio
- `POST /api/portfolio/optimize` - Optimize portfolio allocation
- `POST /api/portfolio/rebalance` - Rebalance portfolio
- `GET /api/portfolio/performance/:user_id` - Get portfolio performance
- `POST /api/portfolio/holdings` - Add/update holding
- `DELETE /api/portfolio/holdings/:holding_id` - Remove holding

### Market Data

- `GET /api/market/indices` - Get market indices
- `GET /api/market/sentiment` - Get market sentiment
- `GET /api/market/predictions/:symbol` - Get market predictions
- `GET /api/market/news` - Get financial news
- `GET /api/market/technical-indicators/:symbol` - Get technical indicators

### Behavioral Analytics

- `GET /api/behavioral/metrics/:user_id` - Get behavioral metrics
- `POST /api/behavioral/update` - Update behavioral metrics
- `GET /api/behavioral/insights/:user_id` - Get behavioral insights

### Goals & Planning

- `GET /api/goals/:user_id` - Get user's goals
- `POST /api/goals/create` - Create a goal
- `PUT /api/goals/:goal_id` - Update goal
- `DELETE /api/goals/:goal_id` - Delete goal
- `GET /api/goals/progress/:user_id` - Get goal progress

### AI Insights

- `GET /api/ai/insights/:user_id` - Get AI insights
- `POST /api/ai/recommendations` - Get personalized recommendations
- `GET /api/ai/predictions/:symbol` - Get AI predictions
- `POST /api/ai/insights/mark-read/:insight_id` - Mark insight as read

### KYC

- `GET /api/kyc/:user_id` - Get KYC documents
- `POST /api/kyc` - Upload KYC document
- `PUT /api/kyc/:document_id/verify` - Update KYC document status

### Transactions

- `GET /api/transactions/:user_id` - Get transaction history
- `POST /api/transactions` - Create transaction
- `PUT /api/transactions/:transaction_id/status` - Update transaction status

### Education

- `GET /api/education/:user_id` - Get education progress
- `POST /api/education/progress` - Update education progress

### News & Sentiment

- `POST /api/news/scrape` - Scrape news from Moneycontrol.com
- `GET /api/news/sentiment` - Get sentiment analysis results

## Database Schema

### Key Tables

1. **users** - User accounts and profiles
2. **risk_profiles** - Risk profiling data with Q-Score, G-Score, B-Score
3. **portfolios** - User portfolios
4. **holdings** - Portfolio holdings
5. **behavioral_metrics** - Behavioral analytics data
6. **market_features** - Market technical indicators and features
7. **goals** - Financial goals
8. **ai_insights** - AI-generated insights
9. **sentiment_analysis** - News sentiment analysis results
10. **transactions** - Transaction history
11. **kyc_documents** - KYC documents
12. **education_progress** - Education tracking

See individual model files in `models/` directory for detailed schema.

## AI Model Integration

### Risk Profiling Model

- **Ensemble Approach**: Q-Score (40%) + G-Score (35%) + B-Score (25%)
- **Cultural Modifiers**: Base_modifier × Regional_factor × Demographic_factor × Tradition_factor
- Returns comprehensive risk profile with confidence scores

### Portfolio Optimization

- **Modern Portfolio Theory** implementation
- Sharpe ratio maximization
- Behavioral constraints from Project 29
- Goal-based optimization (multi-objective)

### Market Prediction

- **LSTM/ARIMA models** from Project 25
- **Sentiment analysis** (FinBERT) as predictive feature
- **80+ technical indicators** from Project 29
- Predicts expected returns and volatility

### Behavioral Analysis

- Portfolio check frequency analysis
- Turnover rate calculations
- Life events correlation
- Sentiment variance analysis

### Investment Decision Model

- **CatBoost model** for binary classification (investable assets)
- **RoBERTa** for sentiment analysis
- Risk-return optimization
- Market condition adaptation

## Caching Strategy

- **Portfolio data**: 5 minutes TTL
- **Market data**: 1 minute TTL
- **Risk profiles**: 1 hour TTL
- Uses Redis if available, falls back to in-memory cache

## Security

- JWT-based authentication
- Password hashing with bcrypt
- Rate limiting on API endpoints
- Input validation and sanitization
- CORS configuration
- Token blacklisting for logout

## Performance Requirements

- API response time: < 2 seconds
- Portfolio optimization: < 5 seconds
- Support 1,000+ concurrent users
- Database query optimization with indexes

## Compliance (SEBI & DPDP Act 2023)

- Log all investment advice for audit trails
- Risk disclosure requirements
- Data encryption for sensitive information
- Consent management for data processing
- Anonymization for analytics

## Testing

Run tests with:

```bash
pytest
```

With coverage:

```bash
pytest --cov=. --cov-report=html
```

## Development

### Running in Development Mode

```bash
export FLASK_ENV=development
python app.py
```

### Database Migrations

```bash
# Create migration
flask db migrate -m "Description"

# Apply migration
flask db upgrade

# Rollback migration
flask db downgrade
```

## Production Deployment

1. Set environment variables in production
2. Use a production WSGI server (e.g., Gunicorn)
3. Configure PostgreSQL with proper credentials
4. Set up Redis for caching
5. Enable HTTPS
6. Configure proper logging
7. Set up monitoring and alerting

### Example Gunicorn Command

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

## API Documentation

API documentation can be accessed via Swagger UI (if configured) or refer to the endpoint documentation above.

## Contributing

1. Follow PEP 8 style guidelines
2. Write tests for new features
3. Update documentation
4. Submit pull requests

## License

Proprietary - ZeTheta FinArcade

## Support

For issues and questions, contact the development team.

