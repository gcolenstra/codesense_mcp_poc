"""
API Client for User Management
Modernized for Python 3.9+
"""

import requests
from datetime import datetime
from typing import Optional, Dict, List, Any


def get_users() -> Optional[List[Dict[str, Any]]]:
    """
    Fetch all users from API.
    
    Returns:
        Optional[List[Dict[str, Any]]]: List of user dictionaries if successful, None otherwise.
    """
    response = requests.get("https://api.example.com/users")
    if response.status_code == 200:
        return response.json()
    else:
        return None


def create_user(name: str, email: str, age: int) -> Dict[str, Any]:
    """
    Create a new user.
    
    Args:
        name: User's full name.
        email: User's email address.
        age: User's age.
    
    Returns:
        Dict[str, Any]: Created user data from API response.
    """
    data = {
        "name": name,
        "email": email,
        "age": age,
        "created_at": datetime.now().isoformat()
    }
    response = requests.post(
        "https://api.example.com/users",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    return response.json()


def update_user(user_id: int, name: str, email: str) -> bool:
    """
    Update existing user.
    
    Args:
        user_id: ID of the user to update.
        name: Updated user name.
        email: Updated user email.
    
    Returns:
        bool: True if update successful, False otherwise.
    """
    url = f"https://api.example.com/users/{user_id}"
    data = {"name": name, "email": email}
    response = requests.put(url, json=data)
    return response.status_code == 200


def delete_user(user_id: int) -> bool:
    """
    Delete a user.
    
    Args:
        user_id: ID of the user to delete.
    
    Returns:
        bool: True if deletion successful, False otherwise.
    """
    url = f"https://api.example.com/users/{user_id}"
    response = requests.delete(url)
    return response.status_code == 204


def get_user_stats() -> Optional[Dict[str, int]]:
    """
    Get statistics about users.
    
    Returns:
        Optional[Dict[str, int]]: Dictionary with total, active, and inactive counts,
                                  or None if users cannot be fetched.
    """
    users = get_users()
    if users is None:
        return None
    
    total = len(users)
    active = sum(1 for user in users if user.get("active") is True)
    inactive = total - active
    
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