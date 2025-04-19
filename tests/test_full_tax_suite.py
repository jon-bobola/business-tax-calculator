import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from BusinessTaxLiabilityCalculator import (
    TaxBracket,
    SocialSecurityTaxLiability,
    MedicareTaxLiability,
    FederalIncomeTaxLiability,
    StateIncomeTaxLiability,
    LocalTaxLiability,
    StandardDeduction,
    SocialSecurityDeduction,
    MedicareDeduction,
    QualifiedBusinessIncomeDeduction,
    MarginalTaxBrackets,
    DeductionRates,
    TaxRates,
    Threshold
)

def test_social_security_tax_basic():
    ss = SocialSecurityTaxLiability()
    income = 50000
    expected = income * TaxRates.SOCIAL_SECURITY_TAX_RATE.value
    result = ss.calculate(income)
    assert abs(result - expected) < 0.01

def test_social_security_tax_cap():
    ss = SocialSecurityTaxLiability()
    income = 200000
    expected = Threshold.SOCIAL_SECURITY_INCOME_THRESHOLD.value * TaxRates.SOCIAL_SECURITY_TAX_RATE.value
    result = ss.calculate(income)
    assert abs(result - expected) < 0.01

def test_medicare_tax_under_threshold():
    medicare = MedicareTaxLiability()
    income = 100000
    expected = income * TaxRates.MEDICARE_TAX_RATE.value
    result = medicare.calculate(income)
    assert abs(result - expected) < 0.01

def test_medicare_tax_above_threshold():
    medicare = MedicareTaxLiability()
    income = 300000
    base = income * TaxRates.MEDICARE_TAX_RATE.value
    additional = (income - Threshold.ADDITIONAL_MEDICARE_INCOME_THRESHOLD.value) * TaxRates.ADDITIONAL_MEDICARE_TAX_RATE.value
    expected = base + additional
    result = medicare.calculate(income)
    assert abs(result - expected) < 0.01

def test_tax_bracket_multilevel():
    brackets = [(10000, 0.1), (20000, 0.2), (float('inf'), 0.3)]
    calc = TaxBracket(brackets)
    income = 25000
    expected = 10000*0.1 + 10000*0.2 + 5000*0.3
    result = calc.calculate_tax(income)
    assert abs(result - expected) < 0.01

def test_federal_tax():
    calc = TaxBracket(MarginalTaxBrackets.FEDERAL.value)
    federal = FederalIncomeTaxLiability(calc)
    income = 50000
    result = federal.calculate(income)
    assert result > 0

def test_state_tax():
    calc = TaxBracket(MarginalTaxBrackets.STATE.value)
    state = StateIncomeTaxLiability(calc)
    income = 60000
    result = state.calculate(income)
    assert result > 0

def test_local_tax():
    local = LocalTaxLiability()
    income = 100000
    expected = income * TaxRates.LOCAL_TAX_RATE.value
    result = local.calculate(income)
    assert abs(result - expected) < 0.01

def test_standard_deduction():
    sd = StandardDeduction()
    result = sd.calculate()
    assert result == 29200

def test_social_security_deduction():
    ss_ded = SocialSecurityDeduction()
    result = ss_ded.calculate(10000)
    expected = 10000 * DeductionRates.SELF_EMPLOYMENT_DEDUCTION_RATE.value
    assert abs(result - expected) < 0.01

def test_medicare_deduction():
    med_ded = MedicareDeduction()
    result = med_ded.calculate(10000)
    expected = 10000 * DeductionRates.SELF_EMPLOYMENT_DEDUCTION_RATE.value
    assert abs(result - expected) < 0.01

def test_qbi_deduction():
    qbi = QualifiedBusinessIncomeDeduction()
    result = qbi.calculate(80000)
    expected = 80000 * DeductionRates.QUALIFIED_BUSINESS_INCOME_DEDUCTION_RATE.value
    assert abs(result - expected) < 0.01