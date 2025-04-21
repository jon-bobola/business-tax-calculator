from dataclasses import dataclass
from app.model.liabilities.liability import Liability
from app.model.filing_status.filing_status import FilingStatus

@dataclass
class SocialSecurityIncomeTaxLiability(Liability):
    rate: float = 0.124  # Social Security tax rate (12.4%)

    def calculate(self, filing_status: FilingStatus, taxable_income: float) -> float:
        """
        Calculate Social Security tax based on income.
        :param income: The income subject to Social Security tax
        :return: The Social Security tax
        """
        taxable_income = min(taxable_income, 168600)  # 2024 cap for Social Security tax
        tax = taxable_income * self.rate
        
        self.value = tax
        return self.value
