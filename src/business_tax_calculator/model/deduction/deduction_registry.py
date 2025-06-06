from business_tax_calculator.model.deduction.base_deduction import BaseDeduction
from business_tax_calculator.model.deduction.business_expenses_deduction import BusinessExpensesDeduction
from business_tax_calculator.model.deduction.self_employment_tax_deduction import SelfEmploymentTaxDeduction
from business_tax_calculator.model.deduction.health_insurance_deduction import HealthInsuranceDeduction
from business_tax_calculator.model.deduction.retirement_contribution_deduction import RetirementContributionDeduction
from business_tax_calculator.model.deduction.home_office_deduction import HomeOfficeDeduction
from business_tax_calculator.model.deduction.other_deduction import OtherDeduction
from business_tax_calculator.model.deduction.deduction_constants import DeductionName
from typing import List

class DeductionRegistry:
    """Registry that manages available deduction types."""

    def __init__(self):
        self._deductions: List[BaseDeduction] = []
        self._register_default_deductions()

    def _register_default_deductions(self):
        """Register all standard deduction types."""
        self.register(BusinessExpensesDeduction())
        self.register(SelfEmploymentTaxDeduction())
        self.register(HealthInsuranceDeduction())
        self.register(RetirementContributionDeduction())
        self.register(HomeOfficeDeduction())
        self.register(OtherDeduction())

    def register(self, deduction: BaseDeduction):
        """Register a new deduction type."""
        self._deductions.append(deduction)

    def get_available_deductions(self) -> List[BaseDeduction]:
        return self._deductions
    
    def get_deduction_by_name(self, name: DeductionName) -> BaseDeduction:
        """Get a deduction by its name."""
        for deduction in self._deductions:
            if deduction.name == name:
                return deduction
        raise ValueError(f"Deduction '{name}' not found in registry.")