from app.model.deduction import Deduction


from typing import Any


class OtherDeduction(Deduction):
    """Other miscellaneous deductions."""

    def get_name(self) -> str:
        return "other_deductions"

    def is_applicable(self, business: Any, filing_status: str) -> bool:
        return hasattr(business, 'other_deductions') and business.other_deductions > 0

    def calculate(self, business: Any, filing_status: str, **kwargs) -> float:
        return business.other_deductions if hasattr(business, 'other_deductions') else 0