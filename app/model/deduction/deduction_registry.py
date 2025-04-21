from app.model.deduction.business_expenses_deduction import BusinessExpensesDeduction
from app.model.deduction.deduction import Deduction
from app.model.deduction.health_insurance_deduction import HealthInsuranceDeduction
from app.model.deduction.home_office_deduction import HomeOfficeDeduction
from app.model.deduction.other_deduction import OtherDeduction
from app.model.deduction.retirement_contribution_deduction import RetirementContributionDeduction
from app.model.deduction.self_employment_tax_deduction import SelfEmploymentTaxDeduction


from typing import Any, Dict, List


class DeductionRegistry:
    """Registry that manages available deduction types."""

    def __init__(self):
        self._deductions: List[Deduction] = []
        self._register_default_deductions()

    def _register_default_deductions(self):
        """Register all standard deduction types."""
        self.register(BusinessExpensesDeduction())
        self.register(SelfEmploymentTaxDeduction())
        self.register(HealthInsuranceDeduction())
        self.register(RetirementContributionDeduction())
        self.register(HomeOfficeDeduction())
        self.register(OtherDeduction())

    def register(self, deduction: Deduction):
        """Register a new deduction type."""
        self._deductions.append(deduction)

    def get_available_deductions(self, business: Any, filing_status: str, **kwargs) -> Dict[str, float]:
        """
        Calculate all applicable deductions for the given business and filing status.

        Args:
            business: The business entity
            filing_status: Tax filing status
            kwargs: Additional parameters needed for calculation

        Returns:
            Dict[str, float]: Dictionary mapping deduction names to amounts
        """
        result = {}
        for deduction in self._deductions:
            if deduction.is_applicable(business, filing_status):
                amount = deduction.calculate(business, filing_status, **kwargs)
                if amount > 0:
                    result[deduction.get_name()] = amount
        return result