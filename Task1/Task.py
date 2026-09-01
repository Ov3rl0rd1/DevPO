import sys
from math import pi

from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QTextEdit,
)


class ShapeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор фигур")
        self.resize(500, 420)

        self.shape_combo = QComboBox()
        self.shape_combo.addItems(["Круг", "Квадрат", "Треугольник", "Куб", "Шар"])

        self.input_layout = QFormLayout()
        self.fields = {}

        self.calculate_button = QPushButton("Рассчитать")
        self.calculate_button.clicked.connect(self.calculate)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setPlainText("Выберите фигуру и введите данные.")

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(QLabel("Фигура:"))
        main_layout.addWidget(self.shape_combo)
        main_layout.addLayout(self.input_layout)
        main_layout.addWidget(self.calculate_button)
        main_layout.addWidget(QLabel("Результат:"))
        main_layout.addWidget(self.result_box)

        self.shape_combo.currentIndexChanged.connect(self.update_fields)
        self.update_fields()

    def update_fields(self):
        shape = self.shape_combo.currentText()

        for i in range(self.input_layout.count()):
            item = self.input_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.fields.clear()

        if shape == "Круг":
            params = [("Радиус r:", "r")]
        elif shape == "Квадрат":
            params = [("Сторона a:", "a")]
        elif shape == "Треугольник":
            params = [
                ("Основание a:", "a"),
                ("Высота h:", "h"),
                ("Сторона b:", "b"),
                ("Сторона c:", "c"),
            ]
        elif shape == "Куб":
            params = [("Ребро a:", "a")]
        elif shape == "Шар":
            params = [("Радиус r:", "r")]
        else:
            params = []

        for label_text, key in params:
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("Введите число")
            self.input_layout.addRow(label_text, line_edit)
            self.fields[key] = line_edit

    def parse_number(self, key, required=True):
        value = self.fields[key].text().strip().replace(",", ".")
        if value == "":
            if required:
                raise ValueError(f"Поле '{key}' не заполнено.")
            return None
        try:
            return float(value)
        except ValueError as exc:
            raise ValueError(f"Поле '{key}' должно быть числом.") from exc

    def calculate(self):
        shape = self.shape_combo.currentText()

        try:
            if shape == "Круг":
                r = self.parse_number("r")
                area = pi * r ** 2
                perimeter = 2 * pi * r
                volume = "Не применимо"
                result = (
                    f"Площадь: {area:.3f}\n"
                    f"Периметр: {perimeter:.3f}\n"
                    f"Объем: {volume}"
                )

            elif shape == "Квадрат":
                a = self.parse_number("a")
                area = a ** 2
                perimeter = 4 * a
                volume = "Не применимо"
                result = (
                    f"Площадь: {area:.3f}\n"
                    f"Периметр: {perimeter:.3f}\n"
                    f"Объем: {volume}"
                )

            elif shape == "Треугольник":
                a = self.parse_number("a")
                h = self.parse_number("h")
                b = self.parse_number("b")
                c = self.parse_number("c")
                area = (a * h) / 2
                perimeter = a + b + c
                volume = "Не применимо"
                result = (
                    f"Площадь: {area:.3f}\n"
                    f"Периметр: {perimeter:.3f}\n"
                    f"Объем: {volume}"
                )

            elif shape == "Куб":
                a = self.parse_number("a")
                area = 6 * a ** 2
                perimeter = 12 * a
                volume = a ** 3
                result = (
                    f"Площадь: {area:.3f}\n"
                    f"Периметр: {perimeter:.3f}\n"
                    f"Объем: {volume:.3f}"
                )

            elif shape == "Шар":
                r = self.parse_number("r")
                area = 4 * pi * r ** 2
                perimeter = "Не применимо"
                volume = 4 / 3 * pi * r ** 3
                result = (
                    f"Площадь: {area:.3f}\n"
                    f"Периметр: {perimeter}\n"
                    f"Объем: {volume:.3f}"
                )
            else:
                result = "Выберите фигуру."

            self.result_box.setPlainText(result)

        except ValueError as exc:
            QMessageBox.critical(self, "Ошибка", str(exc))


def main():
    app = QApplication(sys.argv)
    window = ShapeCalculator()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
