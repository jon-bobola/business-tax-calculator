# calculator/local_tax_calculator.py
"""
Local income tax calculator integrated with LocalTaxLiability.
"""

from business_tax_calculator.model.liabilities.local_income_tax_liability import LocalIncomeTaxLiability

def calculate_local_income_tax(business, taxable_income):
    """
    Instantiate LocalTaxLiability with override or default rate.
    """
    rate = getattr(business, "local_tax_rate", None)
    if rate is not None:
        liab = LocalIncomeTaxLiability(rate=rate)
    else:
        liab = LocalIncomeTaxLiability()
    return liab.calculate(taxable_income)
