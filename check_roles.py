from app.google_sheets_db import GoogleSheetsDB

db = GoogleSheetsDB()
users = db.get_all_users()

print("User Roles:")
for user in users:
    print(f"  {user.get('Full Name')}: Role = '{user.get('Role')}'")
