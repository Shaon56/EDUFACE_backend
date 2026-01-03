#!/usr/bin/env python3
"""
Reset password for a user
"""

from app.google_sheets_db import GoogleSheetsDB
from werkzeug.security import generate_password_hash

def reset_password():
    db = GoogleSheetsDB()
    
    email = input("Enter email to reset password for: ").strip()
    new_password = input("Enter new password: ").strip()
    
    # Find user
    user = db.find_user_by_email(email)
    
    if not user:
        print(f"❌ User not found: {email}")
        return
    
    print(f"\nResetting password for: {user.get('Full Name')} ({email})")
    print(f"Role: {user.get('Role')}")
    
    # Update password in Google Sheets
    try:
        users = db.users_sheet.get_all_records()
        
        # Find the row number (add 2 for header and 1-based indexing)
        for i, record in enumerate(users):
            if record.get('Email', '').lower() == email.lower():
                row_num = i + 2  # +2 because headers are row 1, records start at row 2
                
                # Hash the new password
                hashed_password = generate_password_hash(new_password)
                
                # Update the password cell (Column C = 3)
                db.users_sheet.update_cell(row_num, 4, hashed_password)  # Column 4 is Password
                
                print(f"✅ Password reset successfully!")
                print(f"   New Password: {new_password}")
                print(f"\nUser can now login with:")
                print(f"   Email: {email}")
                print(f"   Password: {new_password}")
                return
        
        print(f"❌ User not found in records")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    reset_password()
