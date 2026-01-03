from app.google_sheets_db import GoogleSheetsDB
try:
    db = GoogleSheetsDB()
    print("✅ Google Sheets connected successfully!")
    users = db.get_all_users()
    print(f"✅ Users sheet found: {len(users)} rows")
    routines = db.get_all_routines()
    print(f"✅ Routines sheet found: {len(routines)} rows")
    attendance = db.get_all_attendance()
    print(f"✅ Attendance sheet found: {len(attendance)} rows")
    results = db.get_all_results()
    print(f"✅ Results sheet found: {len(results)} rows")
    print("\n✅✅✅ All sheets are ready! ✅✅✅")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
