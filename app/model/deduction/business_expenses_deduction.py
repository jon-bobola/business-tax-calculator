from app.model.deduction.deduction import Deduction


from typing import Any


class BusinessExpensesDeduction(Deduction):
    """Standard business expenses deduction."""

    def get_name(self) -> str:
        return "expenses"

    def is_applicable(self, business: Any, filing_status: str) -> bool:
        # Business expenses are always applicable
        return True

    def calculate(self, business: Any, filing_status: str, **kwargs) -> float:
        return business.expenses