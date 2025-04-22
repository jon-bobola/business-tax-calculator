from business_tax_calculator.model.tax_rate.tax_rate import TaxRate

TAX_RATE_NAME = "State Tax Rate"
STATE_TAX_VALUE = 0.00  # Example state tax rate (0%)

class StateTaxRate(TaxRate):
    # This class represents the State tax rate.
   def __init__(self):
        super().__init__(TAX_RATE_NAME, STATE_TAX_VALUE) 