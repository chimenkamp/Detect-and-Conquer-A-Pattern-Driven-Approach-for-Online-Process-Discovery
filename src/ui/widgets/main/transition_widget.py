from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFormLayout, QLineEdit,
    QTextEdit, QComboBox, QCheckBox, QPushButton, QTimeEdit, QStackedWidget,
    QMessageBox
)
from PyQt5.QtCore import Qt

from src.ui.widgets.abstract_widget import AbstractWidget


class TransitionWidget(AbstractWidget):
    """
    TransitionWidget represents a form to add transition information.

    :return: None
    """

    def __init__(self) -> None:
        """
        Initialize the TransitionWidget.

        :return: None
        """
        super().__init__()
        self._name = "Transition Settings"
        self.init_ui()

    def init_ui(self) -> None:
        """
        Initialize the UI components of the widget.

        :return: None
        """
        main_layout = QVBoxLayout()

        # Header
        header_label = QLabel("Add your Transition-Information")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)

        # Introduction text
        intro_label_left = QLabel("Here you can enter the data required for the simulation.")
        intro_label_left.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(intro_label_left)



        # Form
        form_layout = QFormLayout()

        # Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Add a name")
        form_layout.addRow("Name", self.name_input)

        # Description
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Give your transition a description!")
        form_layout.addRow("Description", self.description_input)

        # Duration Distribution Type
        self.dur_dist_type_combobox = QComboBox()
        self.dur_dist_type_combobox.addItems([
            "Fixed duration",
            "Gaussian distributed duration",
            "Duration distributed as equipartition"
        ])
        self.dur_dist_type_combobox.currentIndexChanged.connect(self.on_dur_dist_type_changed)
        form_layout.addRow("Duration Distribution Type", self.dur_dist_type_combobox)

        # Mark Transition as Silent
        self.is_silent_checkbox = QCheckBox("Is Silent")
        form_layout.addRow("Mark Transition as Silent", self.is_silent_checkbox)

        main_layout.addLayout(form_layout)

        self.dur_dist_type_label = QLabel("Fixed Duration")
        self.dur_dist_type_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.dur_dist_type_label)

        # Conditional Layouts based on Distribution Type
        self.stacked_widget = QStackedWidget()

        # Fixed Duration
        self.fixed_duration_layout = QFormLayout()
        self.fixed_duration_input = QTimeEdit()
        self.fixed_duration_layout.addRow("Fixed Duration", self.fixed_duration_input)
        fixed_duration_widget = QWidget()
        fixed_duration_widget.setLayout(self.fixed_duration_layout)
        self.stacked_widget.addWidget(fixed_duration_widget)

        # Gaussian Distribution
        self.gaussian_layout = QFormLayout()
        self.mean_time_input = QTimeEdit()
        self.std_dev_input = QTimeEdit()
        self.gaussian_layout.addRow("Mean Time", self.mean_time_input)
        self.gaussian_layout.addRow("Standard Deviation", self.std_dev_input)
        gaussian_widget = QWidget()
        gaussian_widget.setLayout(self.gaussian_layout)
        self.stacked_widget.addWidget(gaussian_widget)

        # Equipartition Distribution
        self.equipartition_layout = QFormLayout()
        self.lower_border_input = QTimeEdit()
        self.upper_border_input = QTimeEdit()
        self.equipartition_layout.addRow("Lower Border (From)", self.lower_border_input)
        self.equipartition_layout.addRow("Upper Border (Until)", self.upper_border_input)
        equipartition_widget = QWidget()
        equipartition_widget.setLayout(self.equipartition_layout)
        self.stacked_widget.addWidget(equipartition_widget)

        main_layout.addWidget(self.stacked_widget)

        # Bottom Section
        action_layout = QVBoxLayout()
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.on_save_clicked)
        action_layout.addWidget(save_button)
        action_layout.addWidget(close_button)
        main_layout.addLayout(action_layout)

        self.setLayout(main_layout)

    def on_dur_dist_type_changed(self, index: int) -> None:
        """
        Handles the change in duration distribution type.

        :param index: Index of the selected item in the combo box.
        :return: None
        """
        try:
            self.stacked_widget.setCurrentIndex(index)
            label_text = ["Fixed Duration", "Gaussian Distribution", "Equipartition Distribution"]
            self.dur_dist_type_label.setText(label_text[index])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def on_save_clicked(self) -> None:
        """
        Handles the save action.

        :return: None
        """
        # Add validation or save logic here
        QMessageBox.information(self, "Saved", "Transition information has been saved.")
