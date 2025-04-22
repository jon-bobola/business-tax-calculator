from abc import ABC, abstractmethod
from app.utils.decorators import classproperty
from app.model.deduction.deduction_constants import DeductionName

class BaseDeduction(ABC):
    def __init__(self):
        self._name: DeductionName = None
        self._value: float = 0.0
    
    @classproperty
    @abstractmethod
    def name(cls) -> DeductionName:
        pass

    @property
    @abstractmethod
    def value(self) -> float:
        pass