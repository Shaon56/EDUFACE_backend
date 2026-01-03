#!/usr/bin/env python3
"""
Add or verify admin user in Google Sheets
"""

from app.google_sheets_db import GoogleSheetsDB
from werkzeug.security import generate_password_hash

def add_admin_user():
    db = GoogleSheetsDB()
    
    # Check if admin already exists
    admin = db.find_user_by_email('admin@eduface.com')
    
    print("=" * 60)
    if admin:
        print("✅ Admin user already exists!")
        print(f"   Email: {admin.get('Email')}")
        print(f"   Name: {admin.get('Full Name')}")
        print(f"   Role: {admin.get('Role')}")
    else:
        print("❌ Admin user not found. Creating admin user...")
        
        # Create admin user
        admin_data = {
            'name': 'Administrator',
            'email': 'admin@eduface.com',
            'password': generate_password_hash('admin123'),
            'student_id': 'ADMIN001',
            'phone': '0000000000',
            'role': 'admin',
            'section': 'Admin'
        }
        
        new_admin = db.add_user(admin_data)
        
        if new_admin:
            print("✅ Admin user created successfully!")
            print(f"   Email: admin@eduface.com")
            print(f"   Password: admin123")
            print(f"   ID: {new_admin['id']}")
        else:
            print("❌ Failed to create admin user")
    
    print("=" * 60)
    
    # List all users
    print("\nAll users in database:")
    print("-" * 60)
    users = db.get_all_users()
    if users:
        for user in users:
            print(f"ID: {user.get('ID'):3} | Name: {user.get('Full Name'):20} | Email: {user.get('Email'):30} | Role: {user.get('Role')}")
    else:
        print("No users found")
    print("-" * 60)

if __name__ == '__main__':
    add_admin_user()
