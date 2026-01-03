import requests
import json

BASE_URL = "http://localhost:5000"

# Test data
test_user = {
    "full_name": "Test Student",
    "student_id": "STU001",
    "email": "test@eduface.com",
    "contact_number": "1234567890",
    "password": "test123"
}

# Test Registration
print("=" * 50)
print("Testing Registration...")
print("=" * 50)
response = requests.post(f"{BASE_URL}/api/auth/register", json=test_user)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 201:
    print("✅ Registration successful!")
    
    # Test Login
    print("\n" + "=" * 50)
    print("Testing Login...")
    print("=" * 50)
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Login successful!")
        token = response.json().get('access_token')
        print(f"Token: {token[:50]}...")
    else:
        print("❌ Login failed")
else:
    print("❌ Registration failed")
