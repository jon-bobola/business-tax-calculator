from app.model.deduction import Deduction


from typing import Any


class HomeOfficeDeduction(Deduction):
    """Home office expense deduction."""

    def get_name(self) -> str:
        return "home_office"

    def is_applicable(self, business: Any, filing_status: str) -> bool:
        return hasattr(business, 'home_office_expenses') and business.home_office_expenses > 0

    def calculate(self, business: Any, filing_status: str, **kwargs) -> float:
        return business.home_office_expenses if hasattr(business, 'home_office_expenses') else 0