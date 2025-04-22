from app.model.business import Business
from app.model.deduction.base_deduction import BaseDeduction
from typing import List

"""
Deduction calculator module for total and categorized deductions.
"""

def calculate_total_deductions(business: Business) -> float:
    """
    Calculates the total deductions including SE tax adjustments and other business deductions.
    """
    total = 0.0

    deductions: List[BaseDeduction] = business.tax_return.deduction_registry.get_available_deductions()

    for deduction in deductions:
        total += deduction.value

    return total
    
def calculate_qbi_deduction(business, taxable_income, filing_status):
    """
    Computes the Qualified Business Income deduction (20% of qualified income), with income thresholds.
    """
    if business.entity_type not in ["Sole Proprietorship", "LLC", "S-Corp"]:
        return 0.0
    
    qualified_income = max(0.0, business.get_net_income())
    
    # 2023 income thresholds (these should be updated annually)
    thresholds = {
        "Single": 170_050,
        "Married Filing Jointly": 340_100,
        "Head of Household": 170_050
    }
    
    # Basic 20% deduction for incomes below threshold
    if taxable_income <= thresholds.get(filing_status, 0):
        return min(qualified_income * 0.20, taxable_income * 0.20)
    
    # More complex calculation needed for higher incomes
    # (would require additional W-2 wage and business property information)
    # This is a simplified implementation
    return round(qualified_income * 0.20, 2)

def get_deduction_breakdown(deduction_dict):
    """
    Returns a formatted string representation of the deduction breakdown.
    """
    if not deduction_dict:
        return "No deductions available."
    
    result = "DEDUCTION BREAKDOWN\n"
    for key, value in deduction_dict.items():
        formatted_key = key.replace('_', ' ').title()
        result += f"{formatted_key}: ${value:,.2f}\n"
    
    return result