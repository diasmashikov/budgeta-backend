from auth.repository import AuthRepository
from utils.auth import hash_password, verify_password, generate_token
from auth.dto import UserResponse
import re

class AuthService:
    def __init__(self):
        self.repository = AuthRepository()
        self.default_categories = ['Housing', 'Food', 'Transportation', 'Entertainment', 'Utilities']
    
    def validate_registration(self, username, email, password):
        # Check for empty fields
        if not username or not email or not password:
            return False, "Username, email and password are required"
        
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        
        # Check if username or email already exists
        existing_user = self.repository.find_user_by_username_or_email(username, email)
        if existing_user:
            return False, "Username or email already exists"
        
        return True, ""
    
    def register_user(self, username, email, password):
        # Validate registration data
        is_valid, error_message = self.validate_registration(username, email, password)
        if not is_valid:
            raise ValueError(error_message)
        
        # Hash password and create user
        password_hash = hash_password(password)
        user_id = self.repository.create_user(username, email, password_hash)
        
        # Create default categories
        self.repository.create_default_categories(user_id, self.default_categories)
        
        # Return user response
        return UserResponse(
            user_id=user_id,
            username=username,
            email=email
        )
    
    def login_user(self, username, password):
        # Check for empty fields
        if not username or not password:
            raise ValueError("Username and password are required")
        
        # Find user by username
        user = self.repository.find_user_by_username(username)
        if not user:
            raise ValueError("Invalid username or password")
        
        # Verify password
        if not verify_password(user['password_hash'], password):
            raise ValueError("Invalid username or password")
        
        # Generate token
        token = generate_token(user['user_id'])
        
        # Return user response and token
        return UserResponse(
            user_id=user['user_id'],
            username=user['username'],
            email=user['email']
        ), token