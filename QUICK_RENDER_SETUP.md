# Quick Render Setup (2 minutes)

## What You Need:
- Your Render dashboard open
- Your `service_account.json` file content (from backend folder)

## Steps:

### 1️⃣ Get Credentials
Open `d:\demo website\backend\service_account.json` and copy the entire content

### 2️⃣ Go to Render Environment
```
Render Dashboard 
  → Select EDUFACE_backend service
  → Click "Environment" (left sidebar)
```

### 3️⃣ Add First Variable: GOOGLE_SHEETS_CREDS
```
Name:  GOOGLE_SHEETS_CREDS
Value: [PASTE YOUR service_account.json CONTENT HERE]
Click Add
```

### 4️⃣ Add Second Variable: GOOGLE_SHEETS_ID
```
Name:  GOOGLE_SHEETS_ID
Value: EDUFACE Database
Click Add
```

### 5️⃣ Add Third Variable: FLASK_ENV
```
Name:  FLASK_ENV
Value: production
Click Add
```

### 6️⃣ Save and Deploy
- Click "Save"
- Render auto-redeploys
- Wait 2-3 minutes
- Check deployment logs

## That's It! ✅

Your backend is now:
✅ Connected to Google Sheets
✅ Live on Render
✅ Ready to serve your frontend

## Quick Test:
```bash
curl -X GET https://your-render-url.onrender.com/api/health
# Should return: {"status":"ok","message":"EDUFACE backend is running"}
```

Need help? See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for detailed instructions.
