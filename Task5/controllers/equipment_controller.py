from PySide6.QtCore import Property, QObject, Signal, Slot

from models.equipment import (
    CATEGORIES,
    MAX_CONDITION,
    MAX_YEAR,
    MIN_YEAR,
    STATUSES,
    Equipment,
)


class EquipmentController(QObject):
    errorOccurred = Signal(str)

    def __init__(self, model, storage):
        super().__init__()
        self._model = model
        self._storage = storage

    @Property(list, constant=True)
    def categories(self):
        return CATEGORIES

    @Property(list, constant=True)
    def statuses(self):
        return STATUSES

    @Property(int, constant=True)
    def minYear(self):
        return MIN_YEAR

    @Property(int, constant=True)
    def maxYear(self):
        return MAX_YEAR

    @Property("QVariantMap", constant=True)
    def defaults(self):
        return Equipment().to_dict()

    @Slot(int, result="QVariantMap")
    def find(self, equipment_id):
        equipment = self._model.find(equipment_id)
        return equipment.to_dict() if equipment else {}

    @Slot("QVariantMap", result=str)
    def save(self, data):
        try:
            equipment = Equipment.from_dict(data)
        except (TypeError, ValueError):
            return "Проверьте правильность заполнения полей."

        errors = self._validate(equipment)
        if errors:
            return "\n".join(errors)

        if equipment.id:
            self._model.update(equipment)
        else:
            equipment.id = self._model.next_id()
            self._model.add(equipment)
        self._persist()
        return ""

    @Slot(int)
    def remove(self, equipment_id):
        if self._model.find(equipment_id) is None:
            return
        self._model.remove(equipment_id)
        self._persist()

    def _validate(self, equipment):
        errors = []
        if equipment.id and self._model.find(equipment.id) is None:
            errors.append("Редактируемая запись не найдена.")
        if not equipment.name:
            errors.append("Укажите название техники.")
        if not equipment.inventory_number:
            errors.append("Укажите инвентарный номер.")
        elif self._model.has_inventory_number(equipment.inventory_number, equipment.id):
            errors.append(f"Инвентарный номер «{equipment.inventory_number}» уже используется.")
        if equipment.category not in CATEGORIES:
            errors.append("Выберите тип техники из списка.")
        if equipment.status not in STATUSES:
            errors.append("Выберите состояние из списка.")
        if not MIN_YEAR <= equipment.year <= MAX_YEAR:
            errors.append(f"Год выпуска должен быть в диапазоне {MIN_YEAR}–{MAX_YEAR}.")
        if equipment.hours < 0:
            errors.append("Моточасы не могут быть отрицательными.")
        if not 0 <= equipment.condition <= MAX_CONDITION:
            errors.append(f"Оценка состояния должна быть в диапазоне 0–{MAX_CONDITION}.")
        return errors

    def _persist(self):
        try:
            self._storage.save(self._model.items())
        except OSError as error:
            self.errorOccurred.emit(f"Не удалось сохранить данные: {error}")
