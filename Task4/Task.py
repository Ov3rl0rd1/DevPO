import sys
from pathlib import Path

from PySide6.QtCore import Property, QObject, QTimer, Signal, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle


EQUIPMENT_TYPES = ["Станок", "Компьютер", "Транспорт", "Инструмент", "Прочее"]

DEFAULT_TYPE_INDEX = 0
DEFAULT_QUANTITY = 1
DEFAULT_ACTIVE = True
DEFAULT_WEAR = 0

QML_FILE = Path(__file__).resolve().parent / "Main.qml"


class EquipmentCardViewModel(QObject):
    nameChanged = Signal()
    inventoryChanged = Signal()
    typeIndexChanged = Signal()
    quantityChanged = Signal()
    activeChanged = Signal()
    wearChanged = Signal()
    notesChanged = Signal()
    formChanged = Signal()
    statusMessageChanged = Signal()
    saved = Signal()

    def __init__(self):
        super().__init__()
        self._name = ""
        self._inventory = ""
        self._type_index = DEFAULT_TYPE_INDEX
        self._quantity = DEFAULT_QUANTITY
        self._active = DEFAULT_ACTIVE
        self._wear = DEFAULT_WEAR
        self._notes = ""
        self._status_message = ""

        self._status_timer = QTimer(self)
        self._status_timer.setSingleShot(True)
        self._status_timer.timeout.connect(lambda: self._set_status_message(""))

    @Property(list, constant=True)
    def equipmentTypes(self):
        return EQUIPMENT_TYPES

    @Property(str, notify=nameChanged)
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._update("_name", value, self.nameChanged)

    @Property(str, notify=inventoryChanged)
    def inventory(self):
        return self._inventory

    @inventory.setter
    def inventory(self, value):
        self._update("_inventory", value, self.inventoryChanged)

    @Property(int, notify=typeIndexChanged)
    def typeIndex(self):
        return self._type_index

    @typeIndex.setter
    def typeIndex(self, value):
        self._update("_type_index", value, self.typeIndexChanged)

    @Property(int, notify=quantityChanged)
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._update("_quantity", value, self.quantityChanged)

    @Property(bool, notify=activeChanged)
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._update("_active", value, self.activeChanged)

    @Property(int, notify=wearChanged)
    def wear(self):
        return self._wear

    @wear.setter
    def wear(self, value):
        self._update("_wear", value, self.wearChanged)

    @Property(str, notify=notesChanged)
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, value):
        self._update("_notes", value, self.notesChanged)

    @Property(bool, notify=nameChanged)
    def canSave(self):
        return bool(self._name.strip())

    @Property(str, notify=formChanged)
    def preview(self):
        name = self._name.strip() or "—"
        inventory = self._inventory.strip() or "—"
        equipment_type = EQUIPMENT_TYPES[self._type_index]
        status = "в эксплуатации" if self._active else "не используется"
        notes = self._notes.strip() or "—"

        return (
            f"Название: {name}\n"
            f"Инвентарный номер: {inventory}\n"
            f"Тип: {equipment_type}\n"
            f"Количество: {self._quantity} шт.\n"
            f"Статус: {status}\n"
            f"Износ: {self._wear}%\n"
            f"Примечания: {notes}"
        )

    @Property(str, notify=statusMessageChanged)
    def statusMessage(self):
        return self._status_message

    @Slot()
    def save(self):
        if not self.canSave:
            return
        self._show_status("Карточка сохранена", 5000)
        self.saved.emit()

    @Slot()
    def clear(self):
        self.name = ""
        self.inventory = ""
        self.typeIndex = DEFAULT_TYPE_INDEX
        self.quantity = DEFAULT_QUANTITY
        self.active = DEFAULT_ACTIVE
        self.wear = DEFAULT_WEAR
        self.notes = ""
        self._show_status("Форма очищена", 3000)

    def _update(self, attribute, value, signal):
        if getattr(self, attribute) == value:
            return
        setattr(self, attribute, value)
        signal.emit()
        self.formChanged.emit()

    def _show_status(self, message, timeout):
        self._set_status_message(message)
        self._status_timer.start(timeout)

    def _set_status_message(self, message):
        self._status_message = message
        self.statusMessageChanged.emit()


def main():
    app = QGuiApplication(sys.argv)
    QQuickStyle.setStyle("Fusion")

    view_model = EquipmentCardViewModel()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("cardViewModel", view_model)
    engine.load(str(QML_FILE))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
