# Authentication API Documentation

This document outlines the authentication endpoints for the Budget Tracker application.

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login and get authentication token |
| POST | `/api/auth/logout` | Logout user |

## Request and Response DTOs

### Register User

**Endpoint:** `POST /api/auth/register`

**Request DTO:** `RegisterRequest`
```python
@dataclass
class RegisterRequest:
    username: str
    email: str
    password: str
```

**Response DTO:** `AuthResponse` with `UserResponse`
```python
@dataclass
class UserResponse:
    user_id: int
    username: str
    email: str

@dataclass
class AuthResponse:
    status: str
    message: str
    user: Optional[UserResponse] = None
    token: Optional[str] = None
```

**Example Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

**Example Success Response (201 Created):**
```json
{
  "status": "success",
  "message": "User registered successfully",
  "user": {
    "user_id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

**Example Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Username or email already exists"
}
```

### Login User

**Endpoint:** `POST /api/auth/login`

**Request DTO:** `LoginRequest`
```python
@dataclass
class LoginRequest:
    username: str
    password: str
```

**Response DTO:** `AuthResponse` with `UserResponse` and token
```python
@dataclass
class AuthResponse:
    status: str
    message: str
    user: Optional[UserResponse] = None
    token: Optional[str] = None
```

**Example Request:**
```json
{
  "username": "john_doe",
  "password": "secure_password"
}
```

**Example Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Login successful",
  "user": {
    "user_id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Example Error Response (401 Unauthorized):**
```json
{
  "status": "error",
  "message": "Invalid username or password"
}
```

### Logout User

**Endpoint:** `POST /api/auth/logout`

**Request:** No body required, but should include Authorization header with bearer token

**Response DTO:** `AuthResponse`
```python
@dataclass
class AuthResponse:
    status: str
    message: str
    user: Optional[UserResponse] = None
    token: Optional[str] = None
```

**Example Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Logged out successfully"
}
```

## Error Responses

All authentication endpoints use the following error response format:

```python
@dataclass
class ErrorResponse:
    status: str = "error"
    message: str = "An error occurred"
    code: Optional[str] = None
```

## HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created (for register endpoint) |
| 400 | Bad Request (invalid input) |
| 401 | Unauthorized (invalid credentials) |
| 500 | Server Error |

## Authentication Flow

1. Register a user account using the register endpoint
2. Login with the created credentials to obtain a JWT token
3. Include the token in the Authorization header for subsequent requests:
   ```
   Authorization: Bearer <token>
   ```
4. Use the logout endpoint when the user wishes to end their session

