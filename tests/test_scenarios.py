import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from BusinessTaxLiabilityCalculator import (
    SoleProprietorTaxScenario,
    SCorpTaxScenario,
    TaxCalculatorFactory,
    EntityType,
    ResultKeys
)

def test_sole_proprietor_scenario():
    scenario = SoleProprietorTaxScenario(
        gross_revenue=100000,
        expenses=50000,
        salary=0,
        tax_deduction=TaxCalculatorFactory.create_tax_deduction(),
        liabilities=TaxCalculatorFactory.create_liabilities()
    )
    result = scenario.calculate()
    assert result[ResultKeys.ENTITY_TYPE.value] == EntityType.SOLE_PROPRIETOR.value
    assert result[ResultKeys.GROSS_REVENUE.value] == 100000
    assert result[ResultKeys.EXPENSES.value] == 50000
    assert result[ResultKeys.TOTAL_TAX.value] > 0

def test_scorp_scenario():
    scenario = SCorpTaxScenario(
        gross_revenue=200000,
        expenses=100000,
        salary=80000,
        tax_deduction=TaxCalculatorFactory.create_tax_deduction(),
        liabilities=TaxCalculatorFactory.create_liabilities()
    )
    result = scenario.calculate()
    assert result[ResultKeys.ENTITY_TYPE.value] == EntityType.S_CORP.value
    assert result[ResultKeys.GROSS_SALARY.value] == 80000
    assert result[ResultKeys.GROSS_DISTRIBUTIONS.value] == 20000
    assert result[ResultKeys.TOTAL_TAX.value] > 0