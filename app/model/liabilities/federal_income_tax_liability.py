from dataclasses import dataclass
from app.utils.constants import MarginalTaxBrackets
from app.model.liabilities.liability import Liability

@dataclass
class FederalIncomeTaxLiability(Liability):
    """
    Calculate federal income tax based on income using marginal tax brackets.
    """
    def calculate(self, taxable_income: float) -> float:
        """
        Calculate federal income tax based on taxable income.
        :param income: The taxable income
        :return: The federal income tax
        """
        tax = 0.0
        brackets = MarginalTaxBrackets.FEDERAL.value

        for lower, upper, rate in brackets:
            if taxable_income > upper:
                tax += (upper - lower + 1) * rate
            else:
                tax += max(0, taxable_income - lower) * rate
                break

        self.value = tax
        return self.value
