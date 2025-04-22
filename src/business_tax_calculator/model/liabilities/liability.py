from abc import ABC, abstractmethod

class Liability(ABC):
    
    def __init__(self):
        self._value = 0.0
        pass

    @abstractmethod
    def calculate(self, taxable_income: float) -> float:
        pass

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, new_value: float):
        self._value = new_value