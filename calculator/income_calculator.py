"""
Income calculation module for the Business Tax Calculator.
"""
from utils.config import TAX_RATES, SELF_EMPLOYMENT_TAX_RATE, SOCIAL_SECURITY_WAGE_BASE

def calculate_taxable_income(business, total_deductions):
    """
    Calculate taxable income after deductions.
    
    Args:
        business (Business): The business object
        total_deductions (float): Total deductions amount
        
    Returns:
        float: Taxable income
    """
    net_income = business.get_net_income()
    taxable_income = max(0, net_income - total_deductions)
    return taxable_income

def calculate_income_tax(business, taxable_income):
    """
    Calculate income tax based on entity type and taxable income.
    
    Args:
        business (Business): The business object
        taxable_income (float): Taxable income after deductions
        
    Returns:
        float: Income tax amount
    """
    entity_type = business.entity_type
    
    # For C-Corps, use flat corporate tax rate
    if entity_type == "C-Corp":
        return taxable_income * TAX_RATES[entity_type]
    
    # For pass-through entities, use progressive tax brackets
    tax_brackets = TAX_RATES[entity_type]
    total_tax = 0
    
    for min_income, max_income, rate in tax_brackets:
        if taxable_income > min_income:
            bracket_income = min(taxable_income, max_income) - min_income
            bracket_tax = bracket_income * rate
            total_tax += bracket_tax
            
            if taxable_income <= max_income:
                break
    
    return total_tax

def calculate_self_employment_tax(business, taxable_income):
    """
    Calculate self-employment tax for sole proprietorships and some LLCs.
    
    Args:
        business (Business): The business object
        taxable_income (float): Taxable income after deductions
        
    Returns:
        float: Self-employment tax amount
    """
    if business.entity_type in ["Sole Proprietorship", "LLC"]:
        # Social Security portion (12.4%) is capped at the wage base
        social_security_income = min(taxable_income, SOCIAL_SECURITY_WAGE_BASE)
        social_security_tax = social_security_income * 0.124
        
        # Medicare portion (2.9%) applies to all income
        medicare_tax = taxable_income * 0.029
        
        return social_security_tax + medicare_tax
    
    # S-Corps and C-Corps handle employment taxes differently
    return 0.0