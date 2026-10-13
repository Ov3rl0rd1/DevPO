import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


EQUIPMENT_TYPES = ["Станок", "Компьютер", "Транспорт", "Инструмент", "Прочее"]

DEFAULT_TYPE_INDEX = 0
DEFAULT_QUANTITY = 1
DEFAULT_ACTIVE = True
DEFAULT_WEAR = 0


class EquipmentCardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Карточка объекта учёта: Оборудование")
        self.resize(560, 640)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        form_layout = QFormLayout()
        main_layout.addLayout(form_layout)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Например, Токарный станок ТС-16")
        form_layout.addRow("Название объекта*:", self.name_edit)

        self.inventory_edit = QLineEdit()
        self.inventory_edit.setPlaceholderText("Например, INV-00123")
        form_layout.addRow("Инвентарный номер:", self.inventory_edit)

        self.type_combo = QComboBox()
        self.type_combo.addItems(EQUIPMENT_TYPES)
        form_layout.addRow("Тип оборудования:", self.type_combo)

        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(0, 1000)
        self.quantity_spin.setValue(DEFAULT_QUANTITY)
        self.quantity_spin.setSuffix(" шт.")
        form_layout.addRow("Количество:", self.quantity_spin)

        self.active_check = QCheckBox("В эксплуатации")
        self.active_check.setChecked(DEFAULT_ACTIVE)
        form_layout.addRow("Статус:", self.active_check)

        slider_layout = QHBoxLayout()
        self.wear_slider = QSlider(Qt.Horizontal)
        self.wear_slider.setRange(0, 100)
        self.wear_slider.setValue(DEFAULT_WEAR)
        self.wear_value_label = QLabel(f"{DEFAULT_WEAR}%")
        self.wear_value_label.setMinimumWidth(40)
        slider_layout.addWidget(self.wear_slider)
        slider_layout.addWidget(self.wear_value_label)
        form_layout.addRow("Степень износа:", slider_layout)

        self.notes_edit = QPlainTextEdit()
        self.notes_edit.setPlaceholderText("Дополнительные сведения об объекте")
        self.notes_edit.setFixedHeight(80)
        form_layout.addRow("Примечания:", self.notes_edit)

        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.clear_button = QPushButton("Очистить")
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.clear_button)
        main_layout.addLayout(buttons_layout)

        main_layout.addWidget(QLabel("Предпросмотр карточки:"))
        self.preview_label = QLabel()
        self.preview_label.setWordWrap(True)
        self.preview_label.setFrameShape(QFrame.Panel)
        self.preview_label.setFrameShadow(QFrame.Sunken)
        self.preview_label.setMargin(8)
        main_layout.addWidget(self.preview_label)

        main_layout.addStretch()

        self.name_edit.textChanged.connect(self.update_preview)
        self.inventory_edit.textChanged.connect(self.update_preview)
        self.type_combo.currentIndexChanged.connect(self.update_preview)
        self.quantity_spin.valueChanged.connect(self.update_preview)
        self.active_check.stateChanged.connect(self.update_preview)
        self.wear_slider.valueChanged.connect(self.on_wear_changed)
        self.notes_edit.textChanged.connect(self.update_preview)

        self.save_button.clicked.connect(self.save_card)
        self.clear_button.clicked.connect(self.reset_form)
        self.clear_button.clicked.connect(self.name_edit.clear)
        self.clear_button.clicked.connect(self.inventory_edit.clear)
        self.clear_button.clicked.connect(self.notes_edit.clear)

        self.update_preview()

    def on_wear_changed(self, value):
        self.wear_value_label.setText(f"{value}%")
        self.update_preview()

    def update_preview(self, *args):
        name = self.name_edit.text().strip() or "—"
        inventory = self.inventory_edit.text().strip() or "—"
        equipment_type = self.type_combo.currentText()
        quantity = self.quantity_spin.value()
        status = "в эксплуатации" if self.active_check.isChecked() else "не используется"
        wear = self.wear_slider.value()
        notes = self.notes_edit.toPlainText().strip() or "—"

        text = (
            f"Название: {name}\n"
            f"Инвентарный номер: {inventory}\n"
            f"Тип: {equipment_type}\n"
            f"Количество: {quantity} шт.\n"
            f"Статус: {status}\n"
            f"Износ: {wear}%\n"
            f"Примечания: {notes}"
        )
        self.preview_label.setText(text)

    def save_card(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Необходимо заполнить название объекта")
            self.name_edit.setFocus()
            return

        QMessageBox.information(self, "Сохранено", "Карточка объекта успешно сохранена.")
        self.statusBar().showMessage("Карточка сохранена", 5000)

    def reset_form(self):
        self.type_combo.setCurrentIndex(DEFAULT_TYPE_INDEX)
        self.quantity_spin.setValue(DEFAULT_QUANTITY)
        self.active_check.setChecked(DEFAULT_ACTIVE)
        self.wear_slider.setValue(DEFAULT_WEAR)
        self.statusBar().showMessage("Форма очищена", 3000)


def main():
    app = QApplication(sys.argv)
    window = EquipmentCardWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
