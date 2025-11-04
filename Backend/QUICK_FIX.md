# Quick Fix for sentencepiece Installation Error

## Problem
You're getting a CMake error when installing `sentencepiece` on Windows.

## Quick Solution (Recommended)

**Skip sentencepiece installation** - it's not required for core functionality:

```powershell
# Install core packages (this will work)
pip install -r requirements.txt

# Skip requirements-ai.txt for now, or install without sentencepiece
pip install transformers torch scikit-learn --no-deps
pip install tokenizers accelerate safetensors huggingface-hub protobuf
```

The backend will work fine with placeholder AI services. You can add actual AI models later.

## Alternative: Install Core Only

If you just want to get the API running:

```powershell
pip install Flask==3.0.0 Flask-SQLAlchemy==3.1.1 Flask-Migrate==4.0.5
pip install Flask-JWT-Extended==4.6.0 Flask-CORS==4.0.0
pip install psycopg2-binary==2.9.9 python-dotenv==1.0.0
pip install bcrypt==4.1.2 marshmallow==3.20.1 redis==5.0.1
pip install requests==2.31.0 beautifulsoup4==4.12.2 pandas==2.1.4 numpy==1.26.2
```

## Why This Works

- `sentencepiece` is only needed for specific tokenizers (T5, mT5)
- FinBERT (used in Project 25) typically doesn't require it
- The backend uses placeholder AI services by default
- You can add real AI models later when needed

## Next Steps

1. Install core packages (see above)
2. Generate secret keys: `python generate_secrets.py`
3. Test database: `python test_db_connection.py`
4. Initialize database: `python setup.py`
5. Run application: `python app.py`

The API will work with placeholder AI services. You can integrate actual models later.

