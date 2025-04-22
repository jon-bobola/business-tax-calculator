# app/streamlit_app.py

import streamlit as st
from business_tax_calculator.calculator.tax_calculator import BusinessTaxCalculator

# Constants
STATE_OPTIONS = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

COUNTY_MAPPING = {
    "MD": {"Howard County": 3.2},
}
DEFAULT_COUNTIES = ["N/A"]


def set_page_config():
    st.set_page_config(page_title="Business Tax Calculator", layout="wide")
    st.title("🧾 Business Tax Calculator")


def get_sidebar_inputs():
    with st.sidebar:
        st.markdown("## Inputs")
        inputs = {}
        # Business Information
        st.markdown("### Business Information")
        inputs["business_name"] = st.text_input("Business Name", "")
        inputs["entity"] = st.radio(
            "Business Entity Type",
            ["Sole Proprietorship", "LLC", "S-Corp", "C-Corp"],
            index=0
        )
        inputs["filing_status"] = st.radio(
            "Filing Status",
            ["Single", "Married Filing Jointly", "Head of Household"],
            index=0
        )
        # Revenue and Income
        st.markdown("### Revenue and Income")
        inputs["revenue"] = st.number_input(
            "Gross Business Revenue ($)", min_value=0.0, value=100000.0, step=1000.0
        )
        inputs["expenses"] = st.number_input(
            "Business Expenses ($)", min_value=0.0, value=50000.0, step=1000.0
        )
        if inputs["entity"] == "S-Corp":
            inputs["salary"] = st.number_input(
                "Owner Salary ($)", min_value=0.0, value=40000.0, step=1000.0
            )
        else:
            inputs["salary"] = 0.0
        # Location & Details
        st.markdown("### Location & Details")
        inputs["state"] = st.selectbox("State", STATE_OPTIONS)
        if inputs["state"] in COUNTY_MAPPING:
            counties = list(COUNTY_MAPPING[inputs["state"]].keys())
        else:
            counties = DEFAULT_COUNTIES
        inputs["county"] = st.selectbox("County", counties)
        inputs["local_rate"] = (
            COUNTY_MAPPING[inputs["state"]][inputs["county"]]
            if inputs["state"] in COUNTY_MAPPING and inputs["county"] in COUNTY_MAPPING[inputs["state"]]
            else 0.0
        )
        # Additional Details
        st.markdown("### Additional Details")
        inputs["employees"] = st.number_input("Number of Employees", min_value=1, value=1, step=1)
        inputs["retirement"] = st.number_input("Retirement Contributions ($)", min_value=0.0, value=0.0, step=100.0)
        inputs["health"] = st.number_input("Health Insurance Premiums ($)", min_value=0.0, value=0.0, step=100.0)
        inputs["home_office_sqft"] = st.number_input("Home Office (sq ft)", min_value=0.0, value=0.0, step=10.0)
        inputs["other_deductions"] = st.number_input("Other Deductions ($)", min_value=0.0, value=0.0, step=100.0)
        inputs["est_payments"] = st.number_input("Estimated Tax Payments ($)", min_value=0.0, value=0.0, step=100.0)
        inputs["calculate"] = st.button("Calculate")
    return inputs


def calculate_tax(inputs: dict):
    calc = BusinessTaxCalculator()
    # Business info
    calc.business.set_name(inputs["business_name"])
    calc.business.set_entity_type(inputs["entity"])
    calc.business.set_state(inputs["state"])
    calc.business.set_employee_count(inputs["employees"])
    calc.filing_status = inputs["filing_status"]
    # Financials
    calc.business.set_revenue(inputs["revenue"])
    calc.business.set_expenses(inputs["expenses"])
    calc.business.set_retirement_contributions(inputs["retirement"])
    calc.business.set_health_insurance_premiums(inputs["health"])
    calc.business.set_home_office_deduction(min(inputs["home_office_sqft"], 300) * 5)
    calc.business.set_other_deductions(inputs["other_deductions"])
    calc.business.set_local_tax_rate(inputs["local_rate"] / 100.0)
    calc.business.set_estimated_tax_payments(inputs["est_payments"])
    if inputs["entity"] == "S-Corp":
        calc.business.set_reasonable_salary(inputs["salary"])
    results = calc.calculate_liabilities()
    return calc, results, inputs


def display_results(calc: BusinessTaxCalculator, results: dict, inputs: dict):
    st.header("Results")
    # Business Information
    with st.expander("Business Information"):
        st.write(f"- Business Name: **{inputs['business_name']}**")
        st.write(f"- Entity Type: **{inputs['entity']}**")
        st.write(f"- Filing Status: **{inputs['filing_status']}**")
    # Revenue and Income
    net_revenue = inputs['revenue'] - inputs['expenses']
    with st.expander("Revenue and Income"):
        st.write(f"- Gross Business Revenue: **${inputs['revenue']:,.2f}**")
        st.write(f"- Business Expenses: **${inputs['expenses']:,.2f}**")
        st.write(f"- Net Business Revenue: **${net_revenue:,.2f}**")
        if inputs['entity'] == 'S-Corp':
            st.write(f"- Owner Salary: **${inputs['salary']:,.2f}**")
            profit_dist = net_revenue - inputs['salary']
            st.write(f"- Profit Distributions: **${profit_dist:,.2f}**")
        else:
            st.write("- Owner Salary: **N/A**")
            st.write(f"- Profit Distributions: **${net_revenue:,.2f}**")
    # Deductions
    total_ded = results.get('total_deductions', 0.0)
    with st.expander("Total Deductions"):
        st.write(f"Total Deductions: ${total_ded:,.2f}")
        st.write(f"- Retirement Contributions: ${inputs['retirement']:,.2f}")
        st.write(f"- Health Insurance Premiums: ${inputs['health']:,.2f}")
        home_office_ded = min(inputs['home_office_sqft'], 300) * 5
        st.write(f"- Home Office Deduction: ${home_office_ded:,.2f}")
        st.write(f"- Other Deductions: ${inputs['other_deductions']:,.2f}")
        qbi = results.get('qbi_deduction', 0.0)
        if qbi > 0:
            st.write(f"- QBI Deduction: ${qbi:,.2f}")
    # Taxes
    total_tax = results.get('total_tax', 0.0)
    st.write(f"Total Tax Due: ${total_tax:,.2f}")
    inc_tax = results.get('income_tax', 0.0)
    with st.expander(f"Income Tax Subtotal: ${inc_tax:,.2f}"):
        st.write(f"- Federal Income Tax: ${inc_tax:,.2f}")
        st.write(f"- State Income Tax: ${results.get('state_tax',0.0):,.2f}")
        st.write(f"- Local Income Tax: ${results.get('local_tax',0.0):,.2f}")
    se_tax = results.get('self_employment_tax', 0.0)
    with st.expander(f"Self-Employment Tax Subtotal: ${se_tax:,.2f}"):
        st.write(f"- Social Security: ${results.get('social_security_tax',0.0):,.2f}")
        st.write(f"- Medicare: ${results.get('medicare_tax',0.0):,.2f}")


def main():
    set_page_config()
    inputs = get_sidebar_inputs()
    if inputs.get("calculate"):
        calc, results, inputs = calculate_tax(inputs)
        display_results(calc, results, inputs)


if __name__ == "__main__":
    main()
