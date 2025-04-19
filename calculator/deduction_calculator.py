"""
Deduction calculation module for the Business Tax Calculator.
"""
from utils.config import (
    STANDARD_DEDUCTION, 
    RETIREMENT_CONTRIBUTION_LIMITS,
    HEALTH_INSURANCE_DEDUCTION_RATE,
    HOME_OFFICE_DEDUCTION_RATE
)

def calculate_total_deductions(business, filing_status="Single"):
    """
    Calculate total deductions for a business.
    
    Args:
        business (Business): The business object
        filing_status (str): Tax filing status
        
    Returns:
        float: Total deductions amount
        dict: Breakdown of deductions
    """
    deductions = {}
    
    # Standard deduction based on filing status
    deductions["standard"] = STANDARD_DEDUCTION.get(filing_status, STANDARD_DEDUCTION["Single"])
    
    # Retirement contributions
    deductions["retirement"] = min(
        business.retirement_contributions,
        RETIREMENT_CONTRIBUTION_LIMITS.get("401k", 23000)
    )
    
    # Health insurance premiums
    deductions["health_insurance"] = business.health_insurance_premiums * HEALTH_INSURANCE_DEDUCTION_RATE
    
    # Home office deduction
    deductions["home_office"] = business.home_office_deduction
    
    # Other business deductions
    deductions["other"] = business.other_deductions
    
    # Calculate total deductions
    total_deductions = sum(deductions.values())
    
    return total_deductions, deductions

def get_deduction_breakdown(deductions):
    """
    Get a formatted breakdown of deductions.
    
    Args:
        deductions (dict): Deductions breakdown
        
    Returns:
        str: Formatted deduction breakdown
    """
    breakdown = "Deduction Breakdown:\n"
    for category, amount in deductions.items():
        formatted_category = category.replace("_", " ").title()
        breakdown += f"  {formatted_category}: ${amount:,.2f}\n"
    
    return breakdown