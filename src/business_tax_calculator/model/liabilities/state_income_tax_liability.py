from dataclasses import dataclass
from business_tax_calculator.utils.constants import MarginalTaxBrackets
from business_tax_calculator.model.liabilities.liability import Liability

@dataclass
class StateIncomeTaxLiability(Liability):

    def calculate(self, taxable_income: float) -> float:
        tax = 0.0
        brackets = MarginalTaxBrackets.STATE.value

        for lower, upper, rate in brackets:
            if taxable_income > upper:
                tax += (upper - lower + 1) * rate
            else:
                tax += max(0, taxable_income - lower) * rate
                break

        self.value = tax
        return self.value
