from dataclasses import dataclass
from typing import Optional, List
from datetime import date


# Request DTOs
@dataclass
class CreateIncomeRequest:
    source_name: str
    expected_amount: float
    month: int
    year: int
    due_date: Optional[date] = None
    description: Optional[str] = None


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


@dataclass
class ReceiveIncomeRequest:
    actual_amount: float
    receive_date: Optional[date] = None


# Response DTOs
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


@dataclass
class IncomeSingleResponse:
    status: str
    income: IncomeResponse