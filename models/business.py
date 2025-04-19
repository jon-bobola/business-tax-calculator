"""
Business data model for the tax calculator.
"""

class Business:
    """
    Represents a business entity with relevant financial information for tax calculations.
    """
    def __init__(self):
        self.name = ""
        self.entity_type = ""  # Sole Proprietorship, LLC, S-Corp, C-Corp
        self.revenue = 0.0
        self.expenses = 0.0
        self.employee_count = 0
        self.reasonable_salary = 0.0  # For S-Corp owners
        self.retirement_contributions = 0.0
        self.health_insurance_premiums = 0.0
        self.home_office_deduction = 0.0
        self.other_deductions = 0.0
        self.estimated_tax_payments = 0.0
        self.state = ""  # State for local tax calculations
        self.local_tax_rate = 0.05  # Default local tax rate (5%)

    def get_net_income(self):
        """Calculate net income before tax deductions."""
        return self.revenue - self.expenses

    def get_profit_distributions(self):
        """
        Calculate profit distributions (for S-Corps).
        For other entity types, this will be zero.
        """
        if self.entity_type == "S-Corp":
            return max(0, self.get_net_income() - self.reasonable_salary)
        return 0.0

    def get_taxable_compensation(self):
        """
        For S-Corps, this is the reasonable salary.
        For other entity types, it's the net income.
        """
        if self.entity_type == "S-Corp":
            return self.reasonable_salary
        return self.get_net_income()

    def __str__(self):
        """String representation of the business."""
        result = f"""
Business: {self.name}
Entity Type: {self.entity_type}
Revenue: ${self.revenue:,.2f}
Expenses: ${self.expenses:,.2f}
Net Income: ${self.get_net_income():,.2f}
Employees: {self.employee_count}
"""
        
        if self.entity_type == "S-Corp":
            result += f"Reasonable Salary: ${self.reasonable_salary:,.2f}\n"
            result += f"Profit Distributions: ${self.get_profit_distributions():,.2f}\n"
            
        return result