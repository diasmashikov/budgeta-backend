# Budget API Documentation

This document outlines the budget allocation endpoints for the Budget Tracker application.

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/budgets` | Get all budget allocations (with optional filters) |
| GET | `/api/budgets/:id` | Get a specific budget allocation |
| POST | `/api/budgets` | Create a new budget allocation |
| PUT | `/api/budgets/:id` | Update a budget allocation |
| DELETE | `/api/budgets/:id` | Delete a budget allocation |

## Request and Response DTOs

### Get All Budget Allocations

**Endpoint:** `GET /api/budgets?month=&year=`

**Query Parameters:**
- `month` (optional): Integer (1-12)
- `year` (optional): Integer

**Response DTO:** `BudgetListResponse` with list of `BudgetResponse`
```python
@dataclass
class BudgetResponse:
    budget_id: int
    category_id: int
    category_name: str
    amount: float
    month: int
    year: int
    spent_amount: float = 0.0
    remaining: float = 0.0
    percentage_used: float = 0.0

@dataclass
class BudgetListResponse:
    status: str
    budgets: List[BudgetResponse]
    total_budget: float
    total_spent: float
    total_remaining: float
```

**Example Request:**
```
GET /api/budgets?month=4&year=2025
```

**Example Success Response (200 OK):**
```json
{
  "status": "success",
  "total_budget": 2500.00,
  "total_spent": 1245.75,
  "total_remaining": 1254.25,
  "budgets": [
    {
      "budget_id": 1,
      "category_id": 1,
      "category_name": "Housing",
      "amount": 1000.00,
      "spent_amount": 800.00,
      "remaining": 200.00,
      "percentage_used": 80.0,
      "month": 4,
      "year": 2025
    },
    {
      "budget_id": 2,
      "category_id": 2,
      "category_name": "Food",
      "amount": 500.00,
      "spent_amount": 445.75,
      "remaining": 54.25,
      "percentage_used": 89.15,
      "month": 4,
      "year": 2025
    },
    {
      "budget_id": 3,
      "category_id": 3,
      "category_name": "Transportation",
      "amount": 300.00,
      "spent_amount": 0.00,
      "remaining": 300.00,
      "percentage_used": 0.0,
      "month": 4,
      "year": 2025
    },
    {
      "budget_id": 4,
      "category_id": 4,
      "category_name": "Entertainment",
      "amount": 200.00,
      "spent_amount": 0.00,
      "remaining": 200.00,
      "percentage_used": 0.0,
      "month": 4,
      "year": 2025
    },
    {
      "budget_id": 5,
      "category_id": 5,
      "category_name": "Utilities",
      "amount": 500.00,
      "spent_amount": 0.00,
      "remaining": 500.00,
      "percentage_used": 0.0,
      "month": 4,
      "year": 2025
    }
  ]
}
```

### Get Single Budget Allocation

**Endpoint:** `GET /api/budgets/:id`

**URL Parameters:**
- `id`: Budget allocation ID

**Response DTO:** `BudgetSingleResponse` with `BudgetResponse`
```python
@dataclass
class BudgetSingleResponse:
    status: str
    budget: BudgetResponse
```

**Example Request:**
```
GET /api/budgets/1
```

**Example Success Response (200 OK):**
```json
{
  "status": "success",
  "budget": {
    "budget_id": 1,
    "category_id": 1,
    "category_name": "Housing",
    "amount": 1000.00,
    "spent_amount": 800.00,
    "remaining": 200.00,
    "percentage_used": 80.0,
    "month": 4,
    "year": 2025
  }
}
```

**Example Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Budget allocation not found"
}
```

### Create Budget Allocation

**Endpoint:** `POST /api/budgets`

**Request DTO:** `CreateBudgetRequest`
```python
@dataclass
class CreateBudgetRequest:
    category_id: int
    amount: float
    month: int
    year: int
```

**Response DTO:** `BudgetSingleResponse` with `BudgetResponse`

**Example Request:**
```json
{
  "category_id": 6,
  "amount": 250.00,
  "month": 4,
  "year": 2025
}
```

**Example Success Response (201 Created):**
```json
{
  "status": "success",
  "budget": {
    "budget_id": 6,
    "category_id": 6,
    "category_name": "Healthcare",
    "amount": 250.00,
    "spent_amount": 0.00,
    "remaining": 250.00,
    "percentage_used": 0.0,
    "month": 4,
    "year": 2025
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

**Example Error Response (400 Bad Request - Duplicate):**
```json
{
  "status": "error",
  "message": "Budget allocation already exists for this category in the selected month/year"
}
```

**Example Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Category not found"
}
```

### Update Budget Allocation

**Endpoint:** `PUT /api/budgets/:id`

**URL Parameters:**
- `id`: Budget allocation ID

**Request DTO:** `UpdateBudgetRequest`
```python
@dataclass
class UpdateBudgetRequest:
    amount: float
```

**Response DTO:** `BudgetSingleResponse` with `BudgetResponse`

**Example Request:**
```json
{
  "amount": 300.00
}
```

**Example Success Response (200 OK):**
```json
{
  "status": "success",
  "budget": {
    "budget_id": 6,
    "category_id": 6,
    "category_name": "Healthcare",
    "amount": 300.00,
    "spent_amount": 0.00,
    "remaining": 300.00,
    "percentage_used": 0.0,
    "month": 4,
    "year": 2025
  }
}
```

**Example Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Budget allocation not found"
}
```

**Example Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Amount must be greater than zero"
}
```

### Delete Budget Allocation

**Endpoint:** `DELETE /api/budgets/:id`

**URL Parameters:**
- `id`: Budget allocation ID

**Example Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Budget allocation deleted successfully"
}
```

**Example Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Budget allocation not found"
}
```

## Error Responses

All budget endpoints use the following error response format:

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
| 201 | Created (for new budget allocations) |
| 400 | Bad Request (invalid input or constraints violation) |
| 401 | Unauthorized (missing or invalid token) |
| 404 | Not Found (budget allocation or category doesn't exist) |
| 500 | Server Error |

