from app.model.tax_rate.tax_rate import TaxRate

TAX_RATE_NAME = "Federal Tax Rate"
FEDERAL_TAX_VALUE = 0.0  # 0% Federal tax rate placeholder

class FederalTaxRate(TaxRate):
    # This class represents the Federal tax rate.
    def __init__(self):
        super().__init__(TAX_RATE_NAME, FEDERAL_TAX_VALUE)