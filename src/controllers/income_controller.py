# src/controllers/income_controller.py
from models.models import Income
from services.income_service import IncomeService


class IncomeController:

    # Atributo de clase compartido para detectar cambios en UI
    _is_dirty: bool = True

    def __init__(self):
        self.service = IncomeService()

    def get_totals(self) -> dict:
            return self.service.get_totals()

    def create_income(
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

        new_income = Income(
            category_id=category_id,
            origin_id=origin_id,
            amount=amount,
            description=desc_clean,
        )
        self.service.save(new_income)
        IncomeController._is_dirty = True
        return True, "Registro correcto."

    def fetch_history(self) -> list[Income]:
        return self.service.get_all()

    def delete_income(self, income_id: int) -> tuple[bool, str]:
        IncomeController._is_dirty = True
        if not income_id:
            return False, "ID de registro no válido."

        success = self.service.delete(income_id)
        if success:
            return True, "Registro eliminado correctamente."
        return False, "No se pudo eliminar el registro."

    def update_income(
        self,
        income_id: int,
        category_id: int,
        amount_str: str,
        origin_id: int,
        description: str = "",
    ) -> tuple[bool, str]:
        if not income_id:
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

        income = Income(
            id=income_id,
            category_id=category_id,
            origin_id=origin_id,
            amount=amount,
            description=desc_clean,
        )

        if self.service.update(income):
            IncomeController._is_dirty = True
            return True, "Ingreso actualizado correctamente."
        return False, "No se pudo actualizar el registro."

    @classmethod
    def mark_clean(cls):
        cls._is_dirty = False

    @classmethod
    def is_dirty(cls) -> bool:
        return cls._is_dirty