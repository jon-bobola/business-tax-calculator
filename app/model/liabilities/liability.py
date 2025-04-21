from abc import ABC, abstractmethod
from app.model.filing_status.filing_status import FilingStatus

class Liability(ABC):
    
    def __init__(self):
        pass

    @abstractmethod
    def calculate(self, filing_status: FilingStatus, taxable_income: float) -> float:
        pass

    @property
    def value(self) -> float:
        return self.value