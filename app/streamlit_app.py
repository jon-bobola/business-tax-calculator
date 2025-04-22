# app/streamlit_app.py

import streamlit as st
from business_tax_calculator.calculator.tax_calculator import BusinessTaxCalculator

def main():
    st.set_page_config(page_title="Business Tax Calculator", layout="centered")
    st.title("🧾 Business Tax Calculator")

    # Wrap all inputs in a form
    with st.form("calc_form"):
        st.header("Business Details")
        entity = st.selectbox(
            "Entity Type",
            ["Sole Proprietorship", "LLC", "S-Corp", "C-Corp"],
        )
        revenue = st.number_input("Total Revenue ($)", min_value=0.0, value=100_000.0, step=1_000.0)
        expenses = st.number_input("Total Expenses ($)", min_value=0.0, value=50_000.0, step=1_000.0)

        salary = 0.0
        if entity == "S-Corp":
            salary = st.number_input(
                "S‑Corp Owner Salary ($)", min_value=0.0, value=40_000.0, step=1_000.0
            )

        retirement = st.number_input("Retirement Contributions ($)", min_value=0.0, value=0.0, step=100.0)
        health = st.number_input("Health Insurance Premiums ($)", min_value=0.0, value=0.0, step=100.0)

        # This creates a "Submit" button tied to the form
        submitted = st.form_submit_button("Calculate")

    # Only executes after the form is submitted
    if submitted:
        calc = BusinessTaxCalculator()
        calc.business.set_entity_type(entity)
        calc.business.set_revenue(revenue)
        calc.business.set_expenses(expenses)

        if entity == "S-Corp":
            calc.business.set_reasonable_salary(salary)

        calc.business.set_retirement_contributions(retirement)
        calc.business.set_health_insurance_premiums(health)

        results = calc.calculate_liabilities()

        st.subheader("Results")
        st.write(f"**Total Tax:** ${results['total_tax']:,.2f}")
        st.write(f"**Effective Rate:** {results['effective_tax_rate']:.2f}%")

        st.bar_chart({
            "Revenue": revenue,
            "Expenses": expenses,
            "Total Tax": results["total_tax"],
        })

if __name__ == "__main__":
    main()