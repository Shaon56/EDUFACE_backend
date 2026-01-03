# 🚀 RENDER DEPLOYMENT GUIDE

## Environment Variables You Need to Set on Render:

### Step 1: Go to Render Dashboard
1. Log in to [render.com](https://render.com)
2. Select your **EDUFACE_backend** service
3. Click **"Environment"** tab (in the left menu)

### Step 2: Add Environment Variables

Add these 3 environment variables:

#### Variable 1: GOOGLE_SHEETS_CREDS
- **Name:** `GOOGLE_SHEETS_CREDS`
- **Value:** Copy the **ENTIRE** `service_account.json` file content from your local `backend/service_account.json`
  - The file contains JSON with type, project_id, private_key, etc.
  - Paste the **entire JSON as one line** or multiline (Render handles both)

**How to copy:**
```bash
# On your computer, copy the file content:
cat "d:\demo website\backend\service_account.json"
# Then paste it into Render's GOOGLE_SHEETS_CREDS field
```

#### Variable 2: GOOGLE_SHEETS_ID
- **Name:** `GOOGLE_SHEETS_ID`
- **Value:** `EDUFACE Database`

#### Variable 3: FLASK_ENV
- **Name:** `FLASK_ENV`
- **Value:** `production`

### Step 3: Save and Redeploy

1. Click **"Save"** after adding variables
2. Render will automatically redeploy
3. Wait 2-3 minutes for deployment to complete
4. Check logs to verify `✅ Google Sheets connected successfully!`

## Verification:

After deployment, test your endpoints:

```bash
# Test registration
curl -X POST https://your-render-url.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name":"Test User",
    "student_id":"STU001",
    "email":"test@eduface.com",
    "contact_number":"1234567890",
    "password":"test123"
  }'

# Expected response (201):
# {"message":"Registration successful","user":{...}}
```

## Troubleshooting:

### Error: "service_account.json not found"
- Check that `GOOGLE_SHEETS_CREDS` env variable is set ✅
- Verify it's the complete JSON content (not just a path)
- Restart the service (Render → Manual Deploy)

### Error: "Spreadsheet not found"
- Check that Google Sheet is named **exactly** "EDUFACE Database"
- Verify it's shared with `eduface-backend@eduface-483205.iam.gserviceaccount.com`
- Check that all 4 sheets exist: Users, Routine(s), Attendance, Result(s)

### Error: "WorksheetNotFound"
- Verify sheet names match what's in your Google Sheets
- Code handles: Users/User, Routines/Routine, Attendance/Attendances, Results/Result

## What Should Happen:

✅ Code is deployed from GitHub
✅ Flask app starts
✅ On first request, Google Sheets connects using GOOGLE_SHEETS_CREDS
✅ Registration/Login creates records in your Google Sheet
✅ Data persists across redeploys (unlike SQLite)

You're ready to go! 🎉
