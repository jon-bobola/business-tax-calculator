
from app.model.filing_status.filing_status import FilingStatus
from app.model.liabilities.tax_liability import TaxLiability
from app.model.deduction.deduction_registry import DeductionRegistry

class TaxReturn:
    def __init__(self):
        
        self.filing_status = FilingStatus()
        self.tax_liability = TaxLiability()
        self.deduction_registry = DeductionRegistry()