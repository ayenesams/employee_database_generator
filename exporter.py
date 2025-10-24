import os
import datetime
import importlib.util
import pandas as pd

class ExcelExporter:
    def __init__(self, filename: str = "employees.xlsx"):
        self.filename = filename

    def export(self, df: pd.DataFrame, folder: str) -> str:
        filepath = os.path.join(folder, self.filename)
        summary_df = df.groupby("department", as_index=False)["salary"].mean()
        summary_df["salary"] = summary_df["salary"].round(2)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
            summary_df.to_excel(writer, sheet_name="Summary", index=False, startrow=0)
            worksheet = writer.sheets["Summary"]
            ts_row = len(summary_df) + 3
            if engine == "openpyxl":
                # openpyxl uses 1-based row/col and .cell(...)
                worksheet.cell(row=ts_row, column=1, value=f"Exported: {timestamp}")
            else:
                # xlsxwriter uses 0-based row index for .write
                worksheet.write(ts_row - 1, 0, f"Exported: {timestamp}")
        return filepath

