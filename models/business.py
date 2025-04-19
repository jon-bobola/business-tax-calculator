# models/business.py

class Business:
    def __init__(
        self=0.0,
        revenue=0.0,
        expenses=0.0,
        entity_type="",
        reasonable_salary=0.0,
        health_premiums=0.0,
        retirement_contributions=0.0,
        home_office_expenses=0.0,
        local_tax_rate=None,
        state_brackets=None,
    ):
        self.revenue = revenue
        self.expenses = expenses
        self.operating_expenses = expenses  # Explicitly assign for deduction logic
        self.entity_type = entity_type
        self.reasonable_salary = reasonable_salary
        self.health_premiums = health_premiums
        self.retirement_contributions = retirement_contributions
        self.home_office_expenses = home_office_expenses
        self.local_tax_rate = local_tax_rate
        self.state_brackets = state_brackets

    def get_net_income(self):
        return max(0.0, self.revenue - self.expenses)

    def get_taxable_compensation(self):
        if self.entity_type in ["Sole Proprietorship", "LLC"]:
            return self.get_net_income()
        elif self.entity_type == "S-Corp":
            return self.reasonable_salary
        return 0.0
