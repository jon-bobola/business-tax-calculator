"""
Configuration and constants for the Business Tax Calculator.
"""

# Tax rate schedules for different entity types
TAX_RATES = {
    "Sole Proprietorship": [
        (0, 11000, 0.10),
        (11001, 44725, 0.12),
        (44726, 95375, 0.22),
        (95376, 182100, 0.24),
        (182101, 231250, 0.32),
        (231251, 578125, 0.35),
        (578126, float('inf'), 0.37)
    ],
    "LLC": [  # Pass-through taxation (similar to Sole Proprietorship)
        (0, 11000, 0.10),
        (11001, 44725, 0.12),
        (44726, 95375, 0.22),
        (95376, 182100, 0.24),
        (182101, 231250, 0.32),
        (231251, 578125, 0.35),
        (578126, float('inf'), 0.37)
    ],
    "S-Corp": [  # Pass-through taxation with different employment tax considerations
        (0, 11000, 0.10),
        (11001, 44725, 0.12),
        (44726, 95375, 0.22),
        (95376, 182100, 0.24),
        (182101, 231250, 0.32),
        (231251, 578125, 0.35),
        (578126, float('inf'), 0.37)
    ],
    "C-Corp": 0.21  # Flat corporate tax rate
}

# Self-employment tax rates
SELF_EMPLOYMENT_TAX_RATE = 0.153  # 15.3% (12.4% Social Security + 2.9% Medicare)
SOCIAL_SECURITY_WAGE_BASE = 168600  # For 2024

# Standard deduction amounts
STANDARD_DEDUCTION = {
    "Single": 14600,
    "Married Filing Jointly": 29200,
    "Head of Household": 21900
}

# Retirement contribution limits
RETIREMENT_CONTRIBUTION_LIMITS = {
    "401k": 23000,
    "SEP IRA": 69000,  # 25% of compensation or $69,000, whichever is less
    "SIMPLE IRA": 16000
}

# Health insurance premium deduction rate
HEALTH_INSURANCE_DEDUCTION_RATE = 1.0  # 100% deductible for self-employed

# Home office deduction rate (per square foot)
HOME_OFFICE_DEDUCTION_RATE = 5  # $5 per square foot, up to 300 square feet