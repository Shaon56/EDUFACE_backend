"""
Test user profile update functionality
"""

from app.google_sheets_db import GoogleSheetsDB
import json

db = GoogleSheetsDB()

print("=" * 70)
print("USER PROFILE UPDATE TEST")
print("=" * 70)

# Get original user
user_before = db.find_user_by_id(2)
print(f"\n✓ Before update:")
print(f"  Full Name: {user_before.get('Full Name')}")
print(f"  Phone: {user_before.get('Phone')}")

# Test update
print(f"\n✓ Attempting to update user 2...")
update_data = {
    'Full Name': 'Updated Name',
    'Phone': '1234567890',
}

result = db.update_user(2, update_data)
print(f"  Update result: {result}")

# Get updated user
user_after = db.find_user_by_id(2)
print(f"\n✓ After update:")
print(f"  Full Name: {user_after.get('Full Name')}")
print(f"  Phone: {user_after.get('Phone')}")

print("\n" + "=" * 70)
if user_after.get('Full Name') == 'Updated Name':
    print("✅ Profile update working correctly!")
else:
    print("⚠️  Profile update may need debugging")
print("=" * 70)
