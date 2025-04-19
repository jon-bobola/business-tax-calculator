"""
Deduction calculation module for the Business Tax Calculator.
"""
from utils.config import (
    STANDARD_DEDUCTION, 
    RETIREMENT_CONTRIBUTION_LIMITS,
    HEALTH_INSURANCE_DEDUCTION_RATE,
    HOME_OFFICE_DEDUCTION_RATE,
    QBI_DEDUCTION_RATE,
    QBI_INCOME_THRESHOLD_SINGLE,
    QBI_INCOME_THRESHOLD_JOINT,
    SELF_EMPLOYMENT_TAX_DEDUCTION
)

def calculate_total_deductions(business, filing_status="Single", self_employment_tax=0):
    """
    Calculate total deductions for a business.
    
    Args:
        business (Business): The business object
        filing_status (str): Tax filing status
        self_employment_tax (float): Self-employment tax amount for deduction calculation
        
    Returns:
        float: Total deductions amount
        dict: Breakdown of deductions
    """
    deductions = {}
    
    # Standard deduction based on filing status
    deductions["standard"] = STANDARD_DEDUCTION.get(filing_status, STANDARD_DEDUCTION["Single"])
    
    # Retirement contributions
    if hasattr(business, 'retirement_contributions'):
        deductions["retirement"] = min(
            business.retirement_contributions,
            RETIREMENT_CONTRIBUTION_LIMITS.get("401k", 23000)
        )
    else:
        deductions["retirement"] = 0
    
    # Health insurance premiums
    if hasattr(business, 'health_insurance_premiums'):
        deductions["health_insurance"] = business.health_insurance_premiums * HEALTH_INSURANCE_DEDUCTION_RATE
    else:
        deductions["health_insurance"] = 0
    
    # Home office deduction
    if hasattr(business, 'home_office_deduction'):
        deductions["home_office"] = business.home_office_deduction
    else:
        deductions["home_office"] = 0
    
    # Other business deductions
    if hasattr(business, 'other_deductions'):
        deductions["other"] = business.other_deductions
    else:
        deductions["other"] = 0
    
    # Self-employment tax deduction (50% of SE tax)
    if business.entity_type in ["Sole Proprietorship", "LLC"]:
        deductions["self_employment_tax"] = self_employment_tax * SELF_EMPLOYMENT_TAX_DEDUCTION
    else:
        deductions["self_employment_tax"] = 0
    
    # Calculate total deductions
    total_deductions = sum(deductions.values())
    
    return total_deductions, deductions

def calculate_qbi_deduction(business, taxable_income, filing_status="Single"):
    """
    Calculate Qualified Business Income Deduction (Section 199A).
    
    Args:
        business (Business): The business object
        taxable_income (float): Taxable income after other deductions
        filing_status (str): Tax filing status
        
    Returns:
        float: QBI deduction amount
    """
    # QBI only applies to pass-through entities, not C-Corps
    if business.entity_type == "C-Corp":
        return 0
    
    net_income = business.get_net_income()
    
    # Calculate 20% of qualified business income
    potential_deduction = net_income * QBI_DEDUCTION_RATE
    
    # Check income thresholds for phase-out
    threshold = QBI_INCOME_THRESHOLD_JOINT if filing_status == "Married Filing Jointly" else QBI_INCOME_THRESHOLD_SINGLE
    
    # If income is below threshold, use full deduction
    if taxable_income <= threshold:
        qbi_deduction = potential_deduction
    else:
        # Phase-out calculation would go here (simplified version)
        # In a real implementation, this would be more complex based on
        # specified service trades or businesses (SSTBs) and W-2 wages
        phase_out_ratio = max(0, min(1, (threshold * 1.2 - taxable_income) / (threshold * 0.2)))
        qbi_deduction = potential_deduction * phase_out_ratio
    
    # QBI deduction cannot exceed 20% of taxable income
    return min(potential_deduction, taxable_income * QBI_DEDUCTION_RATE)

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