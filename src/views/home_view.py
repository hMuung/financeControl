import flet as ft

from controllers.income_controller import IncomeController
from controllers.expense_controller import ExpenseController

from views.components.common.header import Header
from views.components.quick_expense import QuickExpenseCard
from views.components.quick_income import QuickIncomeCard
from views.components.financial_sumary_card import FinancialSummaryCard


class HomeView(ft.Column):
    def __init__(self):
        super().__init__(
            spacing=10,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        self.income_ctrl = IncomeController()
        self.expense_ctrl = ExpenseController()

        self.summary_card = FinancialSummaryCard(
            setpoint_low=500.0,
            setpoint_high=2000.0,
        )

        self.controls = [
            Header(),
            self.summary_card,
            QuickExpenseCard(on_summit=self.refresh_summary, initially_collapsed=False),
            QuickIncomeCard(on_summit=self.refresh_summary, initially_collapsed=True),
        ]

        self.summary_card.refresh()

    def refresh_summary(self):
        self.summary_card.refresh()
        self.summary_card.update()