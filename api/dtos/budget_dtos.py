from dataclasses import dataclass
from typing import Optional, List


# Request DTOs
@dataclass
class CreateBudgetRequest:
    category_id: int
    amount: float
    month: int
    year: int


@dataclass
class UpdateBudgetRequest:
    amount: float


# Response DTOs
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


@dataclass
class BudgetSingleResponse:
    status: str
    budget: BudgetResponse