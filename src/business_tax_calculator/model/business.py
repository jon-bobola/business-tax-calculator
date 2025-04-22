from typing import Dict
from business_tax_calculator.model.tax_return import TaxReturn
from business_tax_calculator.model.deduction.deduction_constants import DeductionName

class Business:
    def __init__(self):
        
        self.tax_return = TaxReturn()
        
        self.name = ""
        self.entity_type = ""
        self.state = ""
        self.revenue = 0.0
        self.expenses = 0.0
        self.reasonable_salary = 0.0
        self.retirement_contributions = 0.0
        self.health_insurance_premiums = 0.0
        self.home_office_deduction = 0.0
        self.other_deductions = 0.0
        self.local_tax_rate = 0.0
        self.estimated_tax_payments = 0.0
        self.employee_count = 0
        self.filing_status = "Single"
        self.profit_distributions = 0.0
        

    # Setter methods
    def set_name(self, name: str):
        self.name = name

    def set_entity_type(self, entity_type: str):
        self.entity_type = entity_type

    def set_state(self, state: str):
        self.state = state

    def set_revenue(self, revenue: float):
        self.revenue = revenue

    def set_expenses(self, expenses: float):
        self.expenses = expenses

    def set_reasonable_salary(self, salary: float):
        self.reasonable_salary = salary

    def set_retirement_contributions(self, contributions: float):
        self.retirement_contributions = contributions

    def set_health_insurance_premiums(self, premiums: float):
        self.health_insurance_premiums = premiums

    def set_home_office_deduction(self, deduction: float):
        self.home_office_deduction = deduction

    def set_other_deductions(self, deductions: float):
        self.other_deductions = deductions

    def set_local_tax_rate(self, rate: float):
        self.local_tax_rate = rate

    def set_estimated_tax_payments(self, payments: float):
        self.estimated_tax_payments = payments

    def set_employee_count(self, count: int):
        self.employee_count = count

    def set_filing_status(self, status: str):
        self.filing_status = status

    def set_profit_distributions(self, distributions: float):
        self.profit_distributions = distributions

    # Getter methods
    def get_name(self):
        return self.name

    def get_entity_type(self):
        return self.entity_type

    def get_state(self):
        return self.state

    def get_revenue(self):
        return self.revenue

    def get_expenses(self):
        return self.expenses

    def get_reasonable_salary(self):
        return self.reasonable_salary

    def get_retirement_contributions(self):
        return self.retirement_contributions

    def get_health_insurance_premiums(self):
        return self.health_insurance_premiums

    def get_home_office_deduction(self):
        return self.home_office_deduction

    def get_other_deductions(self):
        return self.other_deductions

    def get_local_tax_rate(self):
        return self.local_tax_rate

    def get_estimated_tax_payments(self):
        return self.estimated_tax_payments

    def get_employee_count(self):
        return self.employee_count

    def get_filing_status(self):
        return self.filing_status

    def get_profit_distributions(self):
        return self.profit_distributions

    # Calculate net income (Revenue - Expenses)
    def get_net_income(self):
        return self.revenue - self.expenses
    
    def get_taxable_compensation(self) -> float:
        """
        Returns the portion of net income subject to self‑employment tax:
        92.35% of net earnings, per IRS rules.
        """
        net = self.get_net_income()
        return max(0.0, net * 0.9235)


    def get_deductions(self) -> Dict[DeductionName, float]:
        return self.tax_return.deduction_registry.get_available_deductions(self, self.filing_status)