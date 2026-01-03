# Google Sheets Setup Guide for EDUFACE

Your backend is now configured to use Google Sheets for persistent database storage instead of SQLite. This solves the Render ephemeral filesystem issue.

## What Has Been Done:

✅ **Created `google_sheets_db.py`** - Complete wrapper class for all Google Sheets operations
✅ **Updated all route files** - auth.py, users.py, routines.py, attendance.py, results.py
✅ **Copied service account JSON** - `backend/service_account.json` (READY)
✅ **Created .env file** - Configuration template ready
✅ **Removed SQLAlchemy** - __init__.py updated to use only JWT

## Next Steps:

### Step 1: Create Google Sheets Document

1. Go to [Google Sheets](https://sheets.google.com)
2. Click "Create new spreadsheet"
3. Name it: **EDUFACE Database**
4. Create 4 sheets with these exact names:
   - **Users**
   - **Routines**
   - **Attendance**
   - **Results**

### Step 2: Set Up Sheet Column Headers

**Users Sheet:**
```
ID | Full Name | Email | Password | Student ID | Phone | Role | Section | is_active | created_at
```

**Routines Sheet:**
```
ID | User ID | Day | start_time | end_time | Subject | instructor_name | room_number | created_at
```

**Attendance Sheet:**
```
ID | User ID | Subject | Status | Date | created_at
```

**Results Sheet:**
```
ID | User ID | Subject | Marks | Grade | Date | created_at
```

### Step 3: Share Google Sheets with Service Account

1. In your EDUFACE Database spreadsheet, click **Share** button (top right)
2. Add this email: `eduface-backend@eduface-483205.iam.gserviceaccount.com`
3. Give it **Editor** access
4. Click **Share**

### Step 4: Configure Render Environment Variable

When deploying to Render:

1. Go to your Render backend project settings
2. Add environment variable:
   - **Name:** `GOOGLE_SHEETS_CREDS`
   - **Value:** Copy the entire contents of your `service_account.json` file (it's in the backend folder)

The service account JSON already has your credentials, so no need to recreate it.

### Step 5: Test Locally

Before deploying, test on your computer:

```bash
cd d:\demo website\backend
pip install -r requirements.txt
python run.py
```

Visit: `http://localhost:5000`

Try registering a new user - check your Google Sheets to confirm data is saved!

## How It Works:

- **Local Development**: Uses `backend/service_account.json` file
- **Render Production**: Uses `GOOGLE_SHEETS_CREDS` environment variable
- **Automatic**: Code detects which one to use automatically
- **Same Code**: No changes needed between local and production

## Column Name Mapping:

The Google Sheets uses readable names with spaces:
- "Full Name" (not "full_name")
- "Student ID" (not "student_id")
- "User ID" (not "user_id")

The code handles this automatically - don't worry about underscore vs space differences.

## What This Solves:

✅ Data persists across Render redeploys
✅ No database server needed
✅ Free Google Sheets storage (millions of rows)
✅ Easy backup (just export the spreadsheet)
✅ Same API, faster deployment

## Files Modified:

- `backend/app/google_sheets_db.py` - NEW
- `backend/app/routes/auth.py` - UPDATED
- `backend/app/routes/users.py` - UPDATED
- `backend/app/routes/routines.py` - UPDATED
- `backend/app/routes/attendance.py` - UPDATED
- `backend/app/routes/results.py` - UPDATED
- `backend/app/__init__.py` - UPDATED (removed SQLAlchemy)
- `backend/.env` - NEW
- `backend/service_account.json` - COPIED from root

Ready to test! Let me know if you hit any issues.
