from dataclasses import dataclass
from constants import MarginalTaxBrackets

@dataclass
class StateIncomeTaxLiability:
    bracket_calculator: TaxBracket

    def calculate(self, income: float) -> float:
        return self.bracket_calculator.calculate(income)