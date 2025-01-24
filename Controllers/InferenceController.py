from Views import MainView
import threading
from functools import partial


class InferenceController:
    def __init__(self, main_view: MainView):
        self.inference_tab = main_view.create_new_tab("Inference")
