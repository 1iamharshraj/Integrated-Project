# Windows Installation Guide

This guide helps you install the ZeTheta FinArcade backend on Windows, especially when dealing with package installation issues.

## Quick Start

### 1. Install Core Dependencies (Required)

```powershell
cd "Integrated Projects\Backend"
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Install AI/ML Dependencies (Optional)

If you need AI model functionality (FinBERT, sentiment analysis, etc.), install the optional packages:

```powershell
# First, try installing transformers without sentencepiece
pip install transformers torch scikit-learn --no-deps

# Then install dependencies individually
pip install tokenizers accelerate safetensors huggingface-hub
pip install protobuf

# If you need sentencepiece (for some tokenizers), try:
# Option 1: Use pre-built wheel from unofficial source
pip install sentencepiece --no-build-isolation

# Option 2: Install CMake and Visual Studio Build Tools first
# Download CMake from: https://cmake.org/download/
# Install Visual Studio Build Tools from: https://visualstudio.microsoft.com/downloads/
# Then: pip install sentencepiece
```

## Troubleshooting Common Issues

### Issue 1: sentencepiece Installation Fails

**Error**: `CMake Error` or `subprocess-exited-with-error`

**Solution**: 
1. **Skip sentencepiece** (recommended for basic functionality):
   - Most transformers models work without it
   - Only needed for specific tokenizers (like T5, mT5)
   - FinBERT typically doesn't require it

2. **Install with pre-built wheels**:
   ```powershell
   pip install sentencepiece --no-build-isolation
   ```

3. **Install build dependencies**:
   - Install CMake: https://cmake.org/download/
   - Install Visual Studio Build Tools (C++ workload)
   - Then retry: `pip install sentencepiece`

### Issue 2: PyTorch Installation Issues

**Solution**: Install PyTorch from official site with CPU support:
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Issue 3: psycopg2 Installation Issues

**Solution**: Use the binary version (already in requirements.txt):
```powershell
pip install psycopg2-binary
```

### Issue 4: lxml Installation Issues

**Solution**: Install from unofficial Windows binaries:
```powershell
pip install lxml --prefer-binary
```

## Installation Without AI Dependencies

If you only need the core API functionality without AI models:

```powershell
# Install only core requirements
pip install -r requirements.txt

# Skip requirements-ai.txt
# The backend will work, but AI features will be placeholders
```

## Verification

After installation, verify everything works:

```powershell
# Test imports
python -c "import flask; import sqlalchemy; import flask_jwt_extended; print('Core packages OK')"

# Test database connection
python test_db_connection.py

# Test application startup
python app.py
```

## Alternative: Use Conda (Recommended for ML packages)

If you're having issues with pip, consider using Conda:

```powershell
# Install Miniconda from: https://docs.conda.io/en/latest/miniconda.html

# Create environment
conda create -n zetheta python=3.11
conda activate zetheta

# Install packages
conda install -c conda-forge flask sqlalchemy psycopg2
pip install -r requirements.txt

# For AI packages, conda handles dependencies better
conda install -c conda-forge pytorch transformers scikit-learn
```

## Minimal Installation (Core API Only)

For development without AI features:

```powershell
pip install Flask==3.0.0
pip install Flask-SQLAlchemy==3.1.1
pip install Flask-Migrate==4.0.5
pip install Flask-JWT-Extended==4.6.0
pip install Flask-CORS==4.0.0
pip install psycopg2-binary==2.9.9
pip install python-dotenv==1.0.0
pip install bcrypt==4.1.2
pip install marshmallow==3.20.1
pip install redis==5.0.1
pip install requests==2.31.0
pip install beautifulsoup4==4.12.2
```

## System Requirements

- **Python**: 3.9 or higher (3.11 recommended)
- **Windows**: 10 or 11
- **Visual Studio Build Tools**: Required only for building packages from source (optional)
- **CMake**: Required only for sentencepiece (optional)

## Getting Help

If you encounter issues:

1. Check Python version: `python --version`
2. Upgrade pip: `python -m pip install --upgrade pip`
3. Check error messages - they often suggest solutions
4. Try installing packages individually to identify problematic ones
5. Use `--no-cache-dir` if encountering cache issues: `pip install --no-cache-dir <package>`

## Notes

- **sentencepiece is optional**: Most backend functionality works without it
- **AI models are optional**: The backend can run with placeholder AI services
- **Pre-built wheels preferred**: Always try `pip install --prefer-binary` first
- **Virtual environment recommended**: Always use a virtual environment to avoid conflicts

