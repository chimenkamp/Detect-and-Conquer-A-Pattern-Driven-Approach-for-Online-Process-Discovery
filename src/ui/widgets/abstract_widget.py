from abc import abstractproperty, ABC

from PyQt5.QtWidgets import QWidget

from abc import ABC
from PyQt5.QtWidgets import QWidget


class AbstractWidget(QWidget):
    _name: str = "Abstract Widget"

    @property
    def getName(self) -> str:
        """
        Concrete property with a default value.

        :return: The name of the widget.
        """
        return self._name
