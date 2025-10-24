import random
import datetime
from typing import List
import requests
import pandas as pd

from models import Employee, Department

class DataGenerator:
    def __init__(self, use_api: bool = True):
        self.use_api = use_api
        self.departments = list(Department)
        self.start_date = datetime.date(2020, 1, 1)
        self.end_date = datetime.date.today()
        self.days_range = (self.end_date - self.start_date).days

    def _fetch_names_from_api(self, n: int) -> List[str]:
        if not self.use_api:
            return []
        try:
            resp = requests.get(f"https://randomuser.me/api/?results={n}&nat=us", timeout=10)
            resp.raise_for_status()
            data = resp.json()
            names: List[str] = []
            for item in data.get("results", []):
                name = item.get("name", {})
                first = name.get("first", "").title()
                last = name.get("last", "").title()
                if first and last:
                    names.append(f"{first} {last}")
            return names
        except Exception:
            return []

    def generate(self, n: int) -> pd.DataFrame:
        names = self._fetch_names_from_api(n)

        employees = []
        for i in range(1, n + 1):
            full_name = names[i - 1]
            dept = random.choice(self.departments).value
            salary = random.randint(25000, 120000)
            hire_delta = datetime.timedelta(days=random.randint(0, self.days_range))
            hire_date = self.start_date + hire_delta
            emp = Employee(
                emp_id=i,
                full_name=full_name,
                department=dept,
                salary=salary,
                hire_date=hire_date.isoformat()
            )
            employees.append(emp)
        df = pd.DataFrame([e.to_dict() for e in employees])
        return df
