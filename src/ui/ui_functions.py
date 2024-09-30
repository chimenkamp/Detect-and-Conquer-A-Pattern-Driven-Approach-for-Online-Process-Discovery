import importlib
import os
from copy import deepcopy
from typing import List, Literal, Tuple, Dict

from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtWidgets import QGraphicsScene

from src.ui.ui_generic_elements import CustomQGraphicsItem, CustomLineItem, PlaceGraphicsItem
from src.ui.widgets.abstract_widget import AbstractWidget


def create_connection(start: CustomQGraphicsItem, end: CustomQGraphicsItem, scene: QGraphicsScene) -> CustomLineItem:
    """
    Create a connection between two nodes.
    """
    l = CustomLineItem(start, end, scene)
    start.scene().addItem(l)
    start.scene().on_element_moved.connect(l.update_position)
    end.scene().on_element_moved.connect(l.update_position)
    return l


def load_widget_classes() -> List[AbstractWidget]:
    """
    Load the widget classes dynamically from the 'widgets/main' directory.

    :return: A list of widget classes.
    """
    widget_classes: List[AbstractWidget] = []
    widgets_dir = 'widgets/main'

    for filename in os.listdir(widgets_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]
            module_path = f'widgets.main.{module_name}'
            module = importlib.import_module(module_path)

            for attr in dir(module):
                obj = getattr(module, attr)
                if isinstance(obj, type) and issubclass(obj, AbstractWidget) and obj is not AbstractWidget:
                    widget_classes.append(obj)

    return widget_classes


def update_position_to_place_new_element(item: CustomQGraphicsItem,
                                         direction: Literal["top", "bottom", "right", "left"]) -> Tuple[int, int]:
    """
    Update the position of the new element to be placed in the scene based on the current item's position.

    :param item: The current QGraphicsItem whose position will be the reference.
    :param direction: The direction in which to move the position ("top", "bottom", "right", "left").
    :return: A tuple containing the new x and y coordinates as integers.
    """
    # Get the absolute position in the scene
    position: QPointF = item.mapToScene(item.pos())

    print(f"Position: {position.x()}, {position.y()}")

    position_new: Dict[str, int] = {"x": int(position.x()), "y": int(position.y())}

    if direction == "top":
        position_new["y"] -= 50
    elif direction == "bottom":
        position_new["y"] += 50
    elif direction == "right":
        position_new["x"] += 50
    elif direction == "left":
        position_new["x"] -= 50

    return position_new["x"], position_new["y"]
