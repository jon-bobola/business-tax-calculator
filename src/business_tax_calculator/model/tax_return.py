
from business_tax_calculator.model.filing_status.filing_status import FilingStatus
from business_tax_calculator.model.liabilities.tax_liability import TaxLiability
from business_tax_calculator.model.deduction.deduction_registry import DeductionRegistry

class TaxReturn:
    def __init__(self):
        
        self.filing_status = FilingStatus()
        self.tax_liability = TaxLiability()
        self.deduction_registry = DeductionRegistry()