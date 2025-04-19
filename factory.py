# business_tax_calculator/factory.py
from scenario import SoleProprietorTaxScenario, SCorpTaxScenario
from deductions import TaxDeduction, TaxDeductionDependencies
from liabilities import TaxLiability, TaxLiabilityDependencies
from constants import EntityType


class TaxCalculatorFactory:
    @staticmethod
    def create_tax_deduction() -> TaxDeduction:
        return TaxDeduction(TaxDeductionDependencies())

    @staticmethod
    def create_tax_liability() -> TaxLiability:
        return TaxLiability(TaxLiabilityDependencies())

    @staticmethod
    def create_scenario(**kwargs):
        deduction = TaxCalculatorFactory.create_tax_deduction()
        liability = TaxCalculatorFactory.create_tax_liability()
        et = kwargs.pop("entity_type")
        if et == EntityType.SOLE_PROPRIETOR.value:
            return SoleProprietorTaxScenario(**kwargs, entity_type=et, tax_deduction=deduction, tax_liability=liability)
        elif et == EntityType.S_CORP.value:
            return SCorpTaxScenario(**kwargs, entity_type=et, tax_deduction=deduction, tax_liability=liability)
        else:
            raise ValueError(f"Unknown entity type: {et}")
