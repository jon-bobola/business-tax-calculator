from app.model.deduction import Deduction


from typing import Any


class RetirementContributionDeduction(Deduction):
    """Retirement contribution deduction."""

    def get_name(self) -> str:
        return "retirement"

    def is_applicable(self, business: Any, filing_status: str) -> bool:
        return hasattr(business, 'retirement_contributions') and business.retirement_contributions > 0

    def calculate(self, business: Any, filing_status: str, **kwargs) -> float:
        return business.retirement_contributions if hasattr(business, 'retirement_contributions') else 0