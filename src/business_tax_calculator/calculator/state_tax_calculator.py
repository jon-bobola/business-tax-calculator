# calculator/state_tax_calculator.py
"""
State income tax calculator integrated with StateIncomeTaxLiability.
"""

from business_tax_calculator.model.liabilities.state_income_tax_liability import StateIncomeTaxLiability
from utils.constants import MarginalTaxBrackets

class StateIncomeTaxCalculator:

    def calculate_state_income_tax(business, taxable_income):
        """
        Use custom brackets if provided, else default STATE.
        """
        if hasattr(business, "state_brackets") and business.state_brackets:
            # liab = StateIncomeTaxLiability(bracket_calculator=business.state_brackets)
            liab = StateIncomeTaxLiability()
        else:
            liab = StateIncomeTaxLiability()
        return liab.calculate(taxable_income)