from pydantic import BaseModel
from typing import List

class Expense(BaseModel):
    category: str
    subcategory: str
    amount: float
    frequency: str
    essential: bool

class FinanceData(BaseModel):
    income: float
    expenses: List[Expense]
