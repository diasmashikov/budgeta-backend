# Dashboard API Documentation

This document outlines the dashboard/overview endpoints for the Budget Tracker application.

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard` | Get financial overview for specified month/year |
| GET | `/api/dashboard/savings` | Get savings summary across all months |

## Request and Response DTOs

### Get Financial Overview

**Endpoint:** `GET /api/dashboard?month=&year=`

**Query Parameters:**
- `month`: Integer (1-12)
- `year`: Integer

**Response DTO:** `DashboardResponse`
```python
@dataclass
class BalanceInfo:
    expected_income: float
    actual_income: float
    total_expenses: float
    remaining_budget: float

@dataclass
class CategorySummary:
    category_id: int
    category_name: str
    budget_amount: float
    spent_amount: float
    remaining: float
    percentage_used: float

@dataclass
class Transaction:
    type: str  # 'expense' or 'income'
    id: int
    amount: float
    category_name: str = None  # For expenses
    source_name: str = None    # For income
    date: date = None
    description: str = None

@dataclass
class DashboardResponse:
    status: str
    month: int
    year: int
    balance: BalanceInfo
    budget_summary: List[CategorySummary]
    recent_transactions: List[Transaction]
    savings: float = 0.0
```

**Example Request:**
```
GET /api/dashboard?month=4&year=2025
```

**Example Success Response (200 OK):**
```json
{
  "status": "success",
  "month": 4,
  "year": 2025,
  "balance": {
    "expected_income": 5000.00,
    "actual_income": 3000.00,
    "total_expenses": 1245.75,
    "remaining_budget": 1754.25
  },
  "budget_summary": [
    {
      "category_id": 1,
      "category_name": "Housing",
      "budget_amount": 1000.00,
      "spent_amount": 800.00,
      "remaining": 200.00,
      "percentage_used": 80.0
    },
    {
      "category_id": 2,
      "category_name": "Food",
      "budget_amount": 500.00,
      "spent_amount": 445.75,
      "remaining": 54.25,
      "percentage_used": 89.15
    },
    {
      "category_id": 3,
      "category_name": "Transportation",
      "budget_amount": 300.00,
      "spent_amount": 0.00,
      "remaining": 300.00,
      "percentage_used": 0.0
    },
    {
      "category_id": 4,
      "category_name": "Entertainment",
      "budget_amount": 200.00,
      "spent_amount": 0.00,
      "remaining": 200.00,
      "percentage_used": 0.0
    },
    {
      "category_id": 5,
      "category_name": "Utilities",
      "budget_amount": 500.00,
      "spent_amount": 0.00,
      "remaining": 500.00,
      "percentage_used": 0.0
    }
  ],
  "recent_transactions": [
    {
      "type": "expense",
      "id": 1,
      "amount": 800.00,
      "category_name": "Housing",
      "date": "2025-04-01",
      "description": "April rent"
    },
    {
      "type": "expense",
      "id": 2,
      "amount": 45.75,
      "category_name": "Food",
      "date": "2025-04-03",
      "description": "Grocery shopping"
    },
    {
      "type": "income",
      "id": 1,
      "amount": 3000.00,
      "source_name": "Salary",
      "date": "2025-04-05",
      "description": "Monthly salary"
    },
    {
      "type": "expense",
      "id": 3,
      "amount": 400.00,
      "category_name": "Food",
      "date": "2025-04-10",
      "description": "Restaurant meals"
    }
  ],
  "savings": 500.00
}
```

### Get Savings Summary

**Endpoint:** `GET /api/dashboard/savings`

**Response DTO:**
```python
@dataclass
class SavingsPeriod:
    month: int
    year: int
    amount: float

@dataclass
class SavingsSummaryResponse:
    status: str
    total_savings: float
    savings_by_period: List[SavingsPeriod]
```

**Example Request:**
```
GET /api/dashboard/savings
```

**Example Success Response (200 OK):**
```json
{
  "status": "success",
  "total_savings": 1750.00,
  "savings_by_period": [
    {
      "month": 1,
      "year": 2025,
      "amount": 500.00
    },
    {
      "month": 2,
      "year": 2025,
      "amount": 750.00
    },
    {
      "month": 3,
      "year": 2025,
      "amount": 0.00
    },
    {
      "month": 4,
      "year": 2025,
      "amount": 500.00
    }
  ]
}
```

## Error Responses

All dashboard endpoints use the following error response format:

```python
@dataclass
class ErrorResponse:
    status: str = "error"
    message: str = "An error occurred"
    code: Optional[str] = None
```

**Example Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Month and year are required"
}
```

## HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid or missing parameters) |
| 401 | Unauthorized (missing or invalid token) |
| 500 | Server Error |
