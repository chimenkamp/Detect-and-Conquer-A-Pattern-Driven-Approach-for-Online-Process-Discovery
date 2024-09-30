from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem

from src.ui.widgets.abstract_widget import AbstractWidget


class TerminalView(AbstractWidget):
    def __init__(self) -> None:
        super().__init__()

        self.table = None
        self.layout = None

        self.columns = ["Timestamp", "CaseID", "Activity"]
        self.init_ui()
        self._name = "Terminal View"

    def init_ui(self) -> None:
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.table.setRowCount(0)
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)

        self.set_table_style()

    def set_table_style(self) -> None:
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("color: black; alternate-background-color: #f0f0f0; background-color: #ffffff;")

        font = QFont("Arial", 12, QFont.Bold)
        self.table.setFont(font)

        header_font = QFont("Arial", 14, QFont.Bold)
        self.table.horizontalHeader().setFont(header_font)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)

        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def add_row(self, data: list[str]) -> None:
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        for column, value in enumerate(data):
            self.table.setItem(row_position, column, QTableWidgetItem(value))

        self.table.scrollToBottom()
