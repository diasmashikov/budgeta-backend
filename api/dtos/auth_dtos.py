from dataclasses import dataclass
from typing import Optional


# Request DTOs
@dataclass
class RegisterRequest:
    username: str
    email: str
    password: str


@dataclass
class LoginRequest:
    username: str
    password: str


# Response DTOs
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


@dataclass
class ErrorResponse:
    status: str = "error"
    message: str = "An error occurred"
    code: Optional[str] = None