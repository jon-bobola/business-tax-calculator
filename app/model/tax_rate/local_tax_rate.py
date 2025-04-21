from app.model.tax_rate.tax_rate import TaxRate

TAX_RATE_NAME = "Local Tax Rate"
LOCAL_TAX_VALUE = 0.032  # Howard County, MD local tax rate (3%)

class LocalTaxRate(TaxRate):
    # This class represents the Local tax rate.
    def __init__(self):
        super().__init__(TAX_RATE_NAME, LOCAL_TAX_VALUE)