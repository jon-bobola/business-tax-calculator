"""
Income calculation module for the Business Tax Calculator.
"""
from utils.config import (
    TAX_RATES, 
    SOCIAL_SECURITY_TAX_RATE, 
    MEDICARE_TAX_RATE,
    SOCIAL_SECURITY_WAGE_BASE,
    LOCAL_INCOME_TAX_RATE
)

def calculate_taxable_income(business, total_deductions, qbi_deduction=0):
    """
    Calculate taxable income after deductions.
    
    Args:
        business (Business): The business object
        total_deductions (float): Total deductions amount
        qbi_deduction (float): Qualified Business Income Deduction amount
        
    Returns:
        float: Taxable income
    """
    net_income = business.get_net_income()
    # Ensure taxable income is never negative
    taxable_income = max(0, net_income - total_deductions - qbi_deduction)
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
    # If taxable income is zero, no tax is due
    if taxable_income <= 0:
        return 0
    
    entity_type = business.entity_type
    
    # Handle potential KeyError if entity_type is not in TAX_RATES
    if entity_type not in TAX_RATES:
        raise ValueError(f"Unknown entity type: {entity_type}")
    
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
    Calculate self-employment tax components for sole proprietorships and some LLCs.
    
    Args:
        business (Business): The business object
        taxable_income (float): Taxable income after deductions
        
    Returns:
        tuple: (total self-employment tax, social security tax, medicare tax)
    """
    # If taxable income is zero, no tax is due
    if taxable_income <= 0:
        return 0, 0, 0
    
    social_security_tax = 0
    medicare_tax = 0
    
    if business.entity_type in ["Sole Proprietorship", "LLC"]:
        # For Sole Props and LLCs, use net income for SE tax calculation
        taxable_compensation = business.get_taxable_compensation()
        
        # Social Security portion (12.4%) is capped at the wage base
        social_security_income = min(taxable_compensation, SOCIAL_SECURITY_WAGE_BASE)
        social_security_tax = social_security_income * SOCIAL_SECURITY_TAX_RATE
        
        # Medicare portion (2.9%) applies to all income
        medicare_tax = taxable_compensation * MEDICARE_TAX_RATE
    
    elif business.entity_type == "S-Corp":
        # For S-Corps, only the reasonable salary is subject to employment taxes
        # Business owners pay these through W-2 withholding, so we don't calculate it
        # as self-employment tax, but we do want to track it for reporting
        social_security_income = min(business.reasonable_salary, SOCIAL_SECURITY_WAGE_BASE)
        social_security_tax = social_security_income * SOCIAL_SECURITY_TAX_RATE
        medicare_tax = business.reasonable_salary * MEDICARE_TAX_RATE
    
    # Total self-employment tax (or equivalent payroll tax for S-Corps)
    total_tax = social_security_tax + medicare_tax
    
    return total_tax, social_security_tax, medicare_tax

def calculate_local_income_tax(business, taxable_income):
    """
    Calculate estimated local/state income tax.
    
    Args:
        business (Business): The business object
        taxable_income (float): Taxable income after federal deductions
        
    Returns:
        float: Local income tax amount
    """
    if hasattr(business, 'local_tax_rate') and business.local_tax_rate > 0:
        local_rate = business.local_tax_rate
    else:
        local_rate = LOCAL_INCOME_TAX_RATE  # Default from config
    
    return taxable_income * local_rate

def calculate_effective_tax_rate(total_tax, net_income):
    """
    Calculate the effective tax rate.
    
    Args:
        total_tax (float): Total tax amount
        net_income (float): Net business income
        
    Returns:
        float: Effective tax rate as a percentage
    """
    if net_income <= 0:
        return 0
    
    return (total_tax / net_income) * 100