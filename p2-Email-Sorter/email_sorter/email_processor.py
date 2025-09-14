"""
Email processor module for validating and filtering email addresses.
"""

import re


class EmailProcessor:
    def __init__(self):
        # Email validation regex - basic pattern that checks for @ and domain
        self.email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def remove_duplicates(self, emails):
        """
        Remove duplicate emails from the list.
        
        Args:
            emails (list): List of email strings
            
        Returns:
            list: List with duplicates removed, preserving original order
        """
        # Use dict.fromkeys to preserve order while removing duplicates
        return list(dict.fromkeys(emails))
    
    def remove_invalid(self, emails):
        """
        Remove invalid emails from the list.
        An email is considered invalid if it:
        - Does not contain '@'
        - Contains special characters like '/' or ','
        - Does not match the email regex pattern
        
        Args:
            emails (list): List of email strings
            
        Returns:
            list: List with invalid emails removed
        """
        valid_emails = []
        for email in emails:
            email = email.strip()
            if email and self.is_valid_email(email):
                valid_emails.append(email)
        return valid_emails
    
    def is_valid_email(self, email):
        """
        Check if an email is valid.
        
        Args:
            email (str): Email string to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not email or '@' not in email:
            return False
        
        # Check for problematic special characters
        if any(char in email for char in [',', '/', '\\', ' ']):
            return False
        
        # Use regex for more comprehensive validation
        return bool(self.email_pattern.match(email))
