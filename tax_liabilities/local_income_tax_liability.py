from dataclasses import dataclass

@dataclass
class LocalTaxLiability:
    """
    Calculator for local income tax (flat rate).
    """
    rate: float = 0.032  # Default local tax rate, can be parameterized

    def calculate(self, income: float) -> float:
        return income * self.rate