from dataclasses import dataclass
from app.model.liabilities.liability import Liability

@dataclass
class MedicareIncomeTaxLiability(Liability):
    rate: float = 0.029  # Medicare tax rate (2.9%)
    additional_rate: float = 0.009  # Additional Medicare tax rate (0.9%) for income over $200,000
    threshold: float = 200000  # Threshold for additional Medicare tax

    def calculate(self, taxable_income: float) -> float:
        """
        Calculate Medicare tax based on income.
        :param income: The income subject to Medicare tax
        :return: The Medicare tax
        """
        if taxable_income <= self.threshold:
            tax = taxable_income * self.rate
        else:
            base_tax = self.threshold * self.rate
            additional_tax = (taxable_income - self.threshold) * (self.rate + self.additional_rate)
            tax = base_tax + additional_tax

        self.value = tax
        return self.value