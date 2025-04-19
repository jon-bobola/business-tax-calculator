#!/usr/bin/env python3
"""
Main entry point for the Business Tax Liability Calculator application.
"""
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from calculator.tax_calculator import BusinessTaxCalculator

def main():
    """Main function to run the Business Tax Calculator application."""
    calculator = BusinessTaxCalculator()
    calculator.run()

if __name__ == "__main__":
    main()