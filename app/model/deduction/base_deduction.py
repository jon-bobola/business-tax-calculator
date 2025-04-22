from abc import ABC, abstractmethod
from app.utils.decorators import classproperty
from app.model.deduction.deduction_constants import DeductionName

class BaseDeduction(ABC):
    
    @classproperty
    @abstractmethod
    def name(cls) -> DeductionName:
        pass