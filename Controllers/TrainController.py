from Views import MainView
import threading
from functools import partial


class TrainController:
    def __init__(self, main_view: MainView):
        self.train_tab = main_view.create_new_tab("Train")
