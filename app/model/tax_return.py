
from app.model.filing_status.filing_status import FilingStatus
from app.model.liabilities.tax_liability import TaxLiability
from app.model.deduction.deduction import Deduction

class TaxReturn:
    def __init__(self):
        
        self.filing_status = FilingStatus()
        self.tax_liability = TaxLiability()
        self.tax_deduction = Deduction()
        
        self.tax_deductions = []