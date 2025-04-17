# Expenses API Documentation

This document outlines the expense management endpoints for the Budget Tracker application.

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/expenses` | Get all expenses (with optional filters) |
| GET | `/api/expenses/:id` | Get a specific expense |
| POST | `/api/expenses` | Add a new expense |
| PUT | `/api/expenses/:id` | Update an expense |
| DELETE | `/api/expenses/:id` | Delete an expense |

## Request and Response DTOs

### Get All Expenses

**Endpoint:** `GET /api/expenses?month=&year=&category=`

**Query Parameters:**
- `month` (optional): Integer (1-12)
- `year` (optional): Integer
- `category` (optional): Category ID

**Response DTO:** `ExpenseListResponse` with list of `ExpenseResponse`
```python
@dataclass
class ExpenseResponse:
    expense_id: int
    category_id: int
    category_name: str
    amount: float
    date: date
    description: Optional[str] = None

@dataclass
class ExpenseListResponse:
    status: str
    expenses: List[ExpenseResponse]
    total_amount: float
```

**Example Request:**
```
GET /api/expenses?month=4&year=2025
```

**Example Success Response (200 OK):**
```json
{
  "status": "success",
  "total_amount": 1245.75,
  "expenses": [
    {
      "expense_id": 1,
      "category_id": 1,
      "category_name": "Housing",
      "amount": 800.00,
      "date": "2025-04-01",
      "description": "April rent"
    },
    {
      "expense_id": 2,
      "category_id": 2,
      "category_name": "Food",
      "amount": 45.75,
      "date": "2025-04-03",
      "description": "Grocery shopping"
    },
    {
      "expense_id": 3,
      "category_id": 2,
      "category_name": "Food",
      "amount": 400.00,
      "date": "2025-04-10",
      "description": "Restaurant meals"
    }
  ]
}
```

### Get Single Expense

**Endpoint:** `GET /api/expenses/:id`

**URL Parameters:**
- `id`: Expense ID

**Response DTO:** `ExpenseSingleResponse` with `ExpenseResponse`
```python
@dataclass
class ExpenseSingleResponse:
    status: str
    expense: ExpenseResponse
```

**Example Request:**
```
GET /api/expenses/2
```

**Example Success Response (200 OK):**
```json
{
  "status": "success",
  "expense": {
    "expense_id": 2,
    "category_id": 2,
    "category_name": "Food",
    "amount": 45.75,
    "date": "2025-04-03",
    "description": "Grocery shopping"
  }
}
```

**Example Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Expense not found"
}
```

### Create Expense

**Endpoint:** `POST /api/expenses`

**Request DTO:** `CreateExpenseRequest`
```python
@dataclass
class CreateExpenseRequest:
    category_id: int
    amount: float
    date: date
    description: Optional[str] = None
```

**Response DTO:** `ExpenseSingleResponse` with `ExpenseResponse`

**Example Request:**
```json
{
  "category_id": 5,
  "amount": 85.50,
  "date": "2025-04-15",
  "description": "Electricity bill"
}
```

**Example Success Response (201 Created):**
```json
{
  "status": "success",
  "expense": {
    "expense_id": 4,
    "category_id": 5,
    "category_name": "Utilities",
    "amount": 85.50,
    "date": "2025-04-15",
    "description": "Electricity bill"
  }
}
```

**Example Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Amount must be greater than zero"
}
```

**Example Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Category not found"
}
```

### Update Expense

**Endpoint:** `PUT /api/expenses/:id`

**URL Parameters:**
- `id`: Expense ID

**Request DTO:** `UpdateExpenseRequest`
```python
@dataclass
class UpdateExpenseRequest:
    category_id: Optional[int] = None
    amount: Optional[float] = None
    date: Optional[date] = None
    description: Optional[str] = None
```

**Response DTO:** `ExpenseSingleResponse` with `ExpenseResponse`

**Example Request:**
```json
{
  "amount": 90.25,
  "description": "Electricity and water bill"
}
```

**Example Success Response (200 OK):**
```json
{
  "status": "success",
  "expense": {
    "expense_id": 4,
    "category_id": 5,
    "category_name": "Utilities",
    "amount": 90.25,
    "date": "2025-04-15",
    "description": "Electricity and water bill"
  }
}
```

**Example Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Expense not found"
}
```

**Example Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Amount must be greater than zero"
}
```

### Delete Expense

**Endpoint:** `DELETE /api/expenses/:id`

**URL Parameters:**
- `id`: Expense ID

**Example Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Expense deleted successfully"
}
```

**Example Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Expense not found"
}
```

## Error Responses

All expense endpoints use the following error response format:

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
| 201 | Created (for new expenses) |
| 400 | Bad Request (invalid input) |
| 401 | Unauthorized (missing or invalid token) |
| 404 | Not Found (expense or category doesn't exist) |
| 500 | Server Error |


