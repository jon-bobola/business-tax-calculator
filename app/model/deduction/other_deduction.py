from app.model.deduction.base_deduction import BaseDeduction
from app.model.deduction.deduction_constants import DeductionName
from app.utils.decorators import classproperty

class OtherDeduction(BaseDeduction):
    """Other miscellaneous deductions."""
    
    @classproperty
    def name(cls) -> DeductionName:
        return DeductionName.OTHER_DEDUCTION