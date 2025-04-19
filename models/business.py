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
        self.retirement_contributions = 0.0
        self.health_insurance_premiums = 0.0
        self.home_office_deduction = 0.0
        self.other_deductions = 0.0
        self.estimated_tax_payments = 0.0

    def get_net_income(self):
        """Calculate net income before tax deductions."""
        return self.revenue - self.expenses

    def __str__(self):
        """String representation of the business."""
        return f"""
Business: {self.name}
Entity Type: {self.entity_type}
Revenue: ${self.revenue:,.2f}
Expenses: ${self.expenses:,.2f}
Net Income: ${self.get_net_income():,.2f}
Employees: {self.employee_count}
"""