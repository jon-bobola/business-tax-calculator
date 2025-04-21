from dataclasses import dataclass
from app.model.liabilities.liability import Liability
from app.model.filing_status.filing_status import FilingStatus

@dataclass
class LocalIncomeTaxLiability(Liability):
    """
    Calculator for local income tax (flat rate).
    """
    rate: float = 0.032  # Default local tax rate, can be parameterized

    def calculate(self, filing_status: FilingStatus, taxable_income: float) -> float:
        tax = taxable_income * self.rate
        self.value = tax
        return self.value