"""
Test what the backend returns for user profile
"""

from app.google_sheets_db import GoogleSheetsDB
import json

db = GoogleSheetsDB()

# Get user 2 (the one we've been testing)
user = db.find_user_by_id(2)

print("Backend returns these fields:")
print(json.dumps(user, indent=2))

print("\n\nFrontend expects these fields:")
expected = {
    'full_name': 'N/A',
    'student_id': 'N/A',
    'email': 'N/A',
    'parent_email': 'N/A',
    'contact_number': 'N/A'
}
print(json.dumps(expected, indent=2))

print("\n\nField Mapping Needed:")
print(f"Backend: 'Full Name' → Frontend needs: 'full_name'")
print(f"Backend: 'Student ID' → Frontend needs: 'student_id'")
print(f"Backend: 'Email' → Frontend needs: 'email'")
print(f"Backend: 'Phone' → Frontend needs: 'contact_number' or 'phone'")
print(f"Backend: 'Parent Email' → Frontend needs: 'parent_email' (NOT in Google Sheets!)")
