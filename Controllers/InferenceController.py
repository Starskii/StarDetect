from Views import MainView
import threading
from functools import partial
from Models.ProfileManager import ProfileManager



class InferenceController:
    def __init__(self, main_view: MainView, profile_manager: ProfileManager):
        self.profile_manager = profile_manager
        self.inference_tab = main_view.create_new_tab("Inference")
