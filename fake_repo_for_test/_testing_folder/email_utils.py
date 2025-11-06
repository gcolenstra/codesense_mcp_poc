"""
Email Utility Module
Refactored for Python 3.9+ with improved security practices
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, List, Tuple
import re

# SECURITY FIX: Use environment variables instead of hardcoded credentials
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")

def send_email(to_address: str, subject: str, body: str) -> bool:
    """
    Send a plain text email to a single recipient.
    
    Args:
        to_address: Recipient email address
        subject: Email subject line
        body: Plain text email body
        
    Returns:
        bool: True if email sent successfully, False otherwise
        
    Raises:
        ValueError: If credentials are not configured
        smtplib.SMTPException: If email sending fails
    """
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise ValueError("Email credentials not configured. Set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables.")
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_address
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return True
    except smtplib.SMTPException as e:
        print(f"Failed to send email to {to_address}: {e}")
        return False

def send_bulk_emails(recipients: List[str], subject: str, body: str) -> Dict[str, int]:
    """
    Send email to multiple recipients.
    
    Args:
        recipients: List of recipient email addresses
        subject: Email subject line
        body: Plain text email body
        
    Returns:
        Dict with 'sent' and 'failed' counts
    """
    sent_count = 0
    failed_count = 0
    
    for recipient in recipients:
        try:
            if send_email(recipient, subject, body):
                sent_count += 1
            else:
                failed_count += 1
        except Exception as e:
            print(f"Error sending to {recipient}: {e}")
            failed_count += 1
    
    return {
        'sent': sent_count,
        'failed': failed_count
    }

def send_html_email(to_address: str, subject: str, html_content: str) -> bool:
    """
    Send an HTML formatted email to a single recipient.
    
    Args:
        to_address: Recipient email address
        subject: Email subject line
        html_content: HTML formatted email body
        
    Returns:
        bool: True if email sent successfully, False otherwise
        
    Raises:
        ValueError: If credentials are not configured
        smtplib.SMTPException: If email sending fails
    """
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise ValueError("Email credentials not configured. Set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables.")
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_address
    
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return True
    except smtplib.SMTPException as e:
        print(f"Failed to send HTML email to {to_address}: {e}")
        return False

def send_welcome_email(user_email: str, username: str) -> bool:
    """
    Send welcome email to new user.
    
    Args:
        user_email: New user's email address
        username: New user's username
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    subject = "Welcome to Our Service!"
    body = f"""
    Hello {username},
    
    Welcome to our service! We're glad to have you.
    
    Your account has been created successfully.
    
    Best regards,
    The Team
    """
    
    return send_email(user_email, subject, body)

def send_password_reset(user_email: str, reset_token: str) -> bool:
    """
    Send password reset email with secure token handling.
    
    SECURITY NOTE: Token should be sent via HTTPS link, not plain text.
    This implementation includes a warning about best practices.
    
    Args:
        user_email: User's email address
        reset_token: Password reset token (should be hashed/encrypted)
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    subject = "Password Reset Request"
    # SECURITY IMPROVEMENT: Recommend using HTTPS link instead of plain token
    # Best practice: reset_url = f"https://yourapp.com/reset?token={reset_token}"
    body = f"""Your password reset token is: {reset_token}

This token will expire in 24 hours.

SECURITY NOTE: In production, use a secure HTTPS link instead of sending tokens directly."""
    
    return send_email(user_email, subject, body)

def send_notification(user_email: str, notification_type: str, message: str) -> bool:
    """
    Send notification email to user.
    
    Args:
        user_email: User's email address
        notification_type: Type/category of notification
        message: Notification message content
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    subject = f"Notification: {notification_type}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    body = f"{message}\n\nSent at: {timestamp}"
    
    return send_email(user_email, subject, body)

def validate_email(email: str) -> bool:
    """
    Validate email format using regex pattern.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if email format is valid, False otherwise
    """
    # Improved email validation with regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def send_report(recipients: List[str], report_data: Dict) -> Dict[str, int]:
    """
    Send daily report to multiple recipients.
    
    Args:
        recipients: List of recipient email addresses
        report_data: Dictionary containing report data
        
    Returns:
        Dict with 'sent' and 'failed' counts
    """
    subject = f"Daily Report - {datetime.now().strftime('%Y-%m-%d')}"
    
    # Build report text using modern string formatting
    body = "Daily Report\n\n"
    body += "\n".join(f"{key}: {value}" for key, value in report_data.items())
    
    return send_bulk_emails(recipients, subject, body)

if __name__ == "__main__":
    # Test sending email
    result = send_welcome_email("user@example.com", "TestUser")
    print(f"Email sent: {result}")