from app.google_sheets_db import GoogleSheetsDB

db = GoogleSheetsDB()
routines = db.get_all_routines()

print("Available Subjects:")
subjects = set()
for routine in routines:
    subject = routine.get('subject', 'Unknown')
    subjects.add(subject)
    print(f"  - {subject}")

print(f"\nTotal subjects: {len(subjects)}")
