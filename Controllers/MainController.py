from Controllers.HomeController import HomeController
from Controllers.CollectController import CollectController
from Controllers.AnnotateController import AnnotateController
from Controllers.TrainController import TrainController
from Controllers.InferenceController import InferenceController
from Models.ProfileManager import ProfileManager
from Views.MainView import MainView

class MainController:
    def __init__(self):
        # Initialize ProfileManager to manage data to and from disk
        self.profile_manager = ProfileManager()
        # Initialize View
        self.main_view = MainView("StarDetect", 480, 540)

        # Initialize controllers
        self.home_controller = HomeController(self.main_view, self.profile_manager)
        self.collect_controller = CollectController(self.main_view, self.profile_manager)
        self.annotate_controller = AnnotateController(self.main_view, self.profile_manager)
        self.train_controller = TrainController(self.main_view, self.profile_manager)
        self.inference_controller = InferenceController(self.main_view, self.profile_manager)

        # Start UI
        self.main_view.start()
