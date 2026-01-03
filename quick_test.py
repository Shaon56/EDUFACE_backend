import requests
import json
import time

# Wait for Flask to fully start
time.sleep(2)

BASE_URL = "http://localhost:5000"

# Test data
test_user = {
    "full_name": "Test Student",
    "student_id": "STU001",
    "email": "test@eduface.com",
    "contact_number": "1234567890",
    "password": "test123"
}

try:
    # Test Registration
    print("=" * 50)
    print("Testing Registration...")
    print("=" * 50)
    response = requests.post(f"{BASE_URL}/api/auth/register", json=test_user, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("\n✅ Registration successful!")
    else:
        print("\n❌ Registration failed")
        
except Exception as e:
    print(f"❌ Error: {e}")
