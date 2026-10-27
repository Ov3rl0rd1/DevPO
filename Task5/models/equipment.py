from dataclasses import asdict, dataclass, fields
from datetime import date


CATEGORIES = [
    "Трактор",
    "Комбайн",
    "Грузовой автомобиль",
    "Опрыскиватель",
    "Сеялка",
    "Культиватор",
    "Погрузчик",
    "Прочее",
]

STATUSES = ["Исправна", "Требует обслуживания", "В ремонте", "Списана"]

MIN_YEAR = 1950
MAX_YEAR = date.today().year
MAX_CONDITION = 100


@dataclass
class Equipment:
    id: int = 0
    name: str = ""
    category: str = CATEGORIES[0]
    inventory_number: str = ""
    year: int = MAX_YEAR
    status: str = STATUSES[0]
    location: str = ""
    responsible: str = ""
    hours: int = 0
    active: bool = True
    condition: int = MAX_CONDITION

    @classmethod
    def from_dict(cls, data):
        values = {}
        for field in fields(cls):
            value = field.type(data.get(field.name, field.default))
            values[field.name] = value.strip() if isinstance(value, str) else value
        return cls(**values)

    def to_dict(self):
        return asdict(self)
