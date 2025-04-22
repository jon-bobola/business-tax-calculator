from business_tax_calculator.model.deduction.base_deduction import BaseDeduction
from business_tax_calculator.model.deduction.deduction_constants import DeductionName
from business_tax_calculator.utils.decorators import classproperty

class HealthInsuranceDeduction(BaseDeduction):

    @classproperty
    def name(cls) -> DeductionName:
        return DeductionName.HEALTH_INSURANCE_DEDUCTION
        
    @property
    def value(self) -> float:
        return 0.0  # Replace with actual calculation logic