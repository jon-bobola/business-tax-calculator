from business_tax_calculator.model.liabilities.federal_income_tax_liability import FederalIncomeTaxLiability
from business_tax_calculator.model.liabilities.state_income_tax_liability import StateIncomeTaxLiability
from business_tax_calculator.model.liabilities.local_income_tax_liability import LocalIncomeTaxLiability
from business_tax_calculator.model.liabilities.medicare_income_tax_liability import MedicareIncomeTaxLiability
from business_tax_calculator.model.liabilities.social_security_income_tax_liability import SocialSecurityIncomeTaxLiability
from business_tax_calculator.model.liabilities.liability import Liability

class TaxLiability(Liability):
    
    def __init__(self):
        
        self.federal_income_tax_liability = FederalIncomeTaxLiability()
        self.state_income_tax_liability = StateIncomeTaxLiability()
        self.local_income_tax_liability = LocalIncomeTaxLiability()
        self.medicare_income_tax_liability = MedicareIncomeTaxLiability()
        self.social_security_income_tax_liability = SocialSecurityIncomeTaxLiability()
        
    def calculate(self, taxable_income: float) -> float:
        
        federal_tax = self.federal_income_tax_liability.calculate(taxable_income)
        state_tax = self.state_income_tax_liability.calculate(taxable_income)
        local_tax = self.local_income_tax_liability.calculate(taxable_income)
        medicare_tax = self.medicare_income_tax_liability.calculate(taxable_income)
        ss_tax = self.social_security_income_tax_liability.calculate(taxable_income)

        tax = federal_tax + state_tax + local_tax + medicare_tax + ss_tax
        self.value = tax
        
        return self.value
    
    def income_tax(self) -> float:
        return (
            self.federal_income_tax_liability.value +
            self.state_income_tax_liability.value +
            self.local_income_tax_liability.value
        )

    def self_employment_tax(self) -> float:
        return (
            self.medicare_income_tax_liability.value +
            self.social_security_income_tax_liability.value
        )
