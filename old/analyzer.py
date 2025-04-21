# business_tax_calculator/analyzer.py
import pandas as pd
from typing import List, Dict

from factory import TaxCalculatorFactory
from app.utils.constants import ResultKeys, EntityType


class BusinessScenarioAnalyzer:
    def __init__(self, scenarios: List[Dict]):
        self.scenarios = scenarios

    def run_analysis(self) -> pd.DataFrame:
        dfs = []
        for s in self.scenarios:
            scenario = TaxCalculatorFactory.create_scenario(**s)
            result = scenario.calculate()
            dfs.append(result)
        df = pd.DataFrame(dfs)
        # compute differences, format money/percent columns…
        return df
