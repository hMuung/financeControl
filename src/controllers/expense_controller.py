# src/controllers/expense_controller.py
from models.expense import Expense
from services.expense_service import ExpenseService

class ExpenseController:
    def __init__(self):
        self.service = ExpenseService()

    def create_expense(self, category: str, amount_str: str, origin: str):
        if not category or not amount_str or not origin:
            return False, "Todos los campos son obligatorios."

        try:
            amount = float(amount_str)
            if amount <= 0:
                return False, "El monto debe ser mayor a 0."
        except ValueError:
            return False, "El monto debe ser un numero valido."

        new_expense = Expense(category=category, amount=amount, origin=origin)
        self.service.save(new_expense)
        return True, "Registro correcto."

    def fetch_history(self) -> list[Expense]:
        return self.service.get_all()