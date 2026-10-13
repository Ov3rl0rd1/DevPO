import csv
import os
import sys
import zipfile
from xml.etree import ElementTree

from PySide6.QtCore import QAbstractTableModel, QSettings, Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTableView,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)


SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".txt", ".docx"}
MAX_RECENT_FILES = 10


class TableModel(QAbstractTableModel):
    def __init__(self, rows):
        super().__init__()
        self.rows = rows
        self.column_count = max((len(row) for row in rows), default=0)

    def rowCount(self, parent=None):
        return len(self.rows)

    def columnCount(self, parent=None):
        return self.column_count

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole or not index.isValid():
            return None
        row = self.rows[index.row()]
        return row[index.column()] if index.column() < len(row) else ""

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return str(section + 1)
        return str(section + 1)


class FileViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("FileViewer", "FileViewer")
        self.setWindowTitle("Просмотрщик файлов")
        self.resize(900, 650)

        self.pages = QStackedWidget()
        self.setCentralWidget(self.pages)

        self.home_page = self.create_home_page()
        self.table_page = self.create_table_page()
        self.text_page = self.create_text_page()
        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.table_page)
        self.pages.addWidget(self.text_page)

        self.load_recent_files()

    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Просмотрщик файлов")
        title.setStyleSheet("font-size: 26px; font-weight: bold;")
        layout.addWidget(title)

        description = QLabel("Откройте файл CSV, XLSX, TXT или DOCX")
        layout.addWidget(description)

        choose_button = QPushButton("Выбрать файл")
        choose_button.clicked.connect(self.choose_file)
        layout.addWidget(choose_button)

        self.selected_file_label = QLabel("Файл не выбран")
        self.selected_file_label.setWordWrap(True)
        layout.addWidget(self.selected_file_label)

        layout.addWidget(QLabel("Недавние файлы"))
        self.recent_files = QListWidget()
        self.recent_files.itemDoubleClicked.connect(self.open_recent_file)
        layout.addWidget(self.recent_files)
        layout.addStretch()
        return page

    def create_table_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.table_title = QLabel()
        self.table_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.table_title)
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSortingEnabled(False)
        layout.addWidget(self.table_view)
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.show_home)
        layout.addWidget(back_button)
        return page

    def create_text_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.text_title = QLabel()
        self.text_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.text_title)
        self.text_view = QTextBrowser()
        layout.addWidget(self.text_view)
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.show_home)
        layout.addWidget(back_button)
        return page

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            "Поддерживаемые файлы (*.csv *.xlsx *.txt *.docx);;Все файлы (*)",
        )
        if file_path:
            self.open_file(file_path)

    def open_recent_file(self, item):
        self.open_file(item.data(Qt.ItemDataRole.UserRole))

    def open_file(self, file_path):
        if not os.path.isfile(file_path):
            self.show_error("Файл не найден", "Выбранный файл больше не существует.")
            self.load_recent_files()
            return

        extension = os.path.splitext(file_path)[1].lower()
        if extension not in SUPPORTED_EXTENSIONS:
            self.show_error("Неподдерживаемый формат", "Выберите файл CSV, XLSX, TXT или DOCX.")
            return

        try:
            if extension in {".csv", ".xlsx"}:
                rows = self.read_table(file_path, extension)
                self.table_view.setModel(TableModel(rows))
                self.table_view.resizeColumnsToContents()
                self.table_title.setText(os.path.basename(file_path))
                self.pages.setCurrentWidget(self.table_page)
            else:
                self.text_view.setPlainText(self.read_text(file_path, extension))
                self.text_title.setText(os.path.basename(file_path))
                self.pages.setCurrentWidget(self.text_page)
            self.selected_file_label.setText(file_path)
            self.save_recent_file(file_path)
        except (OSError, UnicodeError, ValueError, ElementTree.ParseError, zipfile.BadZipFile, csv.Error) as error:
            self.show_error("Не удалось открыть файл", str(error) or "Файл повреждён или его содержимое невозможно прочитать.")

    def read_table(self, file_path, extension):
        if extension == ".csv":
            with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
                return [row for row in csv.reader(file)]
        return self.read_xlsx(file_path)

    def read_xlsx(self, file_path):
        namespaces = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
        with zipfile.ZipFile(file_path) as archive:
            shared_strings = []
            if "xl/sharedStrings.xml" in archive.namelist():
                root = ElementTree.fromstring(archive.read("xl/sharedStrings.xml"))
                for item in root.findall("main:si", namespaces):
                    shared_strings.append("".join(node.text or "" for node in item.iter() if node.tag.endswith("}t")))

            worksheet_names = sorted(
                name for name in archive.namelist() if name.startswith("xl/worksheets/sheet") and name.endswith(".xml")
            )
            if not worksheet_names:
                raise ValueError("В книге нет листов.")
            root = ElementTree.fromstring(archive.read(worksheet_names[0]))
            rows = []
            for row_element in root.findall("main:sheetData/main:row", namespaces):
                row = []
                for cell in row_element.findall("main:c", namespaces):
                    value = cell.find("main:v", namespaces)
                    text = "" if value is None or value.text is None else value.text
                    if cell.get("t") == "s" and text:
                        text = shared_strings[int(text)]
                    elif cell.get("t") == "inlineStr":
                        text = "".join(node.text or "" for node in cell.iter() if node.tag.endswith("}t"))
                    row.append(text)
                rows.append(row)
            return rows

    def read_text(self, file_path, extension):
        if extension == ".txt":
            with open(file_path, "r", encoding="utf-8-sig") as file:
                return file.read()
        with zipfile.ZipFile(file_path) as archive:
            root = ElementTree.fromstring(archive.read("word/document.xml"))
        paragraphs = []
        for paragraph in root.iter():
            if paragraph.tag.endswith("}p"):
                parts = []
                for node in paragraph.iter():
                    if node.tag.endswith("}t") and node.text:
                        parts.append(node.text)
                    elif node.tag.endswith("}tab"):
                        parts.append("\t")
                paragraphs.append("".join(parts))
        return "\n".join(paragraphs)

    def save_recent_file(self, file_path):
        files = self.settings.value("recent_files", [], type=list)
        files = [file_path] + [path for path in files if path != file_path]
        self.settings.setValue("recent_files", files[:MAX_RECENT_FILES])
        self.load_recent_files()

    def load_recent_files(self):
        self.recent_files.clear()
        for file_path in self.settings.value("recent_files", [], type=list):
            item = QListWidgetItem(os.path.basename(file_path))
            item.setToolTip(file_path)
            item.setData(Qt.ItemDataRole.UserRole, file_path)
            self.recent_files.addItem(item)

    def show_home(self):
        self.pages.setCurrentWidget(self.home_page)

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileViewer()
    window.show()
    sys.exit(app.exec())