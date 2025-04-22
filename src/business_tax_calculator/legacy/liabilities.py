# business_tax_calculator/liabilities.py
from dataclasses import dataclass
from typing import Dict

from business_tax_calculator.utils.constants import MarginalTaxBrackets


@dataclass
class SocialSecurityTaxLiability:
    rate: float = 0.124  # or from constants

    def calculate(self, base: float) -> float:
        return base * self.rate


@dataclass
class MedicareTaxLiability:
    rate: float = 0.029

    def calculate(self, base: float) -> float:
        return base * self.rate


class TaxBracket:
    def __init__(self, brackets):
        self.brackets = brackets

    def calculate(self, income: float) -> float:
        # implement marginal bracket logic
        ...


@dataclass
class FederalIncomeTaxLiability:
    bracket_calculator: TaxBracket

    def calculate(self, income: float) -> float:
        return self.bracket_calculator.calculate(income)


@dataclass
class StateIncomeTaxLiability:
    bracket_calculator: TaxBracket

    def calculate(self, income: float) -> float:
        return self.bracket_calculator.calculate(income)


@dataclass
class LocalTaxLiability:
    flat_rate: float = 0.03

    def calculate(self, income: float) -> float:
        return income * self.flat_rate


class TaxLiabilityDependencies:
    def __init__(self):
        self.social_security_tax = SocialSecurityTaxLiability()
        self.medicare_tax = MedicareTaxLiability()
        self.federal_income_tax = FederalIncomeTaxLiability(TaxBracket(MarginalTaxBrackets.FEDERAL.value))
        self.state_income_tax = StateIncomeTaxLiability(TaxBracket(MarginalTaxBrackets.STATE.value))
        self.local_tax = LocalTaxLiability()


class TaxLiability:
    def __init__(self, deps: TaxLiabilityDependencies):
        self.social_security_tax = deps.social_security_tax
        self.medicare_tax = deps.medicare_tax
        self.federal_income_tax = deps.federal_income_tax
        self.state_income_tax = deps.state_income_tax
        self.local_tax = deps.local_tax

    def calculate_total_tax(self, se_income: float, taxable_income: float) -> float:
        return (
            self.social_security_tax.calculate(se_income)
            + self.medicare_tax.calculate(se_income)
            + self.federal_income_tax.calculate(taxable_income)
            + self.state_income_tax.calculate(taxable_income)
            + self.local_tax.calculate(taxable_income)
        )

    def as_dict(self) -> Dict[str, float]:
        return {
            "Social Security Tax": self.social_security_tax.calculate,
            "Medicare Tax": self.medicare_tax.calculate,
            "Federal Tax": self.federal_income_tax.calculate,
            "State Tax": self.state_income_tax.calculate,
            "Local Tax": self.local_tax.calculate,
        }
