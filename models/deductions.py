# models/deductions.py
"""
Provides available deductions for a business based on type and filing status.
"""

def get_available_deductions(business, filing_status, se_tax):
    """
    Returns a dictionary of applicable deductions. For now, uses simplified assumptions.
    """
    deductions = {}

    # Standard business expenses
    deductions['operating_expenses'] = business.operating_expenses

    # Self-employment tax deduction (half of SE tax)
    deductions['se_tax_deduction'] = round(se_tax * 0.50, 2)

    # Health insurance premiums (if applicable)
    if hasattr(business, 'health_premiums'):
        deductions['health_insurance'] = business.health_premiums

    # Retirement contributions (if applicable)
    if hasattr(business, 'retirement_contributions'):
        deductions['retirement'] = business.retirement_contributions

    # Home office expenses (if applicable)
    if hasattr(business, 'home_office_expenses'):
        deductions['home_office'] = business.home_office_expenses

    return deductions
