"""
models/deductions.py

Provides a class hierarchy for business tax deductions with an abstract base class
and specific implementations for different deduction types.
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
from app.model.deduction import Deduction, BusinessExpensesDeduction, HealthInsuranceDeduction, HomeOfficeDeduction, OtherDeduction, RetirementContributionDeduction, SelfEmploymentTaxDeduction

from app.model.deduction.deduction_registry import DeductionRegistry


class BusinessDeduction(Deduction):
    tax_deductions = []
    tax_deductions.append(BusinessExpensesDeduction())
    tax_deductions.append(HealthInsuranceDeduction())
    tax_deductions.append(HomeOfficeDeduction())
    tax_deductions.append(OtherDeduction())
    tax_deductions.append(RetirementContributionDeduction())
    tax_deductions.append(SelfEmploymentTaxDeduction())
    
    """Abstract base class for all deduction types."""
    
    @abstractmethod
    def get_name(self) -> str:
        """Returns the human-readable name of the deduction."""
        pass
    
    @abstractmethod
    def is_applicable(self, business: Any, filing_status: str) -> bool:
        """
        Determines if this deduction is applicable for the given business and filing status.
        
        Args:
            business: The business entity
            filing_status: Tax filing status (e.g., "Single", "Married Filing Jointly")
            
        Returns:
            bool: True if the deduction applies, False otherwise
        """
        pass
    
    @abstractmethod
    def calculate(self, business: Any, filing_status: str, **kwargs) -> float:
        """
        Calculates the amount of this deduction.
        
        Args:
            business: The business entity
            filing_status: Tax filing status (e.g., "Single", "Married Filing Jointly")
            kwargs: Additional parameters needed for calculation
            
        Returns:
            float: The deduction amount
        """
        pass


# Global registry instance
_registry = DeductionRegistry()


def register_deduction(deduction: Deduction):
    """Register a custom deduction type with the global registry."""
    _registry.register(deduction)


def get_available_deductions(business: Any, filing_status: str, se_tax: float) -> Dict[str, float]:
    """
    Returns a dictionary of applicable deductions for the given business.
    
    Args:
        business: The business entity
        filing_status: Tax filing status
        se_tax: Self-employment tax amount used for SE tax deduction calculation
        
    Returns:
        Dict[str, float]: Dictionary mapping deduction names to amounts
    """
    return _registry.get_available_deductions(business, filing_status, se_tax=se_tax)