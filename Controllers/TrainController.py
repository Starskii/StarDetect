from Views import MainView
import threading
from functools import partial
from Models.ProfileManager import ProfileManager



class TrainController:
    def __init__(self, main_view: MainView, profile_manager: ProfileManager):
        self.train_tab = main_view.create_new_tab("Train")
        self.profile_manager = profile_manager
        self.main_view = main_view
        self.generate_training_set_button = self.main_view.add_button_to_tab(
            self.train_tab,
            "Generate",
            self.generate_button_event
        )

    def generate_button_event(self):
        print("GENERATE :D")
