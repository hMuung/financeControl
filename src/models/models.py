# src/models/models.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class Expense:
    category_id: int
    origin_id: int
    amount: float
    id: Optional[int] = None
    description: Optional[str] = "Sin descripcion"
    date: Optional[str] = None
    category_name: Optional[str] = None
    origin_name: Optional[str] = None
    

@dataclass
class Income:
    category_id: int
    origin_id: int
    amount: float
    id: Optional[int] = None
    description: Optional[str] = "Sin descripcion"
    date: Optional[str] = None
    category_name: Optional[str] = None
    origin_name: Optional[str] = None


@dataclass
class Category:
    name: str
    id: Optional[int] = None
    color: Optional[str] = None
    bg_color: Optional[str] = None
    icon: Optional[str] = None
    type: str = "EXPENSE"  # "EXPENSE" o "INCOME"


@dataclass
class Origin:
    name: str
    id: Optional[int] = None
    color: Optional[str] = None
    bg_color: Optional[str] = None
    icon: Optional[str] = None
    type: str = "EXPENSE"  #"EXPENSE" o "INCOME"