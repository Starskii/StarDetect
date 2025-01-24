from Views import MainView
import threading
from functools import partial


class HomeController:
    def __init__(self, main_view: MainView):
        self.home_tab = main_view.create_new_tab("Home")
