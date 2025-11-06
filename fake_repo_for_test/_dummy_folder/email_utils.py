"""
Email Utility Module
Legacy code with security issues
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# SECURITY ISSUE: Hardcoded credentials!
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "admin@company.com"
EMAIL_PASSWORD = "mypassword123"  # Never do this!

def send_email(to_address, subject, body):
    """Send email - with hardcoded credentials"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_address
    
    # No error handling
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()
    
    return True

def send_bulk_emails(recipients, subject, body):
    """Send email to multiple recipients - inefficient"""
    sent_count = 0
    failed_count = 0
    
    for recipient in recipients:
        try:
            send_email(recipient, subject, body)
            sent_count = sent_count + 1
        except:
            failed_count = failed_count + 1
    
    return {
        'sent': sent_count,
        'failed': failed_count
    }

def send_html_email(to_address, subject, html_content):
    """Send HTML email"""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_address
    
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)
    
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

def send_welcome_email(user_email, username):
    """Send welcome email to new user"""
    subject = "Welcome to Our Service!"
    body = """
    Hello %s,
    
    Welcome to our service! We're glad to have you.
    
    Your account has been created successfully.
    
    Best regards,
    The Team
    """ % username
    
    return send_email(user_email, subject, body)

def send_password_reset(user_email, reset_token):
    """Send password reset email - SECURITY ISSUE: token in plain text"""
    subject = "Password Reset Request"
    # SECURITY ISSUE: Sending token in email without encryption
    body = "Your password reset token is: %s" % reset_token
    body = body + "\n\nThis token will expire in 24 hours."
    
    return send_email(user_email, subject, body)

def send_notification(user_email, notification_type, message):
    """Send notification email"""
    subject = "Notification: " + notification_type
    body = message + "\n\nSent at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return send_email(user_email, subject, body)

def validate_email(email):
    """Validate email format - very basic"""
    if '@' in email and '.' in email:
        return True
    return False

def send_report(recipients, report_data):
    """Send report to multiple recipients"""
    subject = "Daily Report - " + datetime.now().strftime("%Y-%m-%d")
    
    # Build report text
    body = "Daily Report\n\n"
    for key in report_data:
        body = body + key + ": " + str(report_data[key]) + "\n"
    
    return send_bulk_emails(recipients, subject, body)

if __name__ == "__main__":
    # Test sending email
    result = send_welcome_email("user@example.com", "TestUser")
    print("Email sent:", result)