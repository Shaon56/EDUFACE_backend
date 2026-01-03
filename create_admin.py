"""
Script to create an admin account
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run import create_app, db
from app.models import User

# Create the app
app = create_app()

with app.app_context():
    # Check if admin already exists
    admin = User.query.filter_by(email='admin@eduface.com').first()
    
    if admin:
        print("✅ Admin account already exists!")
        print(f"   Email: {admin.email}")
        print(f"   Name: {admin.full_name}")
    else:
        # Create new admin
        admin = User(
            full_name='EDUFACE Administrator',
            student_id='ADMIN001',
            email='admin@eduface.com',
            parent_email='admin@eduface.com',
            contact_number='+1234567890',
            role='admin'
        )
        admin.set_password('admin123')  # Default password
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Admin account created successfully!")
        print("\n📋 Admin Credentials:")
        print("   Email: admin@eduface.com")
        print("   Password: admin123")
        print("\n⚠️  IMPORTANT: Change the default password after first login!")
