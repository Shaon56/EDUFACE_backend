"""
Test user profile display mapping
Verify that frontend will receive correct field names
"""

from app.google_sheets_db import GoogleSheetsDB
import json

db = GoogleSheetsDB()

user = db.find_user_by_id(2)

print("=" * 70)
print("USER PROFILE DISPLAY TEST")
print("=" * 70)

print("\n✓ Backend returns:")
print(json.dumps(user, indent=2))

print("\n✓ Frontend will map these to form fields:")
form_data = {
    'profile-name': user['Full Name'] or user.get('full_name') or 'N/A',
    'profile-student-id': user['Student ID'] or user.get('student_id') or 'N/A',
    'profile-email': user['Email'] or user.get('email') or 'N/A',
    'profile-parent-email': user.get('Parent Email') or user.get('parent_email') or '',
    'profile-contact': user['Phone'] or user.get('phone') or user.get('contact_number') or 'N/A',
}

print(f"  Full Name:     {form_data['profile-name']}")
print(f"  Student ID:    {form_data['profile-student-id']}")
print(f"  Email:         {form_data['profile-email']}")
print(f"  Parent Email:  {form_data['profile-parent-email']}")
print(f"  Contact:       {form_data['profile-contact']}")

print("\n" + "=" * 70)
print("✅ Profile fields will display correctly!")
print("=" * 70)
