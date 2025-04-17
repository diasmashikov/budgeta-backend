# Income API Documentation

This document outlines the income management endpoints for the Budget Tracker application.

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/income` | Get all income sources (with optional filters) |
| GET | `/api/income/:id` | Get a specific income source |
| POST | `/api/income` | Add a new income source |
| PUT | `/api/income/:id` | Update an income source |
| PATCH | `/api/income/:id/receive` | Mark income as received with actual amount |
| DELETE | `/api/income/:id` | Delete an income source |

## Request and Response DTOs

### Get All Income Sources

**Endpoint:** `GET /api/income?month=&year=`

**Query Parameters:**
- `month` (optional): Integer (1-12)
- `year` (optional): Integer

**Response DTO:** `IncomeListResponse` with list of `IncomeResponse`
```python
@dataclass
class IncomeResponse:
    income_id: int
    source_name: str
    expected_amount: float
    month: int
    year: int
    is_received: bool
    actual_amount: Optional[float] = None
    due_date: Optional[date] = None
    receive_date: Optional[date] = None
    description: Optional[str] = None

@dataclass
class IncomeListResponse:
    status: str
    incomes: List[IncomeResponse]
    total_expected: float
    total_received: float
```

**Example Request:**
```
GET /api/income?month=4&year=2025
```

**Example Success Response (200 OK):**
```json
{
  "status": "success",
  "total_expected": 5000.00,
  "total_received": 3000.00,
  "incomes": [
    {
      "income_id": 1,
      "source_name": "Salary",
      "expected_amount": 3000.00,
      "actual_amount": 3000.00,
      "is_received": true,
      "due_date": "2025-04-25",
      "receive_date": "2025-04-25",
      "month": 4,
      "year": 2025,
      "description": "Monthly salary"
    },
    {
      "income_id": 2,
      "source_name": "Freelance",
      "expected_amount": 2000.00,
      "is_received": false,
      "due_date": "2025-04-30",
      "month": 4,
      "year": 2025,
      "description": "Client project"
    }
  ]
}
```

### Get Single Income Source

**Endpoint:** `GET /api/income/:id`

**URL Parameters:**
- `id`: Income source ID

**Response DTO:** `IncomeSingleResponse` with `IncomeResponse`
```python
@dataclass
class IncomeSingleResponse:
    status: str
    income: IncomeResponse
```

**Example Request:**
```
GET /api/income/1
```

**Example Success Response (200 OK):**
```json
{
  "status": "success",
  "income": {
    "income_id": 1,
    "source_name": "Salary",
    "expected_amount": 3000.00,
    "actual_amount": 3000.00,
    "is_received": true,
    "due_date": "2025-04-25",
    "receive_date": "2025-04-25",
    "month": 4,
    "year": 2025,
    "description": "Monthly salary"
  }
}
```

**Example Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Income source not found"
}
```

### Create Income Source

**Endpoint:** `POST /api/income`

**Request DTO:** `CreateIncomeRequest`
```python
@dataclass
class CreateIncomeRequest:
    source_name: str
    expected_amount: float
    month: int
    year: int
    due_date: Optional[date] = None
    description: Optional[str] = None
```

**Response DTO:** `IncomeSingleResponse` with `IncomeResponse`

**Example Request:**
```json
{
  "source_name": "Bonus",
  "expected_amount": 1000.00,
  "month": 4,
  "year": 2025,
  "due_date": "2025-04-30",
  "description": "Performance bonus"
}
```

**Example Success Response (201 Created):**
```json
{
  "status": "success",
  "income": {
    "income_id": 3,
    "source_name": "Bonus",
    "expected_amount": 1000.00,
    "is_received": false,
    "due_date": "2025-04-30",
    "month": 4,
    "year": 2025,
    "description": "Performance bonus"
  }
}
```

**Example Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Expected amount must be greater than zero"
}
```

### Update Income Source

**Endpoint:** `PUT /api/income/:id`

**URL Parameters:**
- `id`: Income source ID

**Request DTO:** `UpdateIncomeRequest`
```python
@dataclass
class UpdateIncomeRequest:
    source_name: Optional[str] = None
    expected_amount: Optional[float] = None
    actual_amount: Optional[float] = None
    is_received: Optional[bool] = None
    due_date: Optional[date] = None
    receive_date: Optional[date] = None
    month: Optional[int] = None
    year: Optional[int] = None
    description: Optional[str] = None
```

**Response DTO:** `IncomeSingleResponse` with `IncomeResponse`

**Example Request:**
```json
{
  "source_name": "Quarterly Bonus",
  "expected_amount": 1500.00,
  "description": "Q2 performance bonus"
}
```

**Example Success Response (200 OK):**
```json
{
  "status": "success",
  "income": {
    "income_id": 3,
    "source_name": "Quarterly Bonus",
    "expected_amount": 1500.00,
    "is_received": false,
    "due_date": "2025-04-30",
    "month": 4,
    "year": 2025,
    "description": "Q2 performance bonus"
  }
}
```

**Example Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Income source not found"
}
```

### Mark Income as Received

**Endpoint:** `PATCH /api/income/:id/receive`

**URL Parameters:**
- `id`: Income source ID

**Request DTO:** `ReceiveIncomeRequest`
```python
@dataclass
class ReceiveIncomeRequest:
    actual_amount: float
    receive_date: Optional[date] = None
```

**Response DTO:** `IncomeSingleResponse` with `IncomeResponse`

**Example Request:**
```json
{
  "actual_amount": 1550.00,
  "receive_date": "2025-04-28"
}
```

**Example Success Response (200 OK):**
```json
{
  "status": "success",
  "income": {
    "income_id": 3,
    "source_name": "Quarterly Bonus",
    "expected_amount": 1500.00,
    "actual_amount": 1550.00,
    "is_received": true,
    "due_date": "2025-04-30",
    "receive_date": "2025-04-28",
    "month": 4,
    "year": 2025,
    "description": "Q2 performance bonus"
  }
}
```

**Example Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Actual amount cannot be negative"
}
```

### Delete Income Source

**Endpoint:** `DELETE /api/income/:id`

**URL Parameters:**
- `id`: Income source ID

**Example Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Income source deleted successfully"
}
```

**Example Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Income source not found"
}
```

## Error Responses

All income endpoints use the following error response format:

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
| 201 | Created (for new income sources) |
| 400 | Bad Request (invalid input) |
| 401 | Unauthorized (missing or invalid token) |
| 404 | Not Found (income source doesn't exist) |
| 500 | Server Error |
