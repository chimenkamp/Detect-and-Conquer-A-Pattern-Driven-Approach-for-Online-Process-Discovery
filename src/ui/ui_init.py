import sys

from PyQt5.QtCore import QSize, QPoint, Qt, QSettings, QFile, QTextStream, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, \
    QHeaderView, QTabWidget, QAction, QPushButton, QLabel, QGridLayout

from src.ui.ui_functions import load_widget_classes
from src.ui.ui_stylesheet import UI_WIDGET_BUTTON_STYLE
from src.ui.widgets.abstract_widget import AbstractWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Process Mining Tool Box")
        self.setGeometry(100, 100, 1920, 1080)

        self.settings = QSettings('petri_net_editor', 'pn_editor')
        self.tabs = QTabWidget()

        self.overview_widget = OverviewWidget(self)
        self.setCentralWidget(self.overview_widget)

        self.resize(self.settings.value("size", QSize(1920, 1080)))
        self.move(self.settings.value("pos", QPoint(100, 100)))

        self.init_menu()

    def init_menu(self) -> None:
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        new_tab_action = QAction('New Tab', self)
        new_tab_action.setShortcut('Ctrl+T')
        file_menu.addAction(new_tab_action)

    def closeEvent(self, e) -> None:
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        e.accept()


class OverviewWidget(QWidget):
    def __init__(self, main_window: MainWindow) -> None:
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self) -> None:
        layout = QGridLayout()
        widget_classes = load_widget_classes()

        for index, widget_class in enumerate(widget_classes):
            instance = widget_class()
            tile_button = self.create_tile(widget_class.__name__, instance)
            layout.addWidget(tile_button, index // 2, index % 2)

        self.setLayout(layout)

    def create_tile(self, title: str, widget_instance: AbstractWidget) -> QPushButton:
        """
        Create a tile that acts as a button. The button contains the title and
        will open the corresponding widget when clicked.

        :param title: The title of the widget to display on the tile.
        :param widget_instance: The instance of the widget to open on click.
        :return: A QPushButton configured as a tile.
        """
        tile_button = QPushButton()
        tile_button.setFixedSize(150, 100)
        tile_button.setStyleSheet(UI_WIDGET_BUTTON_STYLE)

        tile_layout = QVBoxLayout(tile_button)
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        tile_layout.addWidget(title_label)

        tile_button.clicked.connect(lambda: self.open_widget(widget_instance))
        return tile_button

    def open_widget(self, widget_instance: AbstractWidget) -> None:
        """
        Open the selected widget in the main window's tab area.

        :param widget_instance: The instance of the widget to open.
        """
        self.main_window.tabs.addTab(widget_instance, widget_instance.__class__.__name__)
        self.main_window.setCentralWidget(self.main_window.tabs)


def main() -> None:
    app = QApplication(sys.argv)
    file = QFile(":/dark.qss")
    if file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(file)
        app.setStyleSheet(stream.readAll())
    else:
        ...
        # QMessageBox.warning(None, "Warning", "Failed to load stylesheet.")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
