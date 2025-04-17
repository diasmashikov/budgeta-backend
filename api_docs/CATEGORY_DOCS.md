# Category API Documentation

This document outlines the category management endpoints for the Budget Tracker application.

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories` | Get all categories for the current user |
| POST | `/api/categories` | Create a new category |
| PUT | `/api/categories/:id` | Update a category |
| DELETE | `/api/categories/:id` | Delete a category |

## Request and Response DTOs

### Get All Categories

**Endpoint:** `GET /api/categories`

**Response DTO:** `CategoryListResponse` with list of `CategoryResponse`
```python
@dataclass
class CategoryResponse:
    category_id: int
    name: str

@dataclass
class CategoryListResponse:
    status: str
    categories: List[CategoryResponse]
```

**Example Request:**
```
GET /api/categories
```

**Example Success Response (200 OK):**
```json
{
  "status": "success",
  "categories": [
    {
      "category_id": 1,
      "name": "Housing"
    },
    {
      "category_id": 2,
      "name": "Food"
    },
    {
      "category_id": 3,
      "name": "Transportation"
    },
    {
      "category_id": 4,
      "name": "Entertainment"
    },
    {
      "category_id": 5,
      "name": "Utilities"
    }
  ]
}
```

### Create Category

**Endpoint:** `POST /api/categories`

**Request DTO:** `CreateCategoryRequest`
```python
@dataclass
class CreateCategoryRequest:
    name: str
```

**Response DTO:** `CategorySingleResponse` with `CategoryResponse`
```python
@dataclass
class CategorySingleResponse:
    status: str
    category: CategoryResponse
```

**Example Request:**
```json
{
  "name": "Healthcare"
}
```

**Example Success Response (201 Created):**
```json
{
  "status": "success",
  "category": {
    "category_id": 6,
    "name": "Healthcare"
  }
}
```

**Example Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Category name is required"
}
```

**Example Error Response (400 Bad Request - Duplicate):**
```json
{
  "status": "error",
  "message": "Category with this name already exists"
}
```

### Update Category

**Endpoint:** `PUT /api/categories/:id`

**URL Parameters:**
- `id`: Category ID

**Request DTO:** `UpdateCategoryRequest`
```python
@dataclass
class UpdateCategoryRequest:
    name: str
```

**Response DTO:** `CategorySingleResponse` with `CategoryResponse`

**Example Request:**
```json
{
  "name": "Medical Expenses"
}
```

**Example Success Response (200 OK):**
```json
{
  "status": "success",
  "category": {
    "category_id": 6,
    "name": "Medical Expenses"
  }
}
```

**Example Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Category not found"
}
```

### Delete Category

**Endpoint:** `DELETE /api/categories/:id`

**URL Parameters:**
- `id`: Category ID

**Example Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Category deleted successfully"
}
```

**Example Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Category not found"
}
```

**Example Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Cannot delete category with associated budget allocations or expenses"
}
```

## Error Responses

All category endpoints use the following error response format:

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
| 201 | Created (for new categories) |
| 400 | Bad Request (invalid input or constraints violation) |
| 401 | Unauthorized (missing or invalid token) |
| 404 | Not Found (category doesn't exist) |
| 500 | Server Error |
