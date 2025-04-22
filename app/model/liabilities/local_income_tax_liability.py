from dataclasses import dataclass
from app.model.liabilities.liability import Liability

@dataclass
class LocalIncomeTaxLiability(Liability):
    """
    Calculator for local income tax (flat rate).
    """
    rate: float = 0.032  # Default local tax rate, can be parameterized

    def calculate(self, taxable_income: float) -> float:
        tax = taxable_income * self.rate
        self.value = tax
        return self.value