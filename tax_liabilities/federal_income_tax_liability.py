from dataclasses import dataclass
from constants import MarginalTaxBrackets

@dataclass
class FederalIncomeTaxLiability:
    """
    Calculate federal income tax based on income using marginal tax brackets.
    """
    def calculate(self, income: float) -> float:
        """
        Calculate federal income tax based on taxable income.
        :param income: The taxable income
        :return: The federal income tax
        """
        tax = 0.0
        brackets = MarginalTaxBrackets.FEDERAL.value

        for lower, upper, rate in brackets:
            if income > upper:
                tax += (upper - lower + 1) * rate
            else:
                tax += max(0, income - lower) * rate
                break

        return tax
