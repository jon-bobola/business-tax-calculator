from abc import ABC

class BaseTaxRate(ABC):
	# This class represents a base tax rate.
    # It is an abstract base class that inherits from ABC (Abstract Base Class).
    # This class is intended to be subclassed for specific tax rates.
    
    
    @property
    def name(self) -> str:
        return self.name
    
    @property
    def value(self) -> float:
        return self.value

    def __init__(self, name: str, value: float):
        self.name = name
        self.value = value