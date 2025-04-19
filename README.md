# Business Tax Liability Calculator 🧾💼

A Python-based tool for comparing tax implications of Sole Proprietorship vs. S Corporation entities. Designed to help self-employed professionals (e.g., optometrists, consultants, small business owners) evaluate which structure minimizes tax liability under current U.S. tax law.

---

## 📌 Features

- Compare **Sole Proprietorship** vs **S Corporation** tax structures side-by-side
- Supports:
  - **Federal**, **State**, **Local** income tax
  - **Social Security** & **Medicare** taxes (including thresholds & caps)
  - **Qualified Business Income (QBI)** deduction
  - **Standard** and **self-employment** tax deductions
- Automatically formats and outputs a comparison table
- Extensible via OOP interfaces and dependency injection
- Easy to run from the command line or import into other tools

---

## 📁 Project Structure

```
business-tax-liability-calculator/
│
├── BusinessTaxLiabilityCalculator.py   # Main script with full logic
├── README.md                            # This file
├── requirements.txt                     # Python dependencies
└── .gitignore                           # Files to exclude from Git
```

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.7 or higher
- pip

---

### ✅ Installation

Clone the repo and set up a virtual environment:

```bash
git clone https://github.com/your-username/business-tax-liability-calculator.git
cd business-tax-liability-calculator

# Create and activate virtual environment
python -m venv venv
.env\Scriptsctivate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

---

### ▶️ Running the Calculator

To run the included scenarios and see a tax comparison table:

```bash
python BusinessTaxLiabilityCalculator.py
```

You can modify the `SCENARIOS` list at the bottom of the file to test different income, expense, and salary configurations.

---

## 🧪 Example Output

```plaintext
     Entity Type  Gross Revenue  Expenses  Net Revenue  ...  Liability % Difference
0  SoleProprietor       $100,000   $50,000     $50,000  ...               N/A
1           S Corp       $100,000   $50,000     $50,000  ...            -14.56%
```

✔️ Tax values are formatted with currency symbols and differences calculated automatically.

---

## ⚙️ Customization

Want to test different state tax brackets or entity types?

- Modify the `MarginalTaxBrackets` enum
- Add new entity classes implementing `TaxScenario`
- Swap out deduction or tax strategies via the factory pattern

---

## 🧠 Concepts Used

- Dependency Injection
- Enum-based configuration
- Abstract Base Classes (ABCs)
- Object-Oriented Design Principles
- Data formatting with Pandas

---

## 📦 Dependencies

- [`pandas`](https://pandas.pydata.org/) – Data table handling
- Standard Library: `enum`, `abc`, `dataclasses`, `logging`, `typing`

---

## 📌 Roadmap

- [ ] Export results to CSV / Excel
- [ ] Add support for Partnerships / LLCs
- [ ] Command-line input of scenarios
- [ ] Web UI or Streamlit version

---

## 🤝 Contributing

Contributions are welcome! Fork the project, create a branch, and submit a pull request.

---

## 🛡️ License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👤 Author

**Jon Bobola**  
GitHub: [@jon-bobola](https://github.com/your-username)

---

## 💬 Questions?

Open an [issue](https://github.com/your-username/business-tax-liability-calculator/issues) or shoot me a message!