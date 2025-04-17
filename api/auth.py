from flask import Blueprint, request, jsonify
from utils.db import query_db, insert_db
from utils.auth import hash_password, verify_password, generate_token
import re
from .dtos.auth_dtos import (
    RegisterRequest, 
    LoginRequest, 
    UserResponse, 
    AuthResponse, 
    ErrorResponse
)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        req = RegisterRequest(
            username=data.get('username', ''),
            email=data.get('email', ''),
            password=data.get('password', '')
        )
        
        if not req.username or not req.email or not req.password:
            return jsonify({
                'status': 'error',
                'message': 'Username, email and password are required'
            }), 400
        
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, req.email):
            return jsonify({
                'status': 'error',
                'message': 'Invalid email format'
            }), 400
        
        existing_user = query_db(
            'SELECT * FROM users WHERE username = ? OR email = ?',
            (req.username, req.email),
            one=True
        )
        
        if existing_user:
            return jsonify({
                'status': 'error',
                'message': 'Username or email already exists'
            }), 400
        
        password_hash = hash_password(req.password)
        user_id = insert_db(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (req.username, req.email, password_hash)
        )
        
        default_categories = ['Housing', 'Food', 'Transportation', 'Entertainment', 'Utilities']
        for category in default_categories:
            insert_db(
                'INSERT INTO categories (user_id, name) VALUES (?, ?)',
                (user_id, category)
            )
        
        user_res = UserResponse(
            user_id=user_id,
            username=req.username,
            email=req.email
        )
        
        auth_res = AuthResponse(
            status="success",
            message="User registered successfully",
            user=user_res
        )
        
        return jsonify(vars(auth_res)), 201
        
    except Exception as e:
        error_res = ErrorResponse(message=f"Database error: {str(e)}")
        return jsonify(vars(error_res)), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        req = LoginRequest(
            username=data.get('username', ''),
            password=data.get('password', '')
        )
        
        if not req.username or not req.password:
            return jsonify({
                'status': 'error',
                'message': 'Username and password are required'
            }), 400
        
        user = query_db(
            'SELECT * FROM users WHERE username = ?',
            (req.username,),
            one=True
        )
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'Invalid username or password'
            }), 401
        
        if not verify_password(user['password_hash'], req.password):
            return jsonify({
                'status': 'error',
                'message': 'Invalid username or password'
            }), 401
        
        token = generate_token(user['user_id'])
        
        user_res = UserResponse(
            user_id=user['user_id'],
            username=user['username'],
            email=user['email']
        )
        
        auth_res = AuthResponse(
            status="success",
            message="Login successful",
            user=user_res,
            token=token
        )
        
        return jsonify(vars(auth_res))
        
    except Exception as e:
        error_res = ErrorResponse(message=f"Error during login: {str(e)}")
        return jsonify(vars(error_res)), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    auth_res = AuthResponse(
        status="success",
        message="Logged out successfully"
    )
    return jsonify(vars(auth_res))