"""
Helper functions for the Business Tax Calculator.
"""
import re

def validate_number_input(prompt, min_value=0):
    """
    Validate that the input is a valid number and greater than min_value.
    
    Args:
        prompt (str): The prompt to display to the user
        min_value (float): The minimum acceptable value
        
    Returns:
        float: The validated number input
    """
    while True:
        try:
            value = float(input(prompt))
            if value < min_value:
                print(f"Error: Value must be at least {min_value}.")
                continue
            return value
        except ValueError:
            print("Error: Please enter a valid number.")

def validate_yes_no_input(prompt):
    """
    Validate that the input is 'y' or 'n'.
    
    Args:
        prompt (str): The prompt to display to the user
        
    Returns:
        bool: True if 'y', False if 'n'
    """
    while True:
        response = input(prompt).lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Error: Please enter 'y' or 'n'.")

def format_currency(amount):
    """
    Format a number as currency.
    
    Args:
        amount (float): The amount to format
        
    Returns:
        str: The formatted currency string
    """
    return f"${amount:,.2f}"

def clear_screen():
    """Clear the console screen."""
    print("\n" * 100)

def validate_entity_type(prompt, valid_types):
    """
    Validate that the input is a valid entity type.
    
    Args:
        prompt (str): The prompt to display to the user
        valid_types (list): List of valid entity types
        
    Returns:
        str: The validated entity type
    """
    while True:
        print(prompt)
        for i, entity_type in enumerate(valid_types, 1):
            print(f"{i}. {entity_type}")
        
        try:
            choice = int(input("Enter your choice (number): "))
            if 1 <= choice <= len(valid_types):
                return valid_types[choice - 1]
            else:
                print(f"Error: Please enter a number between 1 and {len(valid_types)}.")
        except ValueError:
            print("Error: Please enter a valid number.")