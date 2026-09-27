# src/controllers/origin_controller.py
from services.origin_service import OriginService
from models.models import Origin

class OriginController:
    def __init__(self):
        self.service = OriginService()

    def get_all_origins(self) -> list[Origin]:
        return self.service.get_all()

    def get_expense_origins(self) -> list[Origin]:
        return self.service.get_all(origin_type="EXPENSE")

    def get_income_origins(self) -> list[Origin]:
        return self.service.get_all(origin_type="INCOME")