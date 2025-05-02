from dataclasses import dataclass
from typing import Optional, List
from datetime import date


# Request DTOs
@dataclass
class CreateExpenseRequest:
    category_id: int
    amount: float
    date: date
    description: Optional[str] = None


@dataclass
class UpdateExpenseRequest:
    category_id: Optional[int] = None
    amount: Optional[float] = None
    expense_data: Optional[date] = None
    description: Optional[str] = None


# Response DTOs
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


@dataclass
class ExpenseSingleResponse:
    status: str
    expense: ExpenseResponse