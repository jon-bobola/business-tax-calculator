from social_security_tax_liability import SocialSecurityTaxLiability
from medicare_tax_liability import MedicareTaxLiability
from federal_income_tax_liability import FederalIncomeTaxLiability

class TaxLiability:
    def __init__(self):
        self.social_security_tax = SocialSecurityTaxLiability()
        self.medicare_tax = MedicareTaxLiability()
        self.federal_income_tax = FederalIncomeTaxLiability()

    def calculate_total_tax(self, se_income: float, taxable_income: float) -> float:
        """
        Calculate total tax by adding Social Security, Medicare, and Federal Income tax.
        :param se_income: Self-employment income
        :param taxable_income: Taxable income for federal tax
        :return: The total tax
        """
        ss_tax = self.social_security_tax.calculate(se_income)
        medicare_tax = self.medicare_tax.calculate(se_income)
        federal_tax = self.federal_income_tax.calculate(taxable_income)

        return ss_tax + medicare_tax + federal_tax
