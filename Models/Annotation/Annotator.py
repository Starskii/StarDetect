from Utilities import utilities


class Annotator:
    def __init__(self):
        self.dataset_options = self.update_dataset_options()
        self.selected_option = None

    def set_selected_option(self, option_event):
        self.selected_option = option_event.widget.get()

    def update_dataset_options(self):
        self.dataset_options = utilities.get_captured_datasets("../Models/DataCollection/data")
