from datetime import time, datetime
from typing import Optional

import pm4py
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QSplitter, QVBoxLayout
from graphviz import Digraph

from src.ui.ui_generic_elements import TransitionGraphicsItem

from src.ui.ui_petri_net_view import PetriNetEditorView
from src.ui.widgets.abstract_widget import AbstractWidget
from src.utils.petri_net_renderer import render_petri_net
from tests.parse_petri_net_test_file import online_order_petri_net


def load_and_parse_petri_net() -> Digraph:
    net = online_order_petri_net()
    # net, im, fm = pm4py.read_pnml("model2012.pnml")

    # seq, and_p, or_p = identify_patterns(net.places, net.transitions, net.arcs)
    #
    # color_iterator = ColorIterator()
    #
    # for pattern in seq:
    #     col: str = next(color_iterator)
    #     for elem in pattern:
    #         elem.properties["color"] = col

    return render_petri_net(net, False)


def open_and_parse_file(file_name: str) -> Optional[Digraph]:
    if file_name.endswith(".pnml"):
        net, im, fm = pm4py.read_pnml(file_name)
        return render_petri_net(net, False)


class PetriNetWidget(AbstractWidget):
    def __init__(self) -> None:
        super().__init__()

        self.graph_view = None
        self.splitter = None

        current: int = 0

        if current == 0:
            self.init_editor(load_and_parse_petri_net())
        else:
            file_name, _ = QFileDialog.getOpenFileName(self, "Open Petri Net File", "",
                                                       "Petri Net Files (*.pnml *.xml);;All Files (*)")
            if not file_name:
                raise FileNotFoundError("No file selected. Please select a valid Petri net file.")

            dot: Optional[Digraph] = open_and_parse_file(file_name)
            if dot is None:
                raise ValueError("Failed to parse Petri net file.")
            self.init_editor(dot)

    def init_editor(self, dot: Digraph) -> None:
        # time.sleep(3)
        self.graph_view = PetriNetEditorView(dot)
        #self.terminal_view = TerminalView(['Timestamp', 'CaseID', 'Activity'])

        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.graph_view)
        #self.splitter.addWidget(self.terminal_view)
        #self.splitter.setSizes([1080, 360])

        layout = QVBoxLayout(self)
        layout.addWidget(self.splitter)
        self.setLayout(layout)

        # self.graph_view.scene.on_transition_fired.connect(self.on_transition_fired)

    @pyqtSlot(TransitionGraphicsItem)
    def on_transition_fired(self, transition: TransitionGraphicsItem) -> None:
        activity: str = transition.text_item.toPlainText() if transition.text_item else "No Activity"
        self.terminal_view.add_row([str(datetime.now()), "sfefwef", activity])
