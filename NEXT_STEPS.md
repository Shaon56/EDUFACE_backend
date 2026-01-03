# ✅ Credentials Fixed - Now Create Google Sheets

## What's Done:
✅ `service_account.json` copied to backend folder
✅ Code now finds credentials correctly

## What You Need to Do NOW:

### Step 1: Create Google Sheets Document

1. Go to https://sheets.google.com
2. Click **"+ Create"** → **"Blank spreadsheet"**
3. Name it: **EDUFACE Database**

### Step 2: Create 4 Sheets

At the bottom of your spreadsheet, you'll see sheet tabs. Delete "Sheet1" and create these 4 sheets:

**Sheet 1: Users**
Add these headers in Row 1:
```
A: ID
B: Full Name
C: Email
D: Password
E: Student ID
F: Phone
G: Role
H: Section
I: is_active
J: created_at
```

**Sheet 2: Routines**
Add these headers in Row 1:
```
A: ID
B: User ID
C: Day
D: start_time
E: end_time
F: Subject
G: instructor_name
H: room_number
I: created_at
```

**Sheet 3: Attendance**
Add these headers in Row 1:
```
A: ID
B: User ID
C: Subject
D: Status
E: Date
F: created_at
```

**Sheet 4: Results**
Add these headers in Row 1:
```
A: ID
B: User ID
C: Subject
D: Marks
E: Grade
F: Date
G: created_at
```

### Step 3: Share with Service Account

1. Click **Share** button (top right)
2. Paste this email: `eduface-backend@eduface-483205.iam.gserviceaccount.com`
3. Select **Editor** permission
4. Click **Share**

### Step 4: Test Locally

```bash
cd d:\demo website\backend
python run.py
```

Then test registration at `http://localhost:5000`

## Quick Checklist:
- [ ] Created "EDUFACE Database" spreadsheet
- [ ] Created 4 sheets: Users, Routines, Attendance, Results
- [ ] Added column headers to each sheet
- [ ] Shared with service account email
- [ ] Tested locally (optional)

Once done, reply with "Done" and I'll help you deploy to Render!
