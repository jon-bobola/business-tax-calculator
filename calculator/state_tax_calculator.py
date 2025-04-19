# calculator/state_tax_calculator.py
"""
State income tax calculator integrated with StateIncomeTaxLiability.
"""

from tax_liabilities.state_income_tax_liability import StateIncomeTaxLiability
from constants import MarginalTaxBrackets

def calculate_state_income_tax(business, taxable_income):
    """
    Use custom brackets if provided, else default STATE.
    """
    if hasattr(business, "state_brackets") and business.state_brackets:
        liab = StateIncomeTaxLiability(bracket_calculator=business.state_brackets)
    else:
        liab = StateIncomeTaxLiability(bracket_calculator=MarginalTaxBrackets.STATE.value)
    return liab.calculate(taxable_income)