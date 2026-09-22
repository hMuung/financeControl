# src/models/expense.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Expense:
    category: str
    amount: float
    origin: str
    date: Optional[str] = None
    id: Optional[int] = None