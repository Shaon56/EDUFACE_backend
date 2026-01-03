"""
Fix all get_jwt_identity() calls to convert to int
"""
import os
import re

files_to_fix = [
    'D:\\demo website\\backend\\app\\routes\\attendance.py',
    'D:\\demo website\\backend\\app\\routes\\results.py'
]

for filepath in files_to_fix:
    print(f"Fixing {filepath}...")
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace all occurrences of "user_id = get_jwt_identity()"
    # with "user_id = int(get_jwt_identity())"
    original_count = content.count('user_id = get_jwt_identity()')
    content = content.replace('user_id = get_jwt_identity()', 'user_id = int(get_jwt_identity())')
    
    # Also replace "current_user_id = get_jwt_identity()"
    content = content.replace('current_user_id = get_jwt_identity()', 'current_user_id = int(get_jwt_identity())')
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    new_count = content.count('user_id = int(get_jwt_identity())')
    print(f"  ✅ Fixed {original_count} occurrences")

print("\n✅ All files fixed!")
