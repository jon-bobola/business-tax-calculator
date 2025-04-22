from enum import StrEnum

class DeductionName(StrEnum):
    BUSINESS_EXPENSES_DEDUCTION = "Business Expenses Deduction"
    SELF_EMPLOYMENT_TAX_DEDUCTION = "Self Employment Tax Deduction"
    HEALTH_INSURANCE_DEDUCTION = "Health Insurance Deduction"
    RETIREMENT_CONTRIBUTION_DEDUCTION = "Retirement Contribution Deduction"
    HOME_OFFICE_DEDUCTION = "Home Office Deduction"
    OTHER_DEDUCTION = "Other Deduction"
    QBI_DEDUCTION = "Qualified Business Income Deduction"