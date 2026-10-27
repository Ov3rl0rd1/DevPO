from collections import Counter

from PySide6.QtCore import Property, QAbstractListModel, QModelIndex, Qt, Signal

from models.equipment import STATUSES


class EquipmentModel(QAbstractListModel):
    IdRole = Qt.ItemDataRole.UserRole + 1
    NameRole = Qt.ItemDataRole.UserRole + 2
    CategoryRole = Qt.ItemDataRole.UserRole + 3
    StatusRole = Qt.ItemDataRole.UserRole + 4
    InventoryRole = Qt.ItemDataRole.UserRole + 5
    YearRole = Qt.ItemDataRole.UserRole + 6
    LocationRole = Qt.ItemDataRole.UserRole + 7
    ResponsibleRole = Qt.ItemDataRole.UserRole + 8
    HoursRole = Qt.ItemDataRole.UserRole + 9
    ActiveRole = Qt.ItemDataRole.UserRole + 10
    ConditionRole = Qt.ItemDataRole.UserRole + 11

    ROLES = {
        IdRole: (b"equipmentId", "id"),
        NameRole: (b"name", "name"),
        CategoryRole: (b"category", "category"),
        StatusRole: (b"status", "status"),
        InventoryRole: (b"inventoryNumber", "inventory_number"),
        YearRole: (b"year", "year"),
        LocationRole: (b"location", "location"),
        ResponsibleRole: (b"responsible", "responsible"),
        HoursRole: (b"hours", "hours"),
        ActiveRole: (b"active", "active"),
        ConditionRole: (b"condition", "condition"),
    }

    summaryChanged = Signal()

    def __init__(self, items=None):
        super().__init__()
        self._items = items or []

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role not in self.ROLES:
            return None
        _, attribute = self.ROLES[role]
        return getattr(self._items[index.row()], attribute)

    def roleNames(self):
        return {role: name for role, (name, _) in self.ROLES.items()}

    @Property(int, notify=summaryChanged)
    def count(self):
        return len(self._items)

    @Property(list, notify=summaryChanged)
    def statistics(self):
        statuses = Counter(item.status for item in self._items)
        return [{"title": "Всего", "value": len(self._items)}] + [
            {"title": status, "value": statuses[status]} for status in STATUSES
        ]

    def items(self):
        return list(self._items)

    def item(self, row):
        return self._items[row]

    def find(self, equipment_id):
        return next((item for item in self._items if item.id == equipment_id), None)

    def next_id(self):
        return max((item.id for item in self._items), default=0) + 1

    def has_inventory_number(self, inventory_number, exclude_id=0):
        number = inventory_number.casefold()
        return any(
            item.inventory_number.casefold() == number and item.id != exclude_id
            for item in self._items
        )

    def add(self, equipment):
        row = len(self._items)
        self.beginInsertRows(QModelIndex(), row, row)
        self._items.append(equipment)
        self.endInsertRows()
        self.summaryChanged.emit()

    def update(self, equipment):
        row = self._row_of(equipment.id)
        self._items[row] = equipment
        index = self.index(row)
        self.dataChanged.emit(index, index)
        self.summaryChanged.emit()

    def remove(self, equipment_id):
        row = self._row_of(equipment_id)
        self.beginRemoveRows(QModelIndex(), row, row)
        del self._items[row]
        self.endRemoveRows()
        self.summaryChanged.emit()

    def _row_of(self, equipment_id):
        for row, item in enumerate(self._items):
            if item.id == equipment_id:
                return row
        raise KeyError(equipment_id)
