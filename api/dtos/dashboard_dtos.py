from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import date


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
    type: str  # expense or income
    id: int
    amount: float
    category_name: str = None  # For expenses
    source_name: str = None    # For income
    transaction_date: date = None
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