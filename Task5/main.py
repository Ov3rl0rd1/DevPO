import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

from controllers.equipment_controller import EquipmentController
from models.equipment_filter_model import EquipmentFilterModel
from models.equipment_model import EquipmentModel
from services.storage import JsonStorage, StorageError


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "equipment.json"
QML_FILE = BASE_DIR / "qml" / "Main.qml"


def main():
    app = QGuiApplication(sys.argv)
    QQuickStyle.setStyle("Fusion")

    storage = JsonStorage(DATA_FILE)
    try:
        items = storage.load()
    except StorageError as error:
        sys.exit(str(error))

    model = EquipmentModel(items)
    filter_model = EquipmentFilterModel(model)
    controller = EquipmentController(model, storage)

    engine = QQmlApplicationEngine()
    context = engine.rootContext()
    context.setContextProperty("equipmentModel", model)
    context.setContextProperty("equipmentFilter", filter_model)
    context.setContextProperty("equipmentController", controller)
    engine.load(str(QML_FILE))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
