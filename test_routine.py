"""
Test script to verify Google Sheets database connection
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.google_sheets_db import GoogleSheetsDB

# Initialize database
db = GoogleSheetsDB()

try:
    # Test getting all users
    print("Testing Google Sheets connection...")
    users = db.get_all_users()
    print(f"✅ Successfully connected to Google Sheets!")
    print(f"   Total users in database: {len(users)}")
    
    if users:
        print("\n📋 Sample user:")
        first_user = users[0]
        for key, value in first_user.items():
            print(f"   {key}: {value}")
    
    # Test getting routines
    print("\nTesting routine retrieval...")
    routines = db.get_all_routines()
    print(f"✅ Successfully retrieved routines!")
    print(f"   Total routines: {len(routines)}")
    
    if routines:
        print("\n📋 Sample routine:")
        first_routine = routines[0]
        for key, value in first_routine.items():
            print(f"   {key}: {value}")
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
