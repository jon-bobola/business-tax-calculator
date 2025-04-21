from app.model.deduction import Deduction


from typing import Any


class SelfEmploymentTaxDeduction(Deduction):
    """Self-employment tax deduction (50% of SE tax)."""

    def get_name(self) -> str:
        return "se_tax_deduction"

    def is_applicable(self, business: Any, filing_status: str) -> bool:
        # Applies to pass-through entities (not C-Corps)
        return business.entity_type in ["Sole Proprietorship", "LLC", "S-Corp"]

    def calculate(self, business: Any, filing_status: str, **kwargs) -> float:
        se_tax = kwargs.get('se_tax', 0)
        return round(se_tax * 0.50, 2)