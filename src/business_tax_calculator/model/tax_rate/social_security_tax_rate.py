from business_tax_calculator.model.tax_rate.tax_rate import TaxRate

TAX_RATE_NAME = "Social Security Tax Rate"
SOCIAL_SECURITY_TAX_VALUE = 0.124  # 12.4% Social Security tax rate

class SocialSecurityTaxRate(TaxRate):
    # This class represents the Social Security tax rate.
    def __init__(self):
        super().__init__(TAX_RATE_NAME, SOCIAL_SECURITY_TAX_VALUE)