from Views import MainView
from HomeController import HomeController
from CollectController import CollectController
from AnnotateController import AnnotateController
from TrainController import TrainController
from InferenceController import InferenceController


class MainController:
    def __init__(self):
        # Initialize View
        self.main_view = MainView.MainView("StarDetect", 1920, 1080)

        # Initialize controllers
        self.home_controller = HomeController(self.main_view)
        self.collect_controller = CollectController(self.main_view)
        self.annotate_controller = AnnotateController(self.main_view)
        self.train_controller = TrainController(self.main_view)
        self.inference_controller = InferenceController(self.main_view)

        # Start UI
        self.main_view.start()


main_controller = MainController()
