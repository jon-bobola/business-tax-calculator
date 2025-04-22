from business_tax_calculator.model.tax_rate.tax_rate import TaxRate

TAX_RATE_NAME = "Medicare High Earner Tax Rate"
MEDICARE_HIGH_EARNER_TAX_VALUE = 0.009  # 0.9% Medicare tax rate for high earners

class MedicareHighEarnerTaxRate(TaxRate):
    # This class represents the Medicare high earner tax rate.
    def __init__(self):
        super().__init__(TAX_RATE_NAME, MEDICARE_HIGH_EARNER_TAX_VALUE)