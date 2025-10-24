from dataclasses import dataclass, asdict
from enum import Enum

@dataclass
class Employee:
    emp_id: int
    full_name: str
    department: str
    salary: int
    hire_date: str  # ISO date string

    def to_dict(self):
        return asdict(self)

class Department(Enum):
    IT = "IT"
    HR = "HR"
    OPERATIONS = "Operations"
    ADMINISTRATION = "Administration"
    FINANCE = "Finance"

