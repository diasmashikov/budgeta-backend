import os
from flask import request, jsonify, current_app, g
from functools import wraps
from datetime import datetime, timedelta, timezone
import jwt
import bcrypt
from utils.db import query_db

def hash_password(password):
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt(12))
    return hashed.decode('utf-8')

def verify_password(stored_hash, provided_password):
    password_bytes = provided_password.encode('utf-8')
    stored_hash_bytes = stored_hash.encode('utf-8')
    return bcrypt.checkpw(password_bytes, stored_hash_bytes)

def generate_token(user_id):
    now = datetime.now(timezone.utc)
    payload = {
        'exp': now + timedelta(seconds=current_app.config['JWT_ACCESS_TOKEN_EXPIRES']),
        'iat': now,
        'sub': str(user_id)
    }
    return jwt.encode(
        payload,
        current_app.config['JWT_SECRET_KEY'],
        algorithm='HS256'
    )

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                
        if not token:
            return jsonify({
                'status': 'error',
                'message': 'Authentication token is missing'
            }), 401
            
        try:
            data = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )
            
            user = query_db(
                'SELECT * FROM users WHERE user_id = ?',
                (data['sub'],),
                one=True
            )
            
            if not user:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid user'
                }), 401
                
            g.user = user
            
        except jwt.ExpiredSignatureError:
            return jsonify({
                'status': 'error',
                'message': 'Token has expired'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'status': 'error',
                'message': 'Invalid token'
            }), 401
            
        return f(*args, **kwargs)
        
    return decorated