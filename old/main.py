# main.py
import sys
from analyzer import BusinessScenarioAnalyzer
from viewer import TaxVisualizationViewer
from app.utils.constants import EntityType

SCENARIOS = [
    {"gross_revenue": 100_000, "expenses": 50_000, "salary": 0, "entity_type": EntityType.SOLE_PROPRIETOR.value},
    {"gross_revenue": 300_000, "expenses": 150_000, "salary": 150_000, "entity_type": EntityType.S_CORP.value},
    # …
]

def main():
    analyzer = BusinessScenarioAnalyzer(SCENARIOS)
    df = analyzer.run_analysis()
    print(df)
    if "--gui" in sys.argv:
        TaxVisualizationViewer(df).run()

if __name__ == "__main__":
    main()
