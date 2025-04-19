from enum import Enum
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any, Optional, Union, Set, TypeVar, Generic
from dataclasses import dataclass
import logging
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# Enums and Constants
class TaxRates(Enum):
    SOCIAL_SECURITY_TAX_RATE = 0.124
    MEDICARE_TAX_RATE = 0.029
    ADDITIONAL_MEDICARE_TAX_RATE = 0.009
    LOCAL_TAX_RATE = 0.032
    EMPLOYER_FICA_TAX_RATE = 0.0765
class DeductionRates(Enum):
    QUALIFIED_BUSINESS_INCOME_DEDUCTION_RATE = 0.20
    SELF_EMPLOYMENT_DEDUCTION_RATE = 0.5
class Threshold(Enum):
    SOCIAL_SECURITY_INCOME_THRESHOLD = 168600
    ADDITIONAL_MEDICARE_INCOME_THRESHOLD = 250000
class MarginalTaxBrackets(Enum):
    FEDERAL = [
        (23200, 0.10), (94300, 0.12), (201050, 0.22), (383900, 0.24),
        (487450, 0.32), (731200, 0.35), (float('inf'), 0.37)
    ]
    STATE = [
        (1000, 0.02), (2000, 0.03), (3000, 0.04), (100000, 0.0475),
        (125000, 0.05), (150000, 0.0525), (250000, 0.055), (float('inf'), 0.0575)
    ]
class EntityType(Enum):
    SOLE_PROPRIETOR = "Sole Proprietor"
    S_CORP = "S Corporation"
class ResultKeys(Enum):
    ENTITY_TYPE = "Entity Type"
    GROSS_REVENUE = "Gross Revenue"
    EXPENSES = "Expenses"
    NET_REVENUE = "Net Revenue"
    GROSS_SALARY = "Gross Salary"
    GROSS_DISTRIBUTIONS = "Gross Distributions"
    STANDARD_DEDUCTION = "Standard Deduction"
    SOCIAL_SECURITY_DEDUCTION = "Social Security Deduction"
    MEDICARE_DEDUCTION = "Medicare Deduction"
    QBI_DEDUCTION = "QBI Deduction"
    TAXABLE_PERSONAL_INCOME = "Taxable Personal Income"
    SOCIAL_SECURITY_TAX = "Social Security Tax"
    MEDICARE_TAX = "Medicare Tax"
    FEDERAL_TAX = "Federal Tax"
    STATE_TAX = "State Tax"
    LOCAL_TAX = "Local Tax"
    TOTAL_TAX = "Total Tax"
    LIABILITY_DIFFERENCE = "Liability Difference"
    LIABILITY_PERCENT_DIFFERENCE = "Liability % Difference"
# Type definitions
BracketType = List[Tuple[float, float]]
TaxResult = Dict[str, Any]
# Interfaces for Dependency Injection
class ITaxBracketCalculator(ABC):
    """Interface for tax bracket calculators"""
    @abstractmethod
    def calculate_tax(self, income: float) -> float:
        """Calculate tax based on income and defined brackets"""
        pass
class ITaxLiability(ABC):
    """Interface for tax liability calculators"""
    @abstractmethod
    def calculate(self, income: float) -> float:
        """Calculate tax liability based on income"""
        pass
    
    @property
    @abstractmethod
    def amount(self) -> float:
        """Get the calculated amount"""
        pass
class IDeduction(ABC):
    """Interface for deduction calculators"""
    @abstractmethod
    def calculate(self, base_amount: float) -> float:
        """Calculate deduction based on base amount"""
        pass
    
    @property
    @abstractmethod
    def amount(self) -> float:
        """Get the calculated amount"""
        pass
class ITaxScenario(ABC):
    """Interface for tax scenarios"""
    @abstractmethod
    def calculate(self) -> TaxResult:
        """Calculate tax scenario and return results"""
        pass
# Implementation Classes
class TaxBracket(ITaxBracketCalculator):
    """Calculate tax based on marginal tax brackets"""
    def __init__(self, brackets: BracketType):
        """
        Initialize with brackets.
        
        Args:
            brackets: List of tuples with (income_threshold, rate)
        """
        self.brackets = brackets
        self.amount = 0
    def calculate_tax(self, income: float) -> float:
        """
        Calculate tax based on marginal brackets.
        
        Args:
            income: Taxable income
            
        Returns:
            Total tax calculated
        """
        tax = 0
        prev_limit = 0
        for limit, rate in self.brackets:
            if income <= limit:
                tax += (income - prev_limit) * rate
                break
            tax += (limit - prev_limit) * rate
            prev_limit = limit
        self.amount = tax
        return tax
# Tax Liability Classes
class SocialSecurityTaxLiability(ITaxLiability):
    """Calculate Social Security tax liability"""
    def __init__(self):
        self._amount = 0
        
    def calculate(self, self_employment_income: float) -> float:
        """
        Calculate Social Security tax based on income.
        
        Args:
            self_employment_income: Self-employment or salary income
            
        Returns:
            Calculated Social Security tax
        """
        self._amount = min(self_employment_income, Threshold.SOCIAL_SECURITY_INCOME_THRESHOLD.value) * TaxRates.SOCIAL_SECURITY_TAX_RATE.value
        return self._amount
    
    @property
    def amount(self) -> float:
        return self._amount
class MedicareTaxLiability(ITaxLiability):
    """Calculate Medicare tax liability, including additional Medicare tax"""
    def __init__(self):
        self._amount = 0
        
    def calculate(self, self_employment_income: float) -> float:
        """
        Calculate Medicare tax including additional Medicare tax if applicable.
        
        Args:
            self_employment_income: Self-employment or salary income
            
        Returns:
            Total Medicare tax
        """
        medicare_tax = self_employment_income * TaxRates.MEDICARE_TAX_RATE.value
        additional_medicare_tax = max(self_employment_income - Threshold.ADDITIONAL_MEDICARE_INCOME_THRESHOLD.value, 0) * TaxRates.ADDITIONAL_MEDICARE_TAX_RATE.value
        self._amount = medicare_tax + additional_medicare_tax
        return self._amount
    
    @property
    def amount(self) -> float:
        return self._amount
class FederalIncomeTaxLiability(ITaxLiability):
    """Calculate Federal income tax liability"""
    def __init__(self, tax_bracket_calculator: ITaxBracketCalculator):
        """
        Initialize with tax bracket calculator.
        
        Args:
            tax_bracket_calculator: Calculator for federal tax brackets
        """
        self.tax_bracket_calculator = tax_bracket_calculator
        self._amount = 0
    def calculate(self, taxable_income: float) -> float:
        """
        Calculate Federal income tax.
        
        Args:
            taxable_income: Taxable income after deductions
            
        Returns:
            Federal income tax
        """
        self._amount = self.tax_bracket_calculator.calculate_tax(taxable_income)
        return self._amount
    
    @property
    def amount(self) -> float:
        return self._amount
class StateIncomeTaxLiability(ITaxLiability):
    """Calculate State income tax liability"""
    def __init__(self, tax_bracket_calculator: ITaxBracketCalculator):
        """
        Initialize with tax bracket calculator.
        
        Args:
            tax_bracket_calculator: Calculator for state tax brackets
        """
        self.tax_bracket_calculator = tax_bracket_calculator
        self._amount = 0
    def calculate(self, taxable_income: float) -> float:
        """
        Calculate State income tax.
        
        Args:
            taxable_income: Taxable income after deductions
            
        Returns:
            State income tax
        """
        self._amount = self.tax_bracket_calculator.calculate_tax(taxable_income)
        return self._amount
    
    @property
    def amount(self) -> float:
        return self._amount
class LocalTaxLiability(ITaxLiability):
    """Calculate local tax liability"""
    def __init__(self):
        self._amount = 0
        
    def calculate(self, taxable_income: float) -> float:
        """
        Calculate local tax.
        
        Args:
            taxable_income: Taxable income after deductions
            
        Returns:
            Local tax
        """
        self._amount = taxable_income * TaxRates.LOCAL_TAX_RATE.value
        return self._amount
    
    @property
    def amount(self) -> float:
        return self._amount
@dataclass
class TaxLiabilityDependencies:
    """Dependencies for TaxLiability class"""
    social_security_tax: ITaxLiability
    medicare_tax: ITaxLiability
    federal_income_tax: ITaxLiability
    state_income_tax: ITaxLiability
    local_tax: ITaxLiability
class TaxLiability:
    """Aggregate tax liability calculator"""
    def __init__(self, dependencies: TaxLiabilityDependencies):
        """
        Initialize with tax liability calculators.
        
        Args:
            dependencies: Various tax liability calculators
        """
        self.social_security_tax_liability = dependencies.social_security_tax
        self.medicare_tax_liability = dependencies.medicare_tax
        self.federal_income_tax_liability = dependencies.federal_income_tax
        self.state_income_tax_liability = dependencies.state_income_tax
        self.local_tax_liability = dependencies.local_tax
        self.total_amount = 0
    def calculate_total_tax(self, self_employment_income: float, taxable_income: float) -> float:
        """
        Calculate total tax liability.
        
        Args:
            self_employment_income: Income subject to self-employment taxes
            taxable_income: Income subject to income taxes
            
        Returns:
            Total tax liability
        """
        self.social_security_tax_liability.calculate(self_employment_income)
        self.medicare_tax_liability.calculate(self_employment_income)
        self.federal_income_tax_liability.calculate(taxable_income)
        self.state_income_tax_liability.calculate(taxable_income)
        self.local_tax_liability.calculate(taxable_income)
        
        self.total_amount = (
            self.social_security_tax_liability.amount +
            self.medicare_tax_liability.amount +
            self.federal_income_tax_liability.amount +
            self.state_income_tax_liability.amount +
            self.local_tax_liability.amount
        )
        return self.total_amount
# Deduction Classes
class StandardDeduction(IDeduction):
    """Standard deduction calculator"""
    STANDARD_DEDUCTION_AMOUNT = 29200
    
    def __init__(self):
        self._amount = 0
    def calculate(self, base_amount: float = None) -> float:
        """
        Calculate standard deduction.
        
        Args:
            base_amount: Not used for standard deduction
            
        Returns:
            Standard deduction amount
        """
        self._amount = self.STANDARD_DEDUCTION_AMOUNT
        return self._amount
    
    @property
    def amount(self) -> float:
        return self._amount
class SocialSecurityDeduction(IDeduction):
    """Social Security tax deduction calculator"""
    def __init__(self):
        self._amount = 0
        
    def calculate(self, social_security_tax: float) -> float:
        """
        Calculate Social Security tax deduction.
        
        Args:
            social_security_tax: Social Security tax paid
            
        Returns:
            Deductible portion
        """
        self._amount = social_security_tax * DeductionRates.SELF_EMPLOYMENT_DEDUCTION_RATE.value
        return self._amount
    
    @property
    def amount(self) -> float:
        return self._amount
class MedicareDeduction(IDeduction):
    """Medicare tax deduction calculator"""
    def __init__(self):
        self._amount = 0
        
    def calculate(self, medicare_tax: float) -> float:
        """
        Calculate Medicare tax deduction.
        
        Args:
            medicare_tax: Medicare tax paid
            
        Returns:
            Deductible portion
        """
        self._amount = medicare_tax * DeductionRates.SELF_EMPLOYMENT_DEDUCTION_RATE.value
        return self._amount
    
    @property
    def amount(self) -> float:
        return self._amount
class QualifiedBusinessIncomeDeduction(IDeduction):
    """Qualified Business Income deduction calculator"""
    def __init__(self):
        self._amount = 0
        
    def calculate(self, qualified_business_income_base: float) -> float:
        """
        Calculate QBI deduction.
        
        Args:
            qualified_business_income_base: QBI base amount
            
        Returns:
            QBI deduction
        """
        self._amount = qualified_business_income_base * DeductionRates.QUALIFIED_BUSINESS_INCOME_DEDUCTION_RATE.value
        return self._amount
    
    @property
    def amount(self) -> float:
        return self._amount
@dataclass
class TaxDeductionDependencies:
    """Dependencies for TaxDeduction class"""
    standard_deduction: IDeduction
    social_security_deduction: IDeduction
    medicare_deduction: IDeduction
    qualified_business_income_deduction: IDeduction
class TaxDeduction:
    """Aggregate tax deduction calculator"""
    def __init__(self, dependencies: TaxDeductionDependencies):
        """
        Initialize with deduction calculators.
        
        Args:
            dependencies: Various deduction calculators
        """
        self.standard_deduction = dependencies.standard_deduction
        self.social_security_deduction = dependencies.social_security_deduction
        self.medicare_deduction = dependencies.medicare_deduction
        self.qualified_business_income_deduction = dependencies.qualified_business_income_deduction
        self.total_amount = 0
    def calculate_total_deductions(self, social_security_tax: float, medicare_tax: float, qualified_business_income_base: float) -> float:
        """
        Calculate total deductions.
        
        Args:
            social_security_tax: Social Security tax paid
            medicare_tax: Medicare tax paid
            qualified_business_income_base: QBI base amount
            
        Returns:
            Total deductions
        """
        self.standard_deduction.calculate()
        self.social_security_deduction.calculate(social_security_tax)
        self.medicare_deduction.calculate(medicare_tax)
        self.qualified_business_income_deduction.calculate(qualified_business_income_base)
        
        self.total_amount = (
            self.standard_deduction.amount +
            self.social_security_deduction.amount +
            self.medicare_deduction.amount +
            self.qualified_business_income_deduction.amount
        )
        return self.total_amount
# Base Tax Scenario
class TaxScenario(ITaxScenario):
    """Base tax scenario class"""
    def __init__(self, 
                 gross_revenue: float, 
                 expenses: float, 
                 salary: float, 
                 entity_type: str,
                 tax_deduction: TaxDeduction,
                 tax_liability: TaxLiability):
        """
        Initialize tax scenario.
        
        Args:
            gross_revenue: Total revenue
            expenses: Business expenses
            salary: Salary paid
            entity_type: Type of business entity
            tax_deduction: Tax deduction calculator
            tax_liability: Tax liability calculator
        """
        self.gross_revenue = gross_revenue
        self.expenses = expenses
        self.salary = salary
        self.entity_type = entity_type
        self.net_revenue = self.gross_revenue - self.expenses
        self.distributions = self.net_revenue - self.salary
        self.tax_deductions = tax_deduction
        self.tax_liability = tax_liability
        self.taxable_income = 0
        self.validate_inputs()
        
    def validate_inputs(self):
        """Validate input values"""
        if self.gross_revenue < 0:
            raise ValueError("Gross revenue cannot be negative")
        if self.expenses < 0:
            raise ValueError("Expenses cannot be negative")
        if self.salary < 0:
            raise ValueError("Salary cannot be negative")
        if self.expenses > self.gross_revenue:
            logger.warning("Expenses exceed gross revenue, resulting in negative net revenue")
    def calculate_taxable_income(self, social_security_tax: float, medicare_tax: float, qualified_business_income_base: float) -> float:
        """
        Calculate taxable income after deductions.
        
        Args:
            social_security_tax: Social Security tax paid
            medicare_tax: Medicare tax paid
            qualified_business_income_base: QBI base amount
            
        Returns:
            Taxable income
        """
        total_deductions = self.tax_deductions.calculate_total_deductions(social_security_tax, medicare_tax, qualified_business_income_base)
        self.taxable_income = max(self.net_revenue - total_deductions, 0)
        return self.taxable_income
    def calculate_taxes(self, self_employment_income: float, taxable_income: float) -> float:
        """
        Calculate total taxes.
        
        Args:
            self_employment_income: Income subject to self-employment taxes
            taxable_income: Income subject to income taxes
            
        Returns:
            Total tax
        """
        return self.tax_liability.calculate_total_tax(self_employment_income, taxable_income)
        
    @abstractmethod
    def calculate(self) -> TaxResult:
        """Calculate tax scenario and return results"""
        pass
class SoleProprietorTaxScenario(TaxScenario):
    """Tax scenario for Sole Proprietor entities"""
    SELF_EMPLOYMENT_INCOME_ADJUSTMENT_FACTOR = 1 - TaxRates.EMPLOYER_FICA_TAX_RATE.value
    
    def __init__(self, 
                 gross_revenue: float, 
                 expenses: float, 
                 salary: float,
                 tax_deduction: TaxDeduction,
                 tax_liability: TaxLiability):
        """
        Initialize Sole Proprietor tax scenario.
        
        Args:
            gross_revenue: Total revenue
            expenses: Business expenses
            salary: Usually 0 for sole proprietors
            tax_deduction: Tax deduction calculator
            tax_liability: Tax liability calculator
        """
        super().__init__(gross_revenue, expenses, salary, EntityType.SOLE_PROPRIETOR.value, tax_deduction, tax_liability)
        self.self_employment_income = 0
        self.qualified_business_income_base = 0
    def get_self_employment_income(self) -> float:
        """
        Calculate self-employment income.
        
        Returns:
            Self-employment income
        """
        self.self_employment_income = self.net_revenue * self.SELF_EMPLOYMENT_INCOME_ADJUSTMENT_FACTOR
        return self.self_employment_income
    def get_qualified_business_income_base(self, social_security_tax: float, medicare_tax: float) -> float:
        """
        Calculate QBI base amount.
        
        Args:
            social_security_tax: Social Security tax paid
            medicare_tax: Medicare tax paid
            
        Returns:
            QBI base amount
        """
        self_employment_tax = social_security_tax + medicare_tax
        self.qualified_business_income_base = max(self.net_revenue - self_employment_tax * DeductionRates.SELF_EMPLOYMENT_DEDUCTION_RATE.value, 0)
        return self.qualified_business_income_base
    def calculate(self) -> TaxResult:
        """
        Calculate tax scenario for Sole Proprietor.
        
        Returns:
            Dictionary with tax calculation results
        """
        self.get_self_employment_income()
        
        social_security_tax = self.tax_liability.social_security_tax_liability.calculate(self.self_employment_income)
        medicare_tax = self.tax_liability.medicare_tax_liability.calculate(self.self_employment_income)
        
        self.get_qualified_business_income_base(social_security_tax, medicare_tax)
        
        self.calculate_taxable_income(social_security_tax, medicare_tax, self.qualified_business_income_base)
        total_tax = self.calculate_taxes(self.self_employment_income, self.taxable_income)
        
        return {
            ResultKeys.ENTITY_TYPE.value: self.entity_type,
            ResultKeys.GROSS_REVENUE.value: self.gross_revenue,
            ResultKeys.EXPENSES.value: self.expenses,
            ResultKeys.NET_REVENUE.value: self.net_revenue,
            ResultKeys.GROSS_SALARY.value: self.salary,
            ResultKeys.GROSS_DISTRIBUTIONS.value: self.distributions,
            ResultKeys.STANDARD_DEDUCTION.value: self.tax_deductions.standard_deduction.amount,
            ResultKeys.SOCIAL_SECURITY_DEDUCTION.value: self.tax_deductions.social_security_deduction.amount,
            ResultKeys.MEDICARE_DEDUCTION.value: self.tax_deductions.medicare_deduction.amount,
            ResultKeys.QBI_DEDUCTION.value: self.tax_deductions.qualified_business_income_deduction.amount,
            ResultKeys.TAXABLE_PERSONAL_INCOME.value: self.taxable_income,
            ResultKeys.SOCIAL_SECURITY_TAX.value: self.tax_liability.social_security_tax_liability.amount,
            ResultKeys.MEDICARE_TAX.value: self.tax_liability.medicare_tax_liability.amount,
            ResultKeys.FEDERAL_TAX.value: self.tax_liability.federal_income_tax_liability.amount,
            ResultKeys.STATE_TAX.value: self.tax_liability.state_income_tax_liability.amount,
            ResultKeys.LOCAL_TAX.value: self.tax_liability.local_tax_liability.amount,
            ResultKeys.TOTAL_TAX.value: self.tax_liability.total_amount
        }
class SCorpTaxScenario(TaxScenario):
    """Tax scenario for S Corporation entities"""
    def __init__(self, 
                 gross_revenue: float, 
                 expenses: float, 
                 salary: float,
                 tax_deduction: TaxDeduction,
                 tax_liability: TaxLiability):
        """
        Initialize S Corp tax scenario.
        
        Args:
            gross_revenue: Total revenue
            expenses: Business expenses
            salary: Salary paid to owner/employee
            tax_deduction: Tax deduction calculator
            tax_liability: Tax liability calculator
        """
        super().__init__(gross_revenue, expenses, salary, EntityType.S_CORP.value, tax_deduction, tax_liability)
        self.self_employment_income = 0
        self.qualified_business_income_base = 0
        self.validate_scorp_salary()
        
    def validate_scorp_salary(self):
        """Validate S Corp specific requirements"""
        if self.salary <= 0 and self.net_revenue > 0:
            logger.warning("S Corp has positive net revenue but no salary. This might trigger IRS scrutiny.")
        if self.salary > self.net_revenue:
            logger.warning("S Corp salary exceeds net revenue. This might not be sustainable.")
    def get_self_employment_income(self) -> float:
        """
        Get self-employment income (salary for S Corps).
        
        Returns:
            Self-employment income
        """
        self.self_employment_income = self.salary
        return self.self_employment_income
    def get_qualified_business_income_base(self) -> float:
        """
        Get QBI base amount (distributions for S Corps).
        
        Returns:
            QBI base amount
        """
        self.qualified_business_income_base = self.distributions
        return self.qualified_business_income_base
    def calculate(self) -> TaxResult:
        """
        Calculate tax scenario for S Corp.
        
        Returns:
            Dictionary with tax calculation results
        """
        self.get_self_employment_income()
        
        social_security_tax = self.tax_liability.social_security_tax_liability.calculate(self.self_employment_income)
        medicare_tax = self.tax_liability.medicare_tax_liability.calculate(self.self_employment_income)
        
        qualified_business_income_base = self.get_qualified_business_income_base()
        
        self.calculate_taxable_income(social_security_tax, medicare_tax, qualified_business_income_base)
        total_tax = self.calculate_taxes(self.self_employment_income, self.taxable_income)
        
        return {
            ResultKeys.ENTITY_TYPE.value: self.entity_type,
            ResultKeys.GROSS_REVENUE.value: self.gross_revenue,
            ResultKeys.EXPENSES.value: self.expenses,
            ResultKeys.NET_REVENUE.value: self.net_revenue,
            ResultKeys.GROSS_SALARY.value: self.salary,
            ResultKeys.GROSS_DISTRIBUTIONS.value: self.distributions,
            ResultKeys.STANDARD_DEDUCTION.value: self.tax_deductions.standard_deduction.amount,
            ResultKeys.SOCIAL_SECURITY_DEDUCTION.value: self.tax_deductions.social_security_deduction.amount,
            ResultKeys.MEDICARE_DEDUCTION.value: self.tax_deductions.medicare_deduction.amount,
            ResultKeys.QBI_DEDUCTION.value: self.tax_deductions.qualified_business_income_deduction.amount,
            ResultKeys.TAXABLE_PERSONAL_INCOME.value: self.taxable_income,
            ResultKeys.SOCIAL_SECURITY_TAX.value: self.tax_liability.social_security_tax_liability.amount,
            ResultKeys.MEDICARE_TAX.value: self.tax_liability.medicare_tax_liability.amount,
            ResultKeys.FEDERAL_TAX.value: self.tax_liability.federal_income_tax_liability.amount,
            ResultKeys.STATE_TAX.value: self.tax_liability.state_income_tax_liability.amount,
            ResultKeys.LOCAL_TAX.value: self.tax_liability.local_tax_liability.amount,
            ResultKeys.TOTAL_TAX.value: self.tax_liability.total_amount
        }
# Tax Calculator Factory
class TaxCalculatorFactory:
    """Factory for creating tax calculators and dependencies"""
    @staticmethod
    def create_tax_liability() -> TaxLiability:
        """Create tax liability calculator with dependencies"""
        federal_bracket_calculator = TaxBracket(MarginalTaxBrackets.FEDERAL.value)
        state_bracket_calculator = TaxBracket(MarginalTaxBrackets.STATE.value)
        
        dependencies = TaxLiabilityDependencies(
            social_security_tax=SocialSecurityTaxLiability(),
            medicare_tax=MedicareTaxLiability(),
            federal_income_tax=FederalIncomeTaxLiability(federal_bracket_calculator),
            state_income_tax=StateIncomeTaxLiability(state_bracket_calculator),
            local_tax=LocalTaxLiability()
        )
        
        return TaxLiability(dependencies)
    
    @staticmethod
    def create_tax_deduction() -> TaxDeduction:
        """Create tax deduction calculator with dependencies"""
        dependencies = TaxDeductionDependencies(
            standard_deduction=StandardDeduction(),
            social_security_deduction=SocialSecurityDeduction(),
            medicare_deduction=MedicareDeduction(),
            qualified_business_income_deduction=QualifiedBusinessIncomeDeduction()
        )
        
        return TaxDeduction(dependencies)
    
    @staticmethod
    def create_scenario(gross_revenue: float, expenses: float, salary: float, entity_type: str) -> ITaxScenario:
        """
        Create appropriate tax scenario based on entity type.
        
        Args:
            gross_revenue: Total revenue
            expenses: Business expenses
            salary: Salary paid
            entity_type: Type of business entity
            
        Returns:
            Configured tax scenario
        """
        tax_deduction = TaxCalculatorFactory.create_tax_deduction()
        tax_liability = TaxCalculatorFactory.create_tax_liability()
        
        if entity_type == EntityType.SOLE_PROPRIETOR.value:
            return SoleProprietorTaxScenario(gross_revenue, expenses, salary, tax_deduction, tax_liability)
        elif entity_type == EntityType.S_CORP.value:
            return SCorpTaxScenario(gross_revenue, expenses, salary, tax_deduction, tax_liability)
        else:
            raise ValueError(f"Unknown entity type: {entity_type}")
# Business Scenario Analyzer
class BusinessScenarioAnalyzer:

    def _format_dataframe(self):
        """Format DataFrame for display."""
        # work on a copy so we don’t lose the raw numeric DataFrame
        df = self.df.copy()

        # 1) Define column order
        COLUMNS = [
            ResultKeys.ENTITY_TYPE.value, ResultKeys.GROSS_REVENUE.value, ResultKeys.EXPENSES.value,
            ResultKeys.NET_REVENUE.value, ResultKeys.GROSS_SALARY.value, ResultKeys.GROSS_DISTRIBUTIONS.value,
            ResultKeys.STANDARD_DEDUCTION.value, ResultKeys.SOCIAL_SECURITY_DEDUCTION.value,
            ResultKeys.MEDICARE_DEDUCTION.value, ResultKeys.QBI_DEDUCTION.value,
            ResultKeys.TAXABLE_PERSONAL_INCOME.value, ResultKeys.SOCIAL_SECURITY_TAX.value,
            ResultKeys.MEDICARE_TAX.value, ResultKeys.FEDERAL_TAX.value, ResultKeys.STATE_TAX.value,
            ResultKeys.LOCAL_TAX.value, ResultKeys.TOTAL_TAX.value,
            ResultKeys.LIABILITY_DIFFERENCE.value, ResultKeys.LIABILITY_PERCENT_DIFFERENCE.value
        ]

        # 2) Format money columns
        money_cols = [
            c for c in df.columns
            if any(keyword in c for keyword in ("Revenue","Expenses","Salary","Distributions","Deduction","Tax","Difference"))
            and c != ResultKeys.LIABILITY_PERCENT_DIFFERENCE.value
        ]
        for col in money_cols:
            df[col] = df[col].map(lambda x: f"${x:,.2f}" if pd.notna(x) else "N/A")

        # 3) Format the % column
        pct_col = ResultKeys.LIABILITY_PERCENT_DIFFERENCE.value
        df[pct_col] = df[pct_col].map(lambda x: f"{x:,.2f}%" if pd.notna(x) else "N/A")

        # 4) Reorder and store back on self
        df = df[COLUMNS]
        self.df = df
        return df

    """Analyzes tax implications of different business scenarios"""
    def __init__(self, scenarios: List[Dict[str, Any]]):
        """
        Initialize analyzer with scenarios.
        
        Args:
            scenarios: List of scenario configurations
        """
        self.scenarios = scenarios
        self.results = None
        self.df = None
        
    def run_analysis(self) -> pd.DataFrame:
        """
        Run tax analysis on all scenarios.
        
        Returns:
            DataFrame with analysis results
        """
        try:
            # Create scenarios
            tax_scenarios = [TaxCalculatorFactory.create_scenario(**data) for data in self.scenarios]
            
            # Calculate results
            self.results = [scenario.calculate() for scenario in tax_scenarios]
            self.df = pd.DataFrame(self.results)
            
            # Calculate differences
            self._calculate_tax_differences()
            
            # Sort on the numeric Net Revenue column
            self.df = self.df.sort_values(
            by=ResultKeys.NET_REVENUE.value,
            ascending=True
            ).reset_index(drop=True)
            
            # Format DataFrame
            self._format_dataframe()
            
            return self.df
        except Exception as e:
            logger.error(f"Error running analysis: {e}")
            raise
    
    def _calculate_tax_differences(self):
        """Calculate tax liability differences between entity types"""
        def calculate_difference(row):
            opposite_type = EntityType.S_CORP.value if row[ResultKeys.ENTITY_TYPE.value] == EntityType.SOLE_PROPRIETOR.value else EntityType.SOLE_PROPRIETOR.value
            match = self.df[(self.df[ResultKeys.NET_REVENUE.value] == row[ResultKeys.NET_REVENUE.value]) & 
                           (self.df[ResultKeys.ENTITY_TYPE.value] == opposite_type)]
            if not match.empty:
                match_total = match.iloc[0][ResultKeys.TOTAL_TAX.value]
                difference = row[ResultKeys.TOTAL_TAX.value] - match_total
                percent_difference = (difference / match_total) * 100 if match_total != 0 else 0
                return pd.Series([difference, percent_difference])
            return pd.Series([None, None])
        self.df[[ResultKeys.LIABILITY_DIFFERENCE.value, ResultKeys.LIABILITY_PERCENT_DIFFERENCE.value]] = self.df.apply(calculate_difference, axis=1)
    
# For direct execution
if __name__ == "__main__":
    import sys

    if "--test" in sys.argv:
        print("✅ Script ran in test mode.")
    else:
        SCENARIOS = [
        # Full run
        
        # Scenarios
        SCENARIOS = [
        {"gross_revenue": 100000, "expenses": 50000, "salary": 0, "entity_type": EntityType.SOLE_PROPRIETOR.value},
        {"gross_revenue": 200000, "expenses": 100000, "salary": 0, "entity_type": EntityType.SOLE_PROPRIETOR.value},
        {"gross_revenue": 300000, "expenses": 150000, "salary": 0, "entity_type": EntityType.SOLE_PROPRIETOR.value},
        {"gross_revenue": 400000, "expenses": 200000, "salary": 0, "entity_type": EntityType.SOLE_PROPRIETOR.value},
        {"gross_revenue": 500000, "expenses": 250000, "salary": 0, "entity_type": EntityType.SOLE_PROPRIETOR.value},
        {"gross_revenue": 300000, "expenses": 150000, "salary": 150000, "entity_type": EntityType.S_CORP.value},
        {"gross_revenue": 400000, "expenses": 200000, "salary": 150000, "entity_type": EntityType.S_CORP.value},
        {"gross_revenue": 500000, "expenses": 250000, "salary": 150000, "entity_type": EntityType.S_CORP.value},
    ]
        
        analyzer = BusinessScenarioAnalyzer(SCENARIOS)
        df = analyzer.run_analysis()
        print(df)