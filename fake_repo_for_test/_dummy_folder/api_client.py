"""
API Client for User Management
Old version with outdated patterns
"""

import requests
import json
from datetime import datetime

def get_users():
    """Fetch all users from API"""
    response = requests.get("https://api.example.com/users")
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

def create_user(name, email, age):
    """Create a new user"""
    data = {
        "name": name,
        "email": email,
        "age": age,
        "created_at": datetime.now().isoformat()
    }
    response = requests.post(
        "https://api.example.com/users",
        data=json.dumps(data),
        headers={"Content-Type": "application/json"}
    )
    return response.json()

def update_user(user_id, name, email):
    """Update existing user"""
    url = "https://api.example.com/users/" + str(user_id)
    data = {"name": name, "email": email}
    response = requests.put(url, data=json.dumps(data))
    if response.status_code == 200:
        return True
    return False

def delete_user(user_id):
    """Delete a user"""
    url = "https://api.example.com/users/%s" % user_id
    response = requests.delete(url)
    return response.status_code == 204

def get_user_stats():
    """Get statistics about users"""
    users = get_users()
    if users is None:
        return None
    
    total = len(users)
    active = 0
    inactive = 0
    
    for user in users:
        if user.get("active") == True:
            active = active + 1
        else:
            inactive = inactive + 1
    
    return {
        "total": total,
        "active": active,
        "inactive": inactive
    }

if __name__ == "__main__":
    # Test the functions
    users = get_users()
    print("Total users:", len(users) if users else 0)
    
    stats = get_user_stats()
    print("Stats:", stats)