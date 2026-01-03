from app.google_sheets_db import GoogleSheetsDB
from werkzeug.security import generate_password_hash
import gspread

db = GoogleSheetsDB()

# Update student password  
new_password_hash = generate_password_hash('test123')

# Get the users sheet
users_sheet = db.users_sheet
all_users = users_sheet.get_all_records()

# Find the Shaon Mondal row (should be around row 5 based on previous output)
for i, user in enumerate(all_users):
    if user.get('Email') == 'mondal33-1627@diu.edu.bd':
        row_num = i + 2  # +1 for headers, +1 for 0-indexing
        users_sheet.update_cell(row_num, 4, new_password_hash)  # Column 4 is Password
        print(f"✅ Password updated for Shaon Mondal (Row {row_num})")
        print(f"Email: mondal33-1627@diu.edu.bd")
        print(f"New Password: test123")
        break
