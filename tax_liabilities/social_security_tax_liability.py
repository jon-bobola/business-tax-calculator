from dataclasses import dataclass

@dataclass
class SocialSecurityTaxLiability:
    rate: float = 0.124  # Social Security tax rate (12.4%)

    def calculate(self, income: float) -> float:
        """
        Calculate Social Security tax based on income.
        :param income: The income subject to Social Security tax
        :return: The Social Security tax
        """
        taxable_income = min(income, 168600)  # 2024 cap for Social Security tax
        return taxable_income * self.rate
