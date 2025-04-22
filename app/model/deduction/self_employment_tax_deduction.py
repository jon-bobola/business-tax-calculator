from app.model.deduction.base_deduction import BaseDeduction
from app.model.deduction.deduction_constants import DeductionName
from app.utils.decorators import classproperty
from typing import Any


class SelfEmploymentTaxDeduction(BaseDeduction):

    @classproperty
    def name(cls) -> DeductionName:
        return DeductionName.SELF_EMPLOYMENT_TAX_DEDUCTION
        
    @property
    def value(self) -> float:
        return 0.0  # Replace with actual calculation logic