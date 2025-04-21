from app.model.tax_rate.tax_rate import TaxRate

TAX_RATE_NAME = "Medicare Tax Rate"
MEDICARE_TAX_VALUE = 0.029  # 2.9% Medicare tax rate

class MedicareTaxRate(TaxRate):
    # This class represents the Medicare tax rate.
    def __init__(self):
        super().__init__(TAX_RATE_NAME, MEDICARE_TAX_VALUE)