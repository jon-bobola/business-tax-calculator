from app.model.business import Business

from deduction_calculator import (
    calculate_total_deductions,
    calculate_qbi_deduction,
    get_deduction_breakdown,
)

from calculator.income_calculator import (
    calculate_taxable_income,
    calculate_self_employment_tax,
    calculate_effective_tax_rate,
)

from utils.helpers import (
    validate_number_input,
    validate_yes_no_input,
    validate_entity_type,
    format_currency,
    clear_screen,
)


class BusinessTaxCalculator:
    """
    Main calculator class that handles the tax calculation workflow.
    """

    def __init__(self):
        self.business = Business()
        self.valid_entity_types = [
            "Sole Proprietorship",
            "LLC",
            "S-Corp",
            "C-Corp",
        ]
        self.filing_status = "Single"
        self.has_home_office = False
        self.home_office_area = 0

    def run(self):
        """Run the tax calculator application."""
        try:
            self.display_welcome()
            self.collect_business_info()
            self.collect_income_info()
            self.collect_deduction_info()
            results = self.calculate_liabilities()
            self.display_results(results)
        except KeyboardInterrupt:
            print("\n\nCalculation cancelled. Exiting program.")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again or contact support.")

    def display_welcome(self):
        """Display welcome message."""
        clear_screen()
        print("=" * 70)
        print(" BUSINESS TAX LIABILITY CALCULATOR")
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
        self.business.set_entity_type(validate_entity_type(
            "Select business entity type:", self.valid_entity_types
        ))
        self.business.set_state(input("State (for state tax estimation): "))

        if self.business.entity_type == "S-Corp":
            print("\nS-Corporation owners must pay themselves a reasonable salary.")
            print("This salary is subject to employment taxes (Social Security and Medicare).")
            self.business.set_reasonable_salary(validate_number_input(
                "Enter reasonable salary for S-Corp owner: $", 0
            ))

        if self.business.entity_type in ["Sole Proprietorship", "LLC", "S-Corp"]:
            self.collect_filing_status()

        self.business.set_employee_count(int(
            validate_number_input("Number of employees (including yourself): ", 1)
        ))

    def collect_filing_status(self):
        """Collect tax filing status for pass-through entities."""
        valid_statuses = [
            "Single",
            "Married Filing Jointly",
            "Head of Household",
        ]
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

        self.business.set_revenue(validate_number_input("Total business revenue: $", 0))
        self.business.set_expenses(validate_number_input("Total business expenses: $", 0))

        net_income = self.business.get_net_income()
        print(f"\nNet income before deductions: {format_currency(net_income)}")
        if net_income < 0:
            print(
                "\nNOTE: Your business is showing a loss. Tax calculations will be based on $0 taxable income."
            )
            print(
                " Consult a tax professional for advice on handling business losses."
            )
            input("\nPress Enter to continue...")

    def collect_deduction_info(self):
        """Collect deduction information."""
        clear_screen()
        print("DEDUCTION INFORMATION\n")

        has_retirement = validate_yes_no_input(
            "Do you have retirement contributions (y/n)? "
        )
        if has_retirement:
            self.business.set_retirement_contributions(validate_number_input(
                "Retirement contribution amount: $", 0
            ))

        has_health = validate_yes_no_input(
            "Do you have health insurance premiums (y/n)? "
        )
        if has_health:
            self.business.set_health_insurance_premiums(validate_number_input(
                "Health insurance premium amount: $", 0
            ))

        self.has_home_office = validate_yes_no_input(
            "Do you claim a home office deduction (y/n)? "
        )
        if self.has_home_office:
            self.home_office_area = validate_number_input(
                "Home office area in square feet (max 300): ", 0
            )
            self.business.set_home_office_deduction(min(self.home_office_area, 300) * 5)

        has_other = validate_yes_no_input(
            "Do you have other business deductions (y/n)? "
        )
        if has_other:
            self.business.set_other_deductions(validate_number_input(
                "Other deduction amount: $", 0
            ))

        custom_local = validate_yes_no_input(
            "Do you want to specify a custom local tax rate (y/n)? "
        )
        if custom_local:
            rate_pct = validate_number_input("Local tax rate percentage: ", 0)
            self.business.set_local_tax_rate(rate_pct / 100)

        has_est = validate_yes_no_input(
            "Have you made estimated tax payments (y/n)? "
        )
        if has_est:
            self.business.set_estimated_tax_payments(validate_number_input(
                "Estimated tax payment amount: $", 0
            ))

    def calculate_liabilities(self):



        """Calculate tax liability based on collected information."""
        # 1. Preliminary SE tax for deduction
        prelim_se_tax, ss_tax, med_tax = calculate_self_employment_tax(
            self.business, self.business.get_net_income()
        )
        # 2. Total deductions
        total_deductions, deduction_breakdown = calculate_total_deductions(
            self.business, self.filing_status, prelim_se_tax
        )
        # 3. Taxable income before QBI
        prelim_taxable = calculate_taxable_income(
            self.business, total_deductions
        )
        # 4. QBI deduction
        qbi_deduction = calculate_qbi_deduction(
            self.business, prelim_taxable, self.filing_status
        )
        # 5. Final taxable income
        taxable_income = calculate_taxable_income(
            self.business, total_deductions, qbi_deduction
        )

        tax_liability = self.business.tax_return.tax_liability

        # 6. Federal income tax
        # 7. Final SE tax
        # 8. State income tax
        # 9. Local income tax
        tax_liability.calculate(self.business.filing_status, taxable_income)

        # 10. Total tax liability
        total_tax = tax_liability.value
        
        # 11. Remaining tax owed
        tax_owed = max(0, total_tax - getattr(self.business, 'estimated_tax_payments', 0))
        # 12. Effective tax rate
        effective_rate = calculate_effective_tax_rate(
            total_tax, self.business.get_net_income()
        )
        # Profit distributions
        profit_dist = self.business.get_profit_distributions()

        return {
            'business': self.business,
            'taxable_income': taxable_income,
            'income_tax': tax_liability.income_tax,
            'self_employment_tax': tax_liability.self_employment_tax,
            'social_security_tax': tax_liability.social_security_tax_liability,
            'medicare_tax': tax_liability.medicare_tax_liability,
            'state_tax': tax_liability.state_income_tax_liability,
            'local_tax': tax_liability.local_income_tax_liability,
            'total_tax': total_tax,
            'estimated_payments': getattr(self.business, 'estimated_tax_payments', 0),
            'tax_owed': tax_owed,
            'total_deductions': total_deductions,
            'deduction_breakdown': deduction_breakdown,
            'qbi_deduction': qbi_deduction,
            'profit_distributions': profit_dist,
            'effective_tax_rate': effective_rate,
        }

    def display_results(self, results):
        """Display tax calculation results."""
        clear_screen()
        print("=" * 70)
        print(" TAX LIABILITY RESULTS")
        print("=" * 70)
        print(f"\nBusiness: {results['business'].name}")
        print(f"Entity Type: {results['business'].entity_type}")
        print(f"Revenue: {format_currency(results['business'].revenue)}")
        print(f"Expenses: {format_currency(results['business'].expenses)}")
        print(f"Net Income (before deductions): {format_currency(results['business'].get_net_income())}")

        if results['business'].entity_type == "S-Corp":
            print(f"Owner's Salary: {format_currency(results['business'].reasonable_salary)}")
            print(f"Profit Distributions: {format_currency(results['profit_distributions'])}")

        print(f"\nTotal Deductions: {format_currency(results['total_deductions'])}")
        if results['qbi_deduction'] > 0:
            print(f"Qualified Business Income Deduction: {format_currency(results['qbi_deduction'])}")
        print(f"Taxable Income: {format_currency(results['taxable_income'])}")

        print("\n" + get_deduction_breakdown(results['deduction_breakdown']))

        print("\nTAX BREAKDOWN")
        print(f"Federal Income Tax: {format_currency(results['income_tax'])}")

        if results['self_employment_tax'] > 0 or results['business'].entity_type == "S-Corp":
            label = "Self-Employment Tax" if results['business'].entity_type in ["Sole Proprietorship", "LLC"] else "Employment Taxes"
            print(f"{label}: {format_currency(results['self_employment_tax'])}")
            print(f" - Social Security Tax: {format_currency(results['social_security_tax'])}")
            print(f" - Medicare Tax: {format_currency(results['medicare_tax'])}")

        if results['state_tax'] > 0:
            print(f"Estimated State Income Tax: {format_currency(results['state_tax'])}")
        if results['local_tax'] > 0:
            print(f"Estimated Local Income Tax: {format_currency(results['local_tax'])}")

        print(f"\nTotal Tax Liability: {format_currency(results['total_tax'])}")
        print(f"Estimated Tax Payments: {format_currency(results['estimated_payments'])}")
        print(f"Remaining Tax Due: {format_currency(results['tax_owed'])}")

        print(f"\nEffective Tax Rate: {results['effective_tax_rate']:.2f}%")
        print("\n" + "=" * 70)
        print("NOTE: This is an estimate only. Consult with a tax professional")
        print("for accurate tax calculations and advice tailored to your situation.")
        print("=" * 70)
