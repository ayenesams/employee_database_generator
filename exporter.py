import os
import importlib.util
import pandas as pd

class ExcelExporter:
    def __init__(self, filename: str = "employees.xlsx"):
        self.filename = filename

    def export(self, df: pd.DataFrame, folder: str) -> str:
        filepath = os.path.join(folder, self.filename)

        engines = []
        if importlib.util.find_spec("openpyxl"):
            engines.append("openpyxl")

        if not engines:
            raise RuntimeError(
                "No Excel writer engine found. Install openpyxl with:\n"
                "    pip install openpyxl"
            )

        engine = engines[0]
        with pd.ExcelWriter(filepath, engine=engine) as writer:
            df.to_excel(writer, sheet_name="Employees", index=False)
        return filepath

