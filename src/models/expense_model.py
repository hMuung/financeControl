# src/models/expense_model.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Expense:
    category: str
    amount: float
    origin: str
    description: str = "Sin descripcion"
    date: Optional[str] = None
    id: Optional[int] = None