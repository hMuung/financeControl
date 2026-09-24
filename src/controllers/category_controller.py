# src/controllers/category_controller.py
from services.category_service import CategoryService
from models.models import Category

class CategoryController:
    def __init__(self):
        self.service = CategoryService()

    def get_all_categories(self) -> list[Category]:
        return self.service.get_all()