# calculator/income_calculator.py
"""
Income calculation module refactored to use tax_liabilities classes.
"""

from tax_liabilities.federal_income_tax_liability import FederalIncomeTaxLiability
from tax_liabilities.social_security_tax_liability import SocialSecurityTaxLiability
from tax_liabilities.medicare_tax_liability import MedicareTaxLiability


def calculate_taxable_income(business, total_deductions, qbi_deduction=0.0):
    """
    Calculate taxable income after deductions.
    """
    net_income = business.get_net_income()
    taxable = net_income - total_deductions - qbi_deduction
    return max(0.0, taxable)


def calculate_income_tax(business, taxable_income):
    """
    Delegate federal tax computation to FederalIncomeTaxLiability.
    """
    if taxable_income <= 0:
        return 0.0
    fed = FederalIncomeTaxLiability()
    return fed.calculate(taxable_income)


def calculate_self_employment_tax(business, taxable_income):
    """
    Delegate SE/payroll tax to SocialSecurity and Medicare liability classes.
    Returns (total, ss_tax, med_tax).
    """
    # Determine compensation
    if business.entity_type in ("Sole Proprietorship", "LLC"):
        comp = business.get_taxable_compensation()
    elif business.entity_type == "S-Corp":
        comp = business.reasonable_salary
    else:
        return 0.0, 0.0, 0.0

    ss_calc = SocialSecurityTaxLiability()
    med_calc = MedicareTaxLiability()
    ss_tax = ss_calc.calculate(comp)
    med_tax = med_calc.calculate(comp)
    return ss_tax + med_tax, ss_tax, med_tax


def calculate_effective_tax_rate(total_tax, net_income):
    """
    Percentage of net income paid in tax.
    """
    if net_income <= 0:
        return 0.0
    return (total_tax / net_income) * 100.0
