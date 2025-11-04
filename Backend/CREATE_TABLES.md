# Quick Fix: Create Database Tables

## The Problem
Error: `relation "users" does not exist`

This means the database tables haven't been created yet.

## Solution

### Option 1: Using setup.py (Recommended)

**Step 1: Activate virtual environment**
```powershell
cd "D:\internships\Zetheta\Integrated Projects\Backend"
venv\Scripts\activate
```

**Step 2: Run setup script**
```powershell
python setup.py
```

You should see:
```
Creating database tables...
Database tables created successfully!

You can now run the application with: python app.py
```

### Option 2: Using Flask-Migrate

**Step 1: Activate virtual environment**
```powershell
cd "D:\internships\Zetheta\Integrated Projects\Backend"
venv\Scripts\activate
```

**Step 2: Initialize migrations (first time only)**
```powershell
flask db init
```

**Step 3: Create migration**
```powershell
flask db migrate -m "Initial migration"
```

**Step 4: Apply migration**
```powershell
flask db upgrade
```

### Option 3: Direct SQLAlchemy (Quick)

Create a simple script:

```python
# create_tables_now.py
from app import create_app
from extensions import db
from models import *

app = create_app()
with app.app_context():
    db.create_all()
    print("✅ Tables created!")
```

Run:
```powershell
python create_tables_now.py
```

## Verify Tables Created

Run:
```powershell
python check_database.py
```

You should see all tables marked with ✅.

## After Creating Tables

Try the registration endpoint again in Postman. It should work now!

## Troubleshooting

**If you get "ModuleNotFoundError":**
- Make sure virtual environment is activated: `venv\Scripts\activate`
- Install requirements: `pip install -r requirements.txt`

**If you get "Database connection error":**
- Check `.env` file has correct `DATABASE_URL`
- Run: `python test_db_connection.py`

