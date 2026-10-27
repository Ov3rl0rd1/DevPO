from PySide6.QtCore import Property, QSortFilterProxyModel, Qt, Signal

from models.equipment_model import EquipmentModel


SORT_OPTIONS = [
    ("По названию", EquipmentModel.NameRole, Qt.SortOrder.AscendingOrder),
    ("По году выпуска", EquipmentModel.YearRole, Qt.SortOrder.DescendingOrder),
    ("По моточасам", EquipmentModel.HoursRole, Qt.SortOrder.DescendingOrder),
]


class EquipmentFilterModel(QSortFilterProxyModel):
    searchTextChanged = Signal()
    categoryChanged = Signal()
    statusChanged = Signal()
    sortIndexChanged = Signal()

    def __init__(self, source_model):
        super().__init__()
        self._search_text = ""
        self._category = ""
        self._status = ""
        self._sort_index = 0

        self.setSourceModel(source_model)
        self.setSortLocaleAware(True)
        self.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self._apply_sort()

    @Property(list, constant=True)
    def sortOptions(self):
        return [title for title, _, _ in SORT_OPTIONS]

    @Property(str, notify=searchTextChanged)
    def searchText(self):
        return self._search_text

    @searchText.setter
    def searchText(self, value):
        self._update_filter("_search_text", value, self.searchTextChanged)

    @Property(str, notify=categoryChanged)
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._update_filter("_category", value, self.categoryChanged)

    @Property(str, notify=statusChanged)
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._update_filter("_status", value, self.statusChanged)

    @Property(int, notify=sortIndexChanged)
    def sortIndex(self):
        return self._sort_index

    @sortIndex.setter
    def sortIndex(self, value):
        if self._sort_index == value:
            return
        self._sort_index = value
        self._apply_sort()
        self.sortIndexChanged.emit()

    def filterAcceptsRow(self, source_row, source_parent):
        equipment = self.sourceModel().item(source_row)
        search = self._search_text.strip().casefold()
        matches_search = (
            search in equipment.name.casefold()
            or search in equipment.inventory_number.casefold()
        )
        matches_category = not self._category or equipment.category == self._category
        matches_status = not self._status or equipment.status == self._status
        return matches_search and matches_category and matches_status

    def _update_filter(self, attribute, value, signal):
        if getattr(self, attribute) == value:
            return
        self.beginFilterChange()
        setattr(self, attribute, value)
        self.endFilterChange(QSortFilterProxyModel.Direction.Rows)
        signal.emit()

    def _apply_sort(self):
        _, role, order = SORT_OPTIONS[self._sort_index]
        self.setSortRole(role)
        self.sort(0, order)
