from Views import MainView
import threading
from functools import partial
from Models.ProfileManager import ProfileManager



class TrainController:
    def __init__(self, main_view: MainView, profile_manager: ProfileManager):
        self.train_tab = main_view.create_new_tab("Train")
        self.profile_manager = profile_manager
