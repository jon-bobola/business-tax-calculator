from app.model.deduction.base_deduction import BaseDeduction
from app.model.deduction.deduction_constants import DeductionName
from app.utils.decorators import classproperty
from typing import Any


class RetirementContributionDeduction(BaseDeduction):
    """Retirement contribution deduction."""

    @classproperty
    def name(cls) -> DeductionName:
        return DeductionName.RETIREMENT_CONTRIBUTION_DEDUCTION