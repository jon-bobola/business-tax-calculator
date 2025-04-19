# business_tax_calculator/deductions.py
from dataclasses import dataclass
from typing import Dict

from constants import DeductionRates


@dataclass
class StandardDeduction:
    amount: float = DeductionRates.STANDARD.value


@dataclass
class SocialSecurityDeduction:
    amount: float = DeductionRates.SOCIAL_SECURITY.value


@dataclass
class MedicareDeduction:
    amount: float = DeductionRates.MEDICARE.value


@dataclass
class QualifiedBusinessIncomeDeduction:
    amount: float = DeductionRates.QBI.value


class TaxDeductionDependencies:
    def __init__(self):
        self.standard = StandardDeduction()
        self.soc_sec = SocialSecurityDeduction()
        self.medicare = MedicareDeduction()
        self.qbi = QualifiedBusinessIncomeDeduction()


class TaxDeduction:
    def __init__(self, dependencies: TaxDeductionDependencies):
        self.standard = dependencies.standard
        self.social_security_deduction = dependencies.soc_sec
        self.medicare_deduction = dependencies.medicare
        self.qbi_deduction = dependencies.qbi

    def calculate_total_deductions(self, ss_tax, med_tax, qbi_base) -> float:
        return (
            self.standard.amount
            + self.social_security_deduction.amount
            + self.medicare_deduction.amount
            + min(self.qbi_deduction.amount, qbi_base * 0.2)
        )

    def as_dict(self) -> Dict[str, float]:
        return {
            "Standard Deduction": self.standard.amount,
            "Social Security Deduction": self.socialial_security_deduction.amount,
            "Medicare Deduction": self.medicare_deduction.amount,
            "QBI Deduction": self.qbi_deduction.amount,
        }
