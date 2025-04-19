from dataclasses import dataclass

@dataclass
class MedicareTaxLiability:
    rate: float = 0.029  # Medicare tax rate (2.9%)
    additional_rate: float = 0.009  # Additional Medicare tax rate (0.9%) for income over $200,000
    threshold: float = 200000  # Threshold for additional Medicare tax

    def calculate(self, income: float) -> float:
        """
        Calculate Medicare tax based on income.
        :param income: The income subject to Medicare tax
        :return: The Medicare tax
        """
        if income <= self.threshold:
            return income * self.rate
        else:
            base_tax = self.threshold * self.rate
            additional_tax = (income - self.threshold) * (self.rate + self.additional_rate)
            return base_tax + additional_tax
