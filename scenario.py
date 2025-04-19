# business_tax_calculator/scenario.py
from abc import ABC, abstractmethod
from typing import Dict, Any

from deductions import TaxDeduction
from liabilities import TaxLiability
from constants import EntityType, ResultKeys, TaxRates, DeductionRates


class TaxScenario(ABC):
    def __init__(
        self,
        gross_revenue: float,
        expenses: float,
        salary: float,
        entity_type: str,
        tax_deduction: TaxDeduction,
        tax_liability: TaxLiability,
    ):
        self.gross_revenue = gross_revenue
        self.expenses = expenses
        self.salary = salary
        self.entity_type = entity_type
        self.net_revenue = gross_revenue - expenses
        self.distributions = self.net_revenue - salary
        self.tax_deductions = tax_deduction
        self.tax_liability = tax_liability
        self.taxable_income = 0
        self._validate_common()

    def _validate_common(self):
        if self.gross_revenue < 0 or self.expenses < 0 or self.salary < 0:
            raise ValueError("Revenue, expenses, and salary must be non-negative")
        if self.expenses > self.gross_revenue:
            # ideally use a logger here
            print("Warning: expenses exceed revenue")

    def calculate_taxable_income(
        self, ss_tax: float, med_tax: float, qbi_base: float
    ) -> float:
        total_ded = self.tax_deductions.calculate_total_deductions(
            ss_tax, med_tax, qbi_base
        )
        self.taxable_income = max(self.net_revenue - total_ded, 0)
        return self.taxable_income

    def calculate_taxes(self, se_income: float) -> float:
        return self.tax_liability.calculate_total_tax(se_income, self.taxable_income)

    @abstractmethod
    def calculate(self) -> Dict[str, Any]:
        ...
    

class SoleProprietorTaxScenario(TaxScenario):
    SELF_EMP_FACTOR = 1 - TaxRates.EMPLOYER_FICA_TAX_RATE.value

    def calculate(self):
        se_income = self.net_revenue * self.SELF_EMP_FACTOR
        ss_tax = self.tax_liability.social_security_tax.calculate(se_income)
        med_tax = self.tax_liability.medicare_tax.calculate(se_income)
        qbi_base = max(self.net_revenue - (ss_tax + med_tax) * DeductionRates.SELF_EMP_EMP_RATE.value, 0)
        self.calculate_taxable_income(ss_tax, med_tax, qbi_base)
        total_tax = self.calculate_taxes(se_income)
        return {
            **{
                ResultKeys.ENTITY_TYPE.value: self.entity_type,
                ResultKeys.GROSS_REVENUE.value: self.gross_revenue,
                ResultKeys.EXPENSES.value: self.expenses,
                ResultKeys.NET_REVENUE.value: self.net_revenue,
                ResultKeys.GROSS_SALARY.value: 0,
                ResultKeys.GROSS_DISTRIBUTIONS.value: self.distributions,
            },
            **self.tax_deductions.as_dict(),
            ResultKeys.TAXABLE_PERSONAL_INCOME.value: self.taxable_income,
            **self.tax_liability.as_dict(),
            ResultKeys.TOTAL_TAX.value: total_tax,
        }


class SCorpTaxScenario(TaxScenario):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.salary <= 0 and self.net_revenue > 0:
            print("Warning: S‑Corp with revenue but no salary")
        if self.salary > self.net_revenue:
            print("Warning: salary exceeds revenue")

    def calculate(self):
        se_income = self.salary
        ss_tax = self.tax_liability.social_security_tax.calculate(se_income)
        med_tax = self.tax_liability.medicare_tax.calculate(se_income)
        qbi_base = self.distributions
        self.calculate_taxable_income(ss_tax, med_tax, qbi_base)
        total_tax = self.calculate_taxes(se_income)
        return {
            **{
                ResultKeys.ENTITY_TYPE.value: self.entity_type,
                ResultKeys.GROSS_REVENUE.value: self.gross_revenue,
                ResultKeys.EXPENSES.value: self.expenses,
                ResultKeys.NET_REVENUE.value: self.net_revenue,
                ResultKeys.GROSS_SALARY.value: self.salary,
                ResultKeys.GROSS_DISTRIBUTIONS.value: self.distributions,
            },
            **self.tax_deductions.as_dict(),
            ResultKeys.TAXABLE_PERSONAL_INCOME.value: self.taxable_income,
            **self.tax_liability.as_dict(),
            ResultKeys.TOTAL_TAX.value: total_tax,
        }
