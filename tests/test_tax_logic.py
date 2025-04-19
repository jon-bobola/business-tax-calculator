import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from BusinessTaxLiabilityCalculator import SocialSecurityTaxLiability, TaxBracket, MarginalTaxBrackets

def test_social_security_tax_under_threshold():
    ss_tax = SocialSecurityTaxLiability()
    result = ss_tax.calculate(50000)
    expected = 50000 * 0.124
    assert abs(result - expected) < 0.01

def test_social_security_tax_above_threshold():
    ss_tax = SocialSecurityTaxLiability()
    result = ss_tax.calculate(200000)
    expected = 168600 * 0.124  # Max taxable income for SS
    assert abs(result - expected) < 0.01

def test_tax_bracket_simple_case():
    brackets = [(10000, 0.1), (20000, 0.2), (float('inf'), 0.3)]
    tax_calc = TaxBracket(brackets)
    result = tax_calc.calculate_tax(15000)
    expected = (10000 * 0.1) + (5000 * 0.2)
    assert abs(result - expected) < 0.01

def test_federal_tax_bracket_from_enum():
    tax_calc = TaxBracket(MarginalTaxBrackets.FEDERAL.value)
    result = tax_calc.calculate_tax(50000)
    # Should be: 23,200 * 10% + (50,000 - 23,200) * 12%
    expected = (23200 * 0.10) + ((50000 - 23200) * 0.12)
    assert abs(result - expected) < 0.01