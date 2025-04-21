from app.model.liabilities.federal_income_tax_liability import FederalIncomeTaxLiability
from app.model.liabilities.state_income_tax_liability import StateIncomeTaxLiability
from app.model.liabilities.local_income_tax_liability import LocalIncomeTaxLiability
from app.model.liabilities.medicare_tax_liability import MedicareIncomeTaxLiability
from app.model.liabilities.social_security_tax_liability import SocialSecurityIncomeTaxLiability
from app.model.liabilities.liability import Liability
from app.model.filing_status.filing_status import FilingStatus

class TaxLiability(Liability):
    
    def __init__(self):
        
        self.federal_income_tax_liability = FederalIncomeTaxLiability()
        self.state_income_tax_liability = StateIncomeTaxLiability()
        self.local_income_tax_liability = LocalIncomeTaxLiability()
        self.medicare_tax_liability = MedicareIncomeTaxLiability()
        self.social_security_tax_liability = SocialSecurityIncomeTaxLiability()
        
    def calculate(self, filing_status: FilingStatus, taxable_income: float) -> float:
        
        federal_tax = self.federal_income_tax_liability.calculate(filing_status, taxable_income)
        state_tax = self.state_income_tax_liability.calculate(filing_status, taxable_income)
        local_tax = self.local_income_tax_liability.calculate(filing_status, taxable_income)
        medicare_tax = self.medicare_tax_liability.calculate(filing_status, taxable_income)
        ss_tax = self.social_security_tax_liability.calculate(filing_status, taxable_income)

        tax = federal_tax + state_tax + local_tax + medicare_tax + ss_tax
        self.value = tax
        
        return self.value
    
    @property
    def income_tax(self) -> float:
        self.income_tax = self.federal_income_tax_liability.value + self.state_income_tax_liability.value + self.local_income_tax_liability.value
        return self.income_tax
    
    @property
    def self_employment_tax(self) -> float:
        self.self_employment_tax = self.medicare_tax_liability.value + self.social_security_tax_liability.value
        return self.self_employment_tax