from Views import MainView
from HomeController import HomeController
from CollectController import CollectController
from AnnotateController import AnnotateController
from TrainController import TrainController
from InferenceController import InferenceController
from Models.ProfileManager import ProfileManager

class MainController:
    def __init__(self):
        # Initialize ProfileManager to manage data to and from disk
        self.profile_manager = ProfileManager()
        # Initialize View
        self.main_view = MainView.MainView("StarDetect", 480, 270)

        # Initialize controllers
        self.home_controller = HomeController(self.main_view, self.profile_manager)
        self.collect_controller = CollectController(self.main_view, self.profile_manager)
        self.annotate_controller = AnnotateController(self.main_view, self.profile_manager)
        self.train_controller = TrainController(self.main_view, self.profile_manager)
        self.inference_controller = InferenceController(self.main_view, self.profile_manager)

        # Start UI
        self.main_view.start()


main_controller = MainController()
