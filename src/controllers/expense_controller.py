# src/controllers/expense_controller.py
from models.expense_model import Expense
from services.expense_service import ExpenseService

class ExpenseController:
    def __init__(self):
        self.service = ExpenseService()

    def create_expense(self, category: str, amount_str: str, origin: str, description: str = ""):
        if not category or not amount_str or not origin:
            return False, "Faltan campos obligatorios."

        try:
            amount = float(amount_str)
            if amount <= 0:
                return False, "El monto debe ser mayor a 0."
        except ValueError:
            return False, "El monto debe ser un numero valido."

        desc_clean = description.strip() if description and description.strip() else "Sin descripción"

        new_expense = Expense(
            category=category,
            amount=amount,
            origin=origin,
            description=desc_clean
        )
        self.service.save(new_expense)
        return True, "Registro correcto."

    def fetch_history(self) -> list[Expense]:
        return self.service.get_all()

    def delete_expense(self, expense_id: int) -> tuple[bool, str]:
        if not expense_id:
            return False, "ID de registro no valido."

        success = self.service.delete(expense_id)
        if success:
            return True, "Registro eliminado correctamente."
        return False, "No se pudo eliminar el registro."