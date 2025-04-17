from dataclasses import dataclass
from typing import Optional, List


# Request DTOs
@dataclass
class CreateCategoryRequest:
    name: str


@dataclass
class UpdateCategoryRequest:
    name: str


# Response DTOs
@dataclass
class CategoryResponse:
    category_id: int
    name: str


@dataclass
class CategoryListResponse:
    status: str
    categories: List[CategoryResponse]


@dataclass
class CategorySingleResponse:
    status: str
    category: CategoryResponse