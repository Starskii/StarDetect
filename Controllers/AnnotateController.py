from Views import MainView
from Models.ProfileManager import ProfileManager
import threading
from functools import partial
from Models.Annotation.Annotator import Annotator


class AnnotateController:
    def __init__(self, main_view: MainView, profile_manager: ProfileManager):
        self.profile_manager = ProfileManager()
        self.annotator = Annotator()
        self.annotate_tab = main_view.create_new_tab("Annotate")
        self.main_view = main_view

        self.dataset_combobox = self.main_view.add_dropdown_to_tab(
            self.annotate_tab,
            self.annotator.dataset_options,
            self.annotator.set_selected_option,
            "Dataset Options:",
            self.update_dataset_options)

        self.class_combobox = self.main_view.add_dropdown_to_tab(
            self.annotate_tab,
            [],
            self.dummy,
            "Class Options:",
            self.dummy,
            ["New Class"],
            [self.dummy])

        self.class_combobox = self.main_view.add_dropdown_to_tab(
            self.annotate_tab,
            [],
            self.dummy,
            "Image Options:",
            self.dummy,
            ["Previous Image", "Next Image"],
            [self.dummy, self.dummy])

    def update_dataset_options(self):
        self.annotator.update_dataset_options()
        if self.dataset_combobox is not None:
            self.dataset_combobox.config(values=self.annotator.dataset_options)

    def dummy(self):
        print("dummy")