from app.google_sheets_db import GoogleSheetsDB
from werkzeug.security import generate_password_hash

db = GoogleSheetsDB()
users = db.get_all_users()
print('All users in database:')
for user in users:
    print(f"  - {user.get('Full Name', 'N/A')} ({user.get('Email', 'N/A')}) - Role: {user.get('Role', 'N/A')}")

print("\n--- Creating Admin User ---")
# Create admin user
admin_data = {
    'name': 'Administrator',
    'email': 'admin@eduface.com',
    'password': generate_password_hash('admin123'),
    'student_id': 'ADMIN001',
    'phone': '01700000000',
    'role': 'admin',
    'section': 'Admin'
}

result = db.add_user(admin_data)
print(f"Admin user created: {result}")
print(f"Email: admin@eduface.com")
print(f"Password: admin123")
print(f"Role: admin")
