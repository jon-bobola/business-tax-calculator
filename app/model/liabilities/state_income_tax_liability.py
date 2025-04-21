from dataclasses import dataclass
from app.utils.constants import MarginalTaxBrackets
from app.model.liabilities.liability import Liability
from app.model.filing_status.filing_status import FilingStatus

@dataclass
class StateIncomeTaxLiability(Liability):

    def calculate(self, filing_status: FilingStatus, taxable_income: float) -> float:
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
