# Troubleshooting Guide

## Issue: 500 Error on Registration

### Symptoms
- `POST /api/auth/register` returns 500 Internal Server Error
- Console shows: `127.0.0.1 - - [timestamp] "POST /api/auth/register HTTP/1.1" 500 -`

### Common Causes & Solutions

#### 1. Database Tables Not Created

**Check:**
```bash
python check_database.py
```

**Solution:**
```bash
# Option 1: Quick setup
python setup.py

# Option 2: Using Flask-Migrate (recommended)
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

#### 2. Database Connection Issue

**Check:**
```bash
python test_db_connection.py
```

**Solution:**
- Verify `.env` file has correct `DATABASE_URL`
- Check Supabase database is accessible
- Ensure database credentials are correct

#### 3. Missing Required Fields

**Error in response:**
```json
{"error": "Missing required field: email"}
```

**Solution:**
Ensure request body includes:
- `email`
- `password`
- `first_name`
- `last_name`
- `phone` (optional)

#### 4. User Already Exists

**Error in response:**
```json
{"error": "User already exists"}
```

**Solution:**
- Use a different email
- Or login instead of registering

#### 5. Invalid Email Format

**Error in response:**
```json
{"error": "Invalid email format"}
```

**Solution:**
- Use valid email format: `user@example.com`

#### 6. Database Schema Issues

**Check:**
- Run `python check_database.py` to verify all tables exist
- Check if migrations are applied: `flask db current`

**Solution:**
```bash
# Recreate database (WARNING: This deletes all data)
flask db downgrade base
flask db upgrade
```

### Debug Steps

1. **Check error details in console:**
   - The improved error handling now prints full traceback
   - Look for specific error message in Flask console

2. **Verify database:**
   ```bash
   python check_database.py
   ```

3. **Test database connection:**
   ```bash
   python test_db_connection.py
   ```

4. **Check Flask debug output:**
   - Ensure `FLASK_ENV=development` in `.env`
   - Check console for detailed error messages

5. **Verify request format:**
   ```json
   {
     "email": "test@example.com",
     "password": "SecurePass123!",
     "first_name": "John",
     "last_name": "Doe"
   }
   ```

### Expected Response (Success)

```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "test@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": null,
    "is_verified": false,
    "created_at": "2024-11-04T23:00:00",
    "updated_at": "2024-11-04T23:00:00"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Quick Fix Checklist

- [ ] Database tables created (`python check_database.py`)
- [ ] Database connection working (`python test_db_connection.py`)
- [ ] `.env` file has correct `DATABASE_URL`
- [ ] Request includes all required fields
- [ ] Email format is valid
- [ ] User doesn't already exist
- [ ] Flask server is running
- [ ] Virtual environment is activated

### Getting More Details

The improved error handler now returns detailed error information in debug mode:

```json
{
  "error": "Internal server error",
  "message": "Detailed error message",
  "details": "Full traceback (only in debug mode)"
}
```

Check the Flask console output for the full traceback.

