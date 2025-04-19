"""
Main tax calculator module for the Business Tax Calculator.
"""
from models.business import Business
from calculator.income_calculator import (
    calculate_taxable_income,
    calculate_income_tax,
    calculate_self_employment_tax
)
from calculator.deduction_calculator import (
    calculate_total_deductions,
    get_deduction_breakdown
)
from utils.helpers import (
    validate_number_input,
    validate_yes_no_input,
    format_currency,
    clear_screen,
    validate_entity_type
)

class BusinessTaxCalculator:
    """
    Main calculator class that handles the tax calculation workflow.
    """
    def __init__(self):
        self.business = Business()
        self.valid_entity_types = ["Sole Proprietorship", "LLC", "S-Corp", "C-Corp"]
        self.filing_status = "Single"
        self.has_home_office = False
        self.home_office_area = 0

    def run(self):
        """Run the tax calculator application."""
        self.display_welcome()
        self.collect_business_info()
        self.collect_income_info()
        self.collect_deduction_info()
        
        results = self.calculate_tax_liability()
        self.display_results(results)

    def display_welcome(self):
        """Display welcome message."""
        clear_screen()
        print("=" * 70)
        print("               BUSINESS TAX LIABILITY CALCULATOR")
        print("=" * 70)
        print("\nThis calculator helps estimate your business tax liability based on")
        print("revenue, expenses, entity type, and available deductions.\n")
        print("=" * 70)
        input("\nPress Enter to continue...")

    def collect_business_info(self):
        """Collect basic business information."""
        clear_screen()
        print("BUSINESS INFORMATION\n")
        
        self.business.name = input("Business name: ")
        self.business.entity_type = validate_entity_type(
            "Select business entity type:", 
            self.valid_entity_types
        )
        
        # For pass-through entities, collect filing status
        if self.business.entity_type in ["Sole Proprietorship", "LLC", "S-Corp"]:
            self.collect_filing_status()
        
        self.business.employee_count = int(validate_number_input("Number of employees (including yourself): ", 1))

    def collect_filing_status(self):
        """Collect tax filing status for pass-through entities."""
        valid_statuses = ["Single", "Married Filing Jointly", "Head of Household"]
        
        print("\nSelect filing status:")
        for i, status in enumerate(valid_statuses, 1):
            print(f"{i}. {status}")
        
        while True:
            try:
                choice = int(input("Enter your choice (number): "))
                if 1 <= choice <= len(valid_statuses):
                    self.filing_status = valid_statuses[choice - 1]
                    break
                else:
                    print(f"Error: Please enter a number between 1 and {len(valid_statuses)}.")
            except ValueError:
                print("Error: Please enter a valid number.")

    def collect_income_info(self):
        """Collect income and expense information."""
        clear_screen()
        print("INCOME AND EXPENSE INFORMATION\n")
        
        self.business.revenue = validate_number_input("Total business revenue: $", 0)
        self.business.expenses = validate_number_input("Total business expenses: $", 0)
        
        print(f"\nNet income before deductions: {format_currency(self.business.get_net_income())}")
        input("\nPress Enter to continue...")

    def collect_deduction_info(self):
        """Collect deduction information."""
        clear_screen()
        print("DEDUCTION INFORMATION\n")
        
        # Retirement contributions
        has_retirement = validate_yes_no_input("Do you have retirement contributions (y/n)? ")
        if has_retirement:
            self.business.retirement_contributions = validate_number_input(
                "Retirement contribution amount: $", 0
            )
        
        # Health insurance premiums
        has_health_insurance = validate_yes_no_input("Do you have health insurance premiums (y/n)? ")
        if has_health_insurance:
            self.business.health_insurance_premiums = validate_number_input(
                "Health insurance premium amount: $", 0
            )
        
        # Home office deduction
        self.has_home_office = validate_yes_no_input("Do you claim a home office deduction (y/n)? ")
        if self.has_home_office:
            self.home_office_area = validate_number_input(
                "Home office area in square feet (max 300): ", 0
            )
            self.business.home_office_deduction = min(self.home_office_area, 300) * 5  # $5 per sq ft
        
        # Other deductions
        has_other_deductions = validate_yes_no_input("Do you have other business deductions (y/n)? ")
        if has_other_deductions:
            self.business.other_deductions = validate_number_input(
                "Other deduction amount: $", 0
            )
        
        # Estimated tax payments
        has_estimated_tax = validate_yes_no_input("Have you made estimated tax payments (y/n)? ")
        if has_estimated_tax:
            self.business.estimated_tax_payments = validate_number_input(
                "Estimated tax payment amount: $", 0
            )

    def calculate_tax_liability(self):
        """
        Calculate tax liability based on collected information.
        
        Returns:
            dict: Dictionary containing tax calculation results
        """
        # Calculate deductions
        total_deductions, deduction_breakdown = calculate_total_deductions(
            self.business, self.filing_status
        )
        
        # Calculate taxable income
        taxable_income = calculate_taxable_income(self.business, total_deductions)
        
        # Calculate income tax
        income_tax = calculate_income_tax(self.business, taxable_income)
        
        # Calculate self-employment tax if applicable
        self_employment_tax = calculate_self_employment_tax(self.business, taxable_income)
        
        # Calculate total tax
        total_tax = income_tax + self_employment_tax
        
        # Calculate remaining tax owed
        tax_owed = max(0, total_tax - self.business.estimated_tax_payments)
        
        # Return results
        return {
            "business": self.business,
            "taxable_income": taxable_income,
            "income_tax": income_tax,
            "self_employment_tax": self_employment_tax,
            "total_tax": total_tax,
            "estimated_payments": self.business.estimated_tax_payments,
            "tax_owed": tax_owed,
            "total_deductions": total_deductions,
            "deduction_breakdown": deduction_breakdown
        }

    def display_results(self, results):
        """
        Display tax calculation results.
        
        Args:
            results (dict): Dictionary containing tax calculation results
        """
        clear_screen()
        print("=" * 70)
        print("                 TAX LIABILITY RESULTS")
        print("=" * 70)
        print(f"\nBusiness: {results['business'].name}")
        print(f"Entity Type: {results['business'].entity_type}")
        print(f"Revenue: {format_currency(results['business'].revenue)}")
        print(f"Expenses: {format_currency(results['business'].expenses)}")
        print(f"Net Income (before deductions): {format_currency(results['business'].get_net_income())}")
        print(f"Total Deductions: {format_currency(results['total_deductions'])}")
        print(f"Taxable Income: {format_currency(results['taxable_income'])}")
        print("\n" + get_deduction_breakdown(results['deduction_breakdown']))
        
        print("\nTAX BREAKDOWN")
        print(f"Income Tax: {format_currency(results['income_tax'])}")
        
        if results['self_employment_tax'] > 0:
            print(f"Self-Employment Tax: {format_currency(results['self_employment_tax'])}")
        
        print(f"Total Tax Liability: {format_currency(results['total_tax'])}")
        print(f"Estimated Tax Payments: {format_currency(results['estimated_payments'])}")
        print(f"Remaining Tax Due: {format_currency(results['tax_owed'])}")
        
        print("\n" + "=" * 70)
        print("NOTE: This is an estimate only. Consult with a tax professional")
        print("for accurate tax calculations and advice tailored to your situation.")
        print("=" * 70)