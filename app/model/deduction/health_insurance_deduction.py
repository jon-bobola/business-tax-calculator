from app.model.deduction import Deduction


from typing import Any


class HealthInsuranceDeduction(Deduction):
    """Health insurance premium deduction."""

    def get_name(self) -> str:
        return "health_insurance"

    def is_applicable(self, business: Any, filing_status: str) -> bool:
        return hasattr(business, 'health_premiums') and business.health_premiums > 0

    def calculate(self, business: Any, filing_status: str, **kwargs) -> float:
        return business.health_premiums if hasattr(business, 'health_premiums') else 0