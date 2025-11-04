# Security Keys Guide

## Overview

The Flask application requires two security keys:
1. **SECRET_KEY** - Used by Flask for session management, CSRF protection, and other security features
2. **JWT_SECRET_KEY** - Used to sign and verify JWT (JSON Web Token) tokens for user authentication

## Generating Keys

### Method 1: Using the provided script (Recommended)

Run the key generation script:

```bash
python generate_secrets.py
```

This will generate two random 64-character secure keys. Copy them and add to your `.env` file.

### Method 2: Using Python directly

```python
import secrets
import string

alphabet = string.ascii_letters + string.digits + string.punctuation
secret_key = ''.join(secrets.choice(alphabet) for _ in range(64))
jwt_secret_key = ''.join(secrets.choice(alphabet) for _ in range(64))

print(f"SECRET_KEY={secret_key}")
print(f"JWT_SECRET_KEY={jwt_secret_key}")
```

### Method 3: Using OpenSSL (Linux/Mac)

```bash
# Generate SECRET_KEY
openssl rand -hex 32

# Generate JWT_SECRET_KEY
openssl rand -hex 32
```

### Method 4: Using PowerShell (Windows)

```powershell
# Generate SECRET_KEY
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | % {[char]$_})

# Generate JWT_SECRET_KEY
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | % {[char]$_})
```

## Adding Keys to .env File

After generating the keys, add them to your `.env` file:

```env
SECRET_KEY=your-generated-secret-key-here
JWT_SECRET_KEY=your-generated-jwt-secret-key-here
DATABASE_URL=postgresql://postgres:ZeThetha#$1@db.bzwpbznefkiypvsbcoio.supabase.co:5432/postgres
REDIS_URL=redis://localhost:6379/0
FLASK_ENV=development
```

## Security Best Practices

### ✅ DO:
- Use different keys for development and production
- Generate keys that are at least 32 characters long (preferably 64)
- Store keys securely in environment variables
- Use strong, random keys (not dictionary words or predictable patterns)
- Rotate keys periodically in production
- Keep keys private and never commit them to version control

### ❌ DON'T:
- Use predictable values like "secret", "password", "12345"
- Share keys publicly or commit them to Git
- Use the same keys across different environments
- Reuse keys from other projects
- Hardcode keys in your source code

## What Happens if Keys are Compromised?

### SECRET_KEY Compromised:
- Sessions can be hijacked
- CSRF protection can be bypassed
- User data can be at risk

**Action**: Immediately regenerate the key and force all users to re-authenticate

### JWT_SECRET_KEY Compromised:
- Attackers can forge authentication tokens
- Unauthorized access to user accounts
- Complete security breach

**Action**: Immediately regenerate the key, invalidate all existing tokens, and force all users to log in again

## Key Rotation

For production environments, consider rotating keys periodically:

1. Generate new keys
2. Update the `.env` file with new keys
3. Restart the application
4. Force all users to re-authenticate (optional but recommended)

## Verification

After adding keys to your `.env` file, verify they're being loaded:

```python
from config import Config
import os

# Check if keys are loaded
print("SECRET_KEY loaded:", bool(Config.SECRET_KEY))
print("JWT_SECRET_KEY loaded:", bool(Config.JWT_SECRET_KEY))
```

## Troubleshooting

### "SECRET_KEY not set" error
- Make sure `.env` file exists in the backend directory
- Verify keys are added correctly (no extra spaces, proper format)
- Check that `python-dotenv` is installed: `pip install python-dotenv`

### "JWT token invalid" error
- Verify JWT_SECRET_KEY matches between token creation and verification
- Check if keys were changed after tokens were issued (tokens will be invalid)
- Ensure keys are properly formatted in `.env` file

### Keys not loading from .env
- Check file path: `.env` should be in the same directory as `config.py`
- Verify `load_dotenv()` is called in `config.py`
- Try absolute path: `load_dotenv('/path/to/.env')`

## Production Deployment

For production, consider using:
- **Environment variables** set directly on the server
- **Secret management services** (AWS Secrets Manager, HashiCorp Vault, etc.)
- **CI/CD pipeline secrets** for automated deployments

Never hardcode keys or commit them to version control!

