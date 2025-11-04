# Quick Start - Create Database Tables

## You're Already in Virtual Environment! ✅

Your terminal shows `(venv) PS` which means you're ready.

## Create Tables Now

**Simply run in your current terminal:**

```powershell
python create_tables_now.py
```

**OR:**

```powershell
python setup.py
```

## Expected Output

You should see:
```
Creating database tables...
✅ All database tables created successfully!

You can now test the registration endpoint.
```

## If You Get Module Errors

Make sure you're in the venv (you should see `(venv)` in prompt).

If not, activate it:
```powershell
venv\Scripts\activate
```

Then install missing packages:
```powershell
pip install -r requirements.txt
```

## After Tables Are Created

1. **Verify tables:**
   ```powershell
   python check_database.py
   ```
   All should show ✅

2. **Test registration in Postman:**
   - Try `POST /api/auth/register` again
   - Should work now!

3. **Start server:**
   ```powershell
   python app.py
   ```

