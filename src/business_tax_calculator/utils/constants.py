from enum import Enum


class EntityType(Enum):
    SOLE_PROPRIETOR = "Sole Proprietor"
    S_CORP = "S-Corporation"


class ResultKeys(Enum):
    ENTITY_TYPE = "Entity Type"
    GROSS_REVENUE = "Gross Revenue"
    EXPENSES = "Expenses"
    NET_REVENUE = "Net Revenue"
    GROSS_SALARY = "Gross Salary"
    GROSS_DISTRIBUTIONS = "Distributions"
    STANDARD_DEDUCTION = "Standard Deduction"
    SOCIAL_SECURITY_DEDUCTION = "Social Security Deduction"
    MEDICARE_DEDUCTION = "Medicare Deduction"
    QBI_DEDUCTION = "Qualified Business Income Deduction"
    TAXABLE_PERSONAL_INCOME = "Taxable Personal Income"
    SOCIAL_SECURITY_TAX = "Social Security Tax"
    MEDICARE_TAX = "Medicare Tax"
    FEDERAL_TAX = "Federal Income Tax"
    STATE_TAX = "State Income Tax"
    LOCAL_TAX = "Local Tax"
    TOTAL_TAX = "Total Tax"


class TaxRates(Enum):
    EMPLOYER_FICA_TAX_RATE = 0.9235


class DeductionRates(Enum):
    STANDARD = 13850  # 2024 single filer standard deduction
    SOCIAL_SECURITY = 0  # not a separate deduction usually, but included for modeling
    MEDICARE = 0  # same as above
    QBI = 0.20  # 20% of qualified business income
    SELF_EMP_EMP_RATE = 0.5  # 50% deductible portion of SE tax


class MarginalTaxBrackets(Enum):
    FEDERAL = [
        (0, 11000, 0.10),
        (11001, 44725, 0.12),
        (44726, 95375, 0.22),
        (95376, 182100, 0.24),
        (182101, 231250, 0.32),
        (231251, 578125, 0.35),
        (578126, float("inf"), 0.37),
    ]
    STATE = [
        (0, 10000, 0.03),
        (10001, 25000, 0.05),
        (25001, float("inf"), 0.07),
    ]
