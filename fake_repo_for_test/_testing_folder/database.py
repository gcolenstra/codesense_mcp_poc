"""
Database Helper Functions
Refactored for Python 3.9+ with security improvements
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict, Tuple
from contextlib import contextmanager
import hashlib
import secrets

DATABASE_PATH = "users.db"


@contextmanager
def get_db_connection():
    """
    Context manager for database connections.
    
    Ensures proper connection handling and automatic cleanup.
    
    Yields:
        sqlite3.Connection: Database connection object
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256 with a salt.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        str: Hashed password with salt (salt:hash format)
    """
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}:{pwd_hash}"


def verify_password(password: str, stored_hash: str) -> bool:
    """
    Verify a password against a stored hash.
    
    Args:
        password: Plain text password to verify
        stored_hash: Stored hash in salt:hash format
        
    Returns:
        bool: True if password matches, False otherwise
    """
    try:
        salt, stored_pwd_hash = stored_hash.split(':')
        pwd_hash = hashlib.sha256((salt + password).encode()).hexdigest()
        return pwd_hash == stored_pwd_hash
    except (ValueError, AttributeError):
        return False


def init_db() -> None:
    """
    Initialize database with users table.
    
    Creates the users table if it doesn't exist with proper schema.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()


def get_user_by_username(username: str) -> Optional[sqlite3.Row]:
    """
    Get user by username using parameterized query.
    
    Args:
        username: Username to search for
        
    Returns:
        Optional[sqlite3.Row]: User record if found, None otherwise
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        return result


def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate user with username and password.
    
    Uses secure password hashing for verification.
    
    Args:
        username: Username to authenticate
        password: Plain text password to verify
        
    Returns:
        bool: True if authentication successful, False otherwise
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()
        
        if user and verify_password(password, user['password']):
            return True
        return False


def create_user(username: str, email: str, password: str) -> bool:
    """
    Create new user with hashed password.
    
    Args:
        username: Unique username for the user
        email: Email address for the user
        password: Plain text password (will be hashed)
        
    Returns:
        bool: True if user created successfully
        
    Raises:
        sqlite3.IntegrityError: If username already exists
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        created = datetime.now().isoformat()
        hashed_password = hash_password(password)
        
        cursor.execute(
            "INSERT INTO users (username, email, password, created_at) VALUES (?, ?, ?, ?)",
            (username, email, hashed_password, created)
        )
        conn.commit()
        return True


def get_all_users() -> List[Dict[str, any]]:
    """
    Get all users (excluding password field).
    
    Returns:
        List[Dict[str, any]]: List of user dictionaries with id, username, and email
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email FROM users")
        users = cursor.fetchall()
        
        return [
            {
                "id": user['id'],
                "username": user['username'],
                "email": user['email']
            }
            for user in users
        ]


def delete_user(user_id: int) -> None:
    """
    Delete user by ID using parameterized query.
    
    Args:
        user_id: ID of the user to delete
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()


def search_users(search_term: str) -> List[sqlite3.Row]:
    """
    Search users by username using parameterized query.
    
    Args:
        search_term: Search term to match against usernames
        
    Returns:
        List[sqlite3.Row]: List of matching user records
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username LIKE ?",
            (f"%{search_term}%",)
        )
        results = cursor.fetchall()
        return results