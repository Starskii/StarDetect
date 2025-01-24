from Views import MainView
import threading
from functools import partial


class AnnotateController:
    def __init__(self, main_view: MainView):
        self.annotate_tab = main_view.create_new_tab("Annotate")
