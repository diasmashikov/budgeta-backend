from flask import request, jsonify
from http import HTTPStatus
from auth.service import AuthService
from auth.dto import RegisterRequest, LoginRequest, AuthResponse, ErrorResponse
from auth import auth_bp

auth_service = AuthService()

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        req = RegisterRequest(
            username=data.get('username', ''),
            email=data.get('email', ''),
            password=data.get('password', '')
        )
        
        try:
            user = auth_service.register_user(req.username, req.email, req.password)
            
            auth_res = AuthResponse(
                status="success",
                message="User registered successfully",
                user=user
            )
            
            return jsonify(vars(auth_res)), HTTPStatus.CREATED
            
        except ValueError as e:
            error_res = ErrorResponse(message=str(e))
            return jsonify(vars(error_res)), HTTPStatus.BAD_REQUEST
        
    except Exception as e:
        error_res = ErrorResponse(message=f"Database error: {str(e)}")
        return jsonify(vars(error_res)), HTTPStatus.INTERNAL_SERVER_ERROR

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        req = LoginRequest(
            username=data.get('username', ''),
            password=data.get('password', '')
        )
        
        try:
            user, token = auth_service.login_user(req.username, req.password)
            
            auth_res = AuthResponse(
                status="success",
                message="Login successful",
                user=user,
                token=token
            )
            print(f"User {user.username} logged in successfully.")
            print(f"Token: {token}")
            
            return jsonify(vars(auth_res)), HTTPStatus.OK
            
        except ValueError as e:
            error_res = ErrorResponse(message=str(e))
            return jsonify(vars(error_res)), HTTPStatus.UNAUTHORIZED
        
    except Exception as e:
        error_res = ErrorResponse(message=f"Error during login: {str(e)}")
        return jsonify(vars(error_res)), HTTPStatus.INTERNAL_SERVER_ERROR

@auth_bp.route('/logout', methods=['POST'])
def logout():
    auth_res = AuthResponse(
        status="success",
        message="Logged out successfully"
    )
    return jsonify(vars(auth_res)), HTTPStatus.OK