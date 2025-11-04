# Postman Testing Guide - ZeTheta FinArcade API

Complete guide to test all API endpoints using Postman.

## Prerequisites

1. **Postman installed**: Download from [postman.com](https://www.postman.com/downloads/)
2. **Backend running**: Start the Flask server:
   ```bash
   cd "Integrated Projects\Backend"
   venv\Scripts\activate
   python app.py
   ```
3. **Database initialized**: Run `python setup.py` if not done already

## Setup Postman Environment

### Step 1: Import Collection

1. Open Postman
2. Click **Import** button
3. Select `Postman_Collection.json` from the backend directory
4. Collection will be imported with all endpoints

### Step 2: Create Environment Variables

1. Click **Environments** in left sidebar
2. Click **+** to create new environment
3. Name it: `ZeTheta FinArcade Local`
4. Add these variables:

| Variable | Initial Value | Current Value |
|----------|---------------|---------------|
| `base_url` | `http://localhost:5000` | `http://localhost:5000` |
| `access_token` | (leave empty) | (auto-filled after login) |
| `refresh_token` | (leave empty) | (auto-filled after login) |
| `user_id` | `1` | (auto-filled after login) |

5. Click **Save**
6. Select this environment from dropdown (top right)

## Testing Flow

### Phase 1: Authentication (Required First)

#### 1. Register a New User
- **Endpoint**: `POST /api/auth/register`
- **Body**: Update email/password in request body
- **Expected**: 201 Created with user data and tokens
- **Action**: Copy `access_token` and `user_id` from response

#### 2. Login (Alternative to Register)
- **Endpoint**: `POST /api/auth/login`
- **Body**: Use same email/password
- **Expected**: 200 OK with tokens
- **Auto-action**: Tokens automatically saved to environment (via test script)

#### 3. Get Profile
- **Endpoint**: `GET /api/auth/profile`
- **Headers**: Authorization auto-added from `{{access_token}}`
- **Expected**: 200 OK with user profile

#### 4. Update Profile
- **Endpoint**: `PUT /api/auth/profile`
- **Body**: Update first_name, last_name, phone
- **Expected**: 200 OK

#### 5. Refresh Token
- **Endpoint**: `POST /api/auth/refresh`
- **Headers**: Uses `{{refresh_token}}`
- **Expected**: 200 OK with new access_token

#### 6. Logout
- **Endpoint**: `POST /api/auth/logout`
- **Expected**: 200 OK (token blacklisted)

---

### Phase 2: Risk Profiling

**Prerequisites**: Must be logged in (have valid `access_token`)

#### 1. Submit Questionnaire
- **Endpoint**: `POST /api/risk-profiling/questionnaire`
- **Body**: Update answers object with questionnaire responses
- **Expected**: 200 OK with Q-Score

#### 2. Submit Demographics
- **Endpoint**: `POST /api/risk-profiling/demographics`
- **Body**: Update with demographic data
- **Expected**: 200 OK with cultural modifiers

#### 3. Submit Life Events
- **Endpoint**: `POST /api/risk-profiling/life-events`
- **Body**: Update life_events array
- **Expected**: 200 OK with impact assessment

#### 4. Submit Behavioral Data
- **Endpoint**: `POST /api/risk-profiling/behavioral`
- **Body**: Update behavioral_data object
- **Expected**: 200 OK with B-Score

#### 5. Calculate Comprehensive Risk Profile
- **Endpoint**: `POST /api/risk-profiling/calculate`
- **Expected**: 200 OK with complete risk profile
- **Note**: Combines Q-Score (40%), G-Score (35%), B-Score (25%) + cultural modifiers

#### 6. Get Risk Profile
- **Endpoint**: `GET /api/risk-profiling/profile/{{user_id}}`
- **Expected**: 200 OK with risk profile data

---

### Phase 3: Portfolio Management

#### 1. Get Portfolio
- **Endpoint**: `GET /api/portfolio/{{user_id}}`
- **Expected**: 200 OK with portfolio and holdings (empty if new user)

#### 2. Optimize Portfolio
- **Endpoint**: `POST /api/portfolio/optimize`
- **Body**: Update risk_category, investment_amount, goals
- **Expected**: 200 OK with optimized allocation

#### 3. Add Holding
- **Endpoint**: `POST /api/portfolio/holdings`
- **Body**: Update with holding details (portfolio_id, asset_name, etc.)
- **Expected**: 200 OK with created holding
- **Note**: Get portfolio_id from previous Get Portfolio response

#### 4. Get Portfolio Performance
- **Endpoint**: `GET /api/portfolio/performance/{{user_id}}`
- **Expected**: 200 OK with performance metrics

#### 5. Rebalance Portfolio
- **Endpoint**: `POST /api/portfolio/rebalance`
- **Body**: Update target_allocation
- **Expected**: 200 OK with rebalancing recommendations

#### 6. Delete Holding
- **Endpoint**: `DELETE /api/portfolio/holdings/{holding_id}`
- **Expected**: 200 OK
- **Note**: Update holding_id in URL (use ID from Get Portfolio response)

---

### Phase 4: Market Data

#### 1. Get Market Indices
- **Endpoint**: `GET /api/market/indices`
- **Expected**: 200 OK with NIFTY 50, SENSEX, NIFTY BANK data

#### 2. Get Market Sentiment
- **Endpoint**: `GET /api/market/sentiment`
- **Expected**: 200 OK with aggregated sentiment

#### 3. Get Market Predictions
- **Endpoint**: `GET /api/market/predictions/{symbol}`
- **URL**: Update symbol (e.g., RELIANCE, TCS, INFY)
- **Expected**: 200 OK with predictions and technical indicators

#### 4. Get Financial News
- **Endpoint**: `GET /api/market/news?limit=20`
- **Query Params**: Adjust limit as needed
- **Expected**: 200 OK with news articles

#### 5. Get Technical Indicators
- **Endpoint**: `GET /api/market/technical-indicators/{symbol}`
- **URL**: Update symbol
- **Expected**: 200 OK with 80+ technical indicators

---

### Phase 5: Behavioral Analytics

#### 1. Get Behavioral Metrics
- **Endpoint**: `GET /api/behavioral/metrics/{{user_id}}`
- **Expected**: 200 OK with behavioral metrics (defaults if new user)

#### 2. Update Behavioral Metrics
- **Endpoint**: `POST /api/behavioral/update`
- **Body**: Update all behavioral fields
- **Expected**: 200 OK with updated metrics

#### 3. Get Behavioral Insights
- **Endpoint**: `GET /api/behavioral/insights/{{user_id}}`
- **Expected**: 200 OK with insights and recommendations

---

### Phase 6: Goals & Planning

#### 1. Get Goals
- **Endpoint**: `GET /api/goals/{{user_id}}`
- **Expected**: 200 OK with user's goals (empty array if new)

#### 2. Create Goal
- **Endpoint**: `POST /api/goals/create`
- **Body**: Update goal details
- **Expected**: 201 Created with goal data

#### 3. Get Goal Progress
- **Endpoint**: `GET /api/goals/progress/{{user_id}}`
- **Expected**: 200 OK with progress and Monte Carlo simulations

#### 4. Update Goal
- **Endpoint**: `PUT /api/goals/{goal_id}`
- **URL**: Update goal_id from Create Goal response
- **Body**: Update goal fields
- **Expected**: 200 OK

#### 5. Delete Goal
- **Endpoint**: `DELETE /api/goals/{goal_id}`
- **URL**: Update goal_id
- **Expected**: 200 OK

---

### Phase 7: AI Insights

#### 1. Get AI Insights
- **Endpoint**: `GET /api/ai/insights/{{user_id}}?unread_only=false&limit=20`
- **Query Params**: Adjust as needed
- **Expected**: 200 OK with AI-generated insights

#### 2. Get Recommendations
- **Endpoint**: `POST /api/ai/recommendations`
- **Body**: Update user_id
- **Expected**: 200 OK with personalized recommendations

#### 3. Get AI Predictions
- **Endpoint**: `GET /api/ai/predictions/{symbol}`
- **URL**: Update symbol
- **Expected**: 200 OK with AI predictions

#### 4. Mark Insight as Read
- **Endpoint**: `POST /api/ai/insights/mark-read/{insight_id}`
- **URL**: Update insight_id from Get AI Insights response
- **Expected**: 200 OK

---

### Phase 8: KYC Management

#### 1. Get KYC Documents
- **Endpoint**: `GET /api/kyc/{{user_id}}`
- **Expected**: 200 OK with documents (empty if new user)

#### 2. Upload KYC Document
- **Endpoint**: `POST /api/kyc`
- **Body**: Update document_type (aadhaar/pan/bank_statement) and document_url
- **Expected**: 201 Created with document data

#### 3. Verify KYC Document
- **Endpoint**: `PUT /api/kyc/{document_id}/verify`
- **URL**: Update document_id from Upload response
- **Body**: Update status (pending/verified/rejected)
- **Expected**: 200 OK

---

### Phase 9: Transactions

#### 1. Get Transactions
- **Endpoint**: `GET /api/transactions/{{user_id}}?page=1&per_page=20`
- **Query Params**: Adjust pagination, optionally filter by type/status
- **Expected**: 200 OK with paginated transactions

#### 2. Create Transaction
- **Endpoint**: `POST /api/transactions`
- **Body**: Update transaction details
- **Expected**: 201 Created with transaction data

#### 3. Update Transaction Status
- **Endpoint**: `PUT /api/transactions/{transaction_id}/status`
- **URL**: Update transaction_id from Create response
- **Body**: Update status (pending/completed/failed)
- **Expected**: 200 OK

---

### Phase 10: Education

#### 1. Get Education Progress
- **Endpoint**: `GET /api/education/{{user_id}}`
- **Expected**: 200 OK with education progress

#### 2. Update Education Progress
- **Endpoint**: `POST /api/education/progress`
- **Body**: Update course details and progress
- **Expected**: 200 OK with updated progress

---

### Phase 11: News & Sentiment

#### 1. Scrape News
- **Endpoint**: `POST /api/news/scrape`
- **Expected**: 200 OK with scraping results

#### 2. Get Sentiment Analysis
- **Endpoint**: `GET /api/news/sentiment?limit=50`
- **Query Params**: Adjust limit, optionally filter by date
- **Expected**: 200 OK with sentiment analysis results

---

## Common Issues & Solutions

### Issue 1: "Token is missing or invalid"
**Solution**: 
- Run Login endpoint first
- Check if `access_token` is set in environment
- Verify token hasn't expired (tokens expire in 1 hour)

### Issue 2: "Unauthorized" error
**Solution**: 
- Verify user_id in URL matches logged-in user
- Check Authorization header is present
- Re-login if token expired

### Issue 3: "User not found" or "Portfolio not found"
**Solution**: 
- Create user first (Register/Login)
- Some endpoints auto-create resources (e.g., portfolio), others need manual creation

### Issue 4: Database errors
**Solution**: 
- Ensure database is initialized: `python setup.py`
- Check database connection in `.env` file
- Verify Supabase database is accessible

### Issue 5: Empty responses
**Solution**: 
- This is normal for new users (empty portfolios, goals, etc.)
- Create data using POST endpoints first
- Then GET endpoints will return data

---

## Testing Checklist

### ✅ Authentication
- [ ] Register user
- [ ] Login
- [ ] Get profile
- [ ] Update profile
- [ ] Refresh token
- [ ] Logout

### ✅ Risk Profiling
- [ ] Submit questionnaire
- [ ] Submit demographics
- [ ] Submit life events
- [ ] Submit behavioral data
- [ ] Calculate risk profile
- [ ] Get risk profile

### ✅ Portfolio
- [ ] Get portfolio
- [ ] Optimize portfolio
- [ ] Add holding
- [ ] Get performance
- [ ] Rebalance
- [ ] Delete holding

### ✅ Market Data
- [ ] Get indices
- [ ] Get sentiment
- [ ] Get predictions
- [ ] Get news
- [ ] Get technical indicators

### ✅ Behavioral Analytics
- [ ] Get metrics
- [ ] Update metrics
- [ ] Get insights

### ✅ Goals
- [ ] Get goals
- [ ] Create goal
- [ ] Get progress
- [ ] Update goal
- [ ] Delete goal

### ✅ AI Insights
- [ ] Get insights
- [ ] Get recommendations
- [ ] Get predictions
- [ ] Mark as read

### ✅ KYC
- [ ] Get documents
- [ ] Upload document
- [ ] Verify document

### ✅ Transactions
- [ ] Get transactions
- [ ] Create transaction
- [ ] Update status

### ✅ Education
- [ ] Get progress
- [ ] Update progress

### ✅ News
- [ ] Scrape news
- [ ] Get sentiment

---

## Quick Test Script

Run this sequence for a complete test:

1. **Register** → Get tokens
2. **Get Profile** → Verify user
3. **Submit Questionnaire** → Get Q-Score
4. **Submit Demographics** → Get cultural modifiers
5. **Calculate Risk Profile** → Get complete risk assessment
6. **Get Portfolio** → Should return empty portfolio
7. **Optimize Portfolio** → Get allocation recommendations
8. **Add Holding** → Create a holding
9. **Get Portfolio** → Should return portfolio with holding
10. **Create Goal** → Add a financial goal
11. **Get Goal Progress** → See progress tracking
12. **Get Market Indices** → Get market data
13. **Get AI Recommendations** → Get personalized advice

---

## Tips

1. **Use Collection Runner**: Run entire collection automatically
2. **Save Responses**: Save example responses for reference
3. **Use Variables**: Update `{{user_id}}` and other variables dynamically
4. **Test Error Cases**: Try invalid data to test error handling
5. **Check Logs**: Monitor Flask console for detailed error messages

---

## Expected Response Times

- Authentication endpoints: < 500ms
- Risk profiling: < 1s
- Portfolio operations: < 2s
- Market data: < 1s (cached)
- AI insights: < 3s (may vary with model loading)

---

## Notes

- All endpoints except Register and Login require authentication
- Token expires after 1 hour - use refresh endpoint
- Some endpoints auto-create resources (portfolio, behavioral metrics)
- Database is shared - changes persist across requests
- Use different users for testing different scenarios

Happy Testing! 🚀

