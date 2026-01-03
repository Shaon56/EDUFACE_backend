"""
Script to create an admin account (Google Sheets version)
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.google_sheets_db import GoogleSheetsDB
from werkzeug.security import generate_password_hash

# Initialize database
db = GoogleSheetsDB()

# Check if admin already exists
existing_users = db.get_all_users()
admin_exists = any(u.get('Email', '').lower() == 'admin@eduface.com' for u in existing_users)

if admin_exists:
    print("✅ Admin account already exists!")
    admin = [u for u in existing_users if u.get('Email', '').lower() == 'admin@eduface.com'][0]
    print(f"   Email: {admin.get('Email')}")
    print(f"   Name: {admin.get('Full Name')}")
else:
    # Create new admin
    admin_data = {
        'name': 'EDUFACE Administrator',
        'student_id': 'ADMIN001',
        'email': 'admin@eduface.com',
        'password': generate_password_hash('admin123'),
        'phone': '+1234567890',
        'role': 'admin',
        'section': 'Admin'
    }
    
    new_admin = db.add_user(admin_data)
    
    if new_admin:
        print("✅ Admin account created successfully!")
        print("\n📋 Admin Credentials:")
        print("   Email: admin@eduface.com")
        print("   Password: admin123")
        print("\n⚠️  IMPORTANT: Change the default password after first login!")
    else:
        print("❌ Failed to create admin account")
