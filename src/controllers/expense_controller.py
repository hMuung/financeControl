# src/controllers/expense_controller.py
from models.models import Expense
from services.expense_service import ExpenseService


class ExpenseController:

    # Atributo de clase compartido
    _is_dirty: bool = True

    def __init__(self):
        self.service = ExpenseService()

    def get_totals(self) -> dict:
        return self.service.get_totals()

    def create_expense(
        self,
        category_id: int,
        amount_str: str,
        origin_id: int,
        description: str = "",
    ) -> tuple[bool, str]:
        if not category_id or not amount_str or not origin_id:
            return False, "Faltan campos obligatorios."

        try:
            clean_amount = str(amount_str).replace(",", "").strip()
            amount = float(clean_amount)
            if amount <= 0:
                return False, "El monto debe ser mayor a 0."
        except ValueError:
            return False, "El monto debe ser un número válido."

        desc_clean = (
            description.strip()
            if description and description.strip()
            else "Sin descripción"
        )

        new_expense = Expense(
            
            category_id=category_id,
            origin_id=origin_id,
            amount=amount,
            description=desc_clean,
        )
        self.service.save(new_expense)
        ExpenseController._is_dirty = True
        return True, "Registro correcto."

    def fetch_history(self) -> list[Expense]:
        return self.service.get_all()

    def delete_expense(self, expense_id: int) -> tuple[bool, str]:
        ExpenseController._is_dirty = True
        if not expense_id:
            return False, "ID de registro no válido."

        success = self.service.delete(expense_id)
        if success:
            return True, "Registro eliminado correctamente."
        return False, "No se pudo eliminar el registro."

    def update_expense(
        self,
        expense_id: int,
        category_id: int,
        amount_str: str,
        origin_id: int,
        description: str = "",
    ) -> tuple[bool, str]:
        
        if not expense_id:
            return False, "ID de registro no válido."

        if not category_id or not amount_str or not origin_id:
            return False, "Faltan campos obligatorios."

        try:
            clean_amount = str(amount_str).replace(",", "").strip()
            amount = float(clean_amount)
            if amount <= 0:
                return False, "El monto debe ser mayor a 0."
        except ValueError:
            return False, "El monto debe ser un número válido."

        desc_clean = (
            description.strip()
            if description and description.strip()
            else "Sin descripción"
        )

        expense = Expense(
            id=expense_id,
            category_id=category_id,
            origin_id=origin_id,
            amount=amount,
            description=desc_clean,
        )

        if self.service.update(expense):
            ExpenseController._is_dirty = True
            return True, "Gasto actualizado correctamente."
        return False, "No se pudo actualizar el registro."

    @classmethod
    def mark_clean(cls):
        cls._is_dirty = False

    @classmethod
    def is_dirty(cls) -> bool:
        return cls._is_dirty
