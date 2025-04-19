# calculator/deduction_calculator.py
"""
Deduction calculator module for total and categorized deductions.
"""

from models.deductions import get_available_deductions

def calculate_total_deductions(business, filing_status, se_tax):
    """
    Calculates the total deductions including SE tax adjustments and other business deductions.
    """
    deductions = get_available_deductions(business, filing_status, se_tax)
    total = sum(deductions.values())
    return total, deductions


def get_deduction_breakdown(business, filing_status, se_tax):
    """
    Returns the breakdown of deductions used in calculation.
    """
    return get_available_deductions(business, filing_status, se_tax)


def calculate_qbi_deduction(business, taxable_income, filing_status):
    """
    Computes the Qualified Business Income deduction (20% of qualified income), with placeholder logic.
    """
    if business.entity_type not in ["Sole Proprietorship", "LLC", "S-Corp"]:
        return 0.0
    qualified_income = max(0.0, business.get_net_income())
    return round(qualified_income * 0.20, 2)
