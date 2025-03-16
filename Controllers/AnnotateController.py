from tkinter import simpledialog, colorchooser

from Views import MainView
from Models.ProfileManager import ProfileManager
import threading
from functools import partial
from Models.DataClasses.Classification import Classification

class AnnotateController:
    def __init__(self, main_view: MainView, profile_manager: ProfileManager):
        self.profile_manager = profile_manager
        self.annotate_tab = main_view.create_new_tab("Annotate")
        self.main_view = main_view

        self.dataset_combobox = self.main_view.add_dropdown_to_tab(
            self.annotate_tab,
            self.profile_manager.get_dataset_option_strings(),
            self.dataset_selected_event,
            "Dataset Options:",
            self.update_dataset_options)

        self.class_combobox = self.main_view.add_dropdown_to_tab(
            self.annotate_tab,
            [],
            self.class_selected_event,
            "Class Options:",
            self.update_class_options,
            ["New Class"],
            [self.create_new_class_event])

        self.image_combobox = self.main_view.add_dropdown_to_tab(
            self.annotate_tab,
            [],
            self.dummy,
            "Image Options:",
            self.dummy,
            ["Previous Image", "Next Image"],
            [self.dummy, self.dummy])

    def dataset_selected_event(self, event):
        self.profile_manager.update_selected_dataset(str(self.dataset_combobox.get()))

    def class_selected_event(self, event):
        pass

    def create_new_class_event(self):
        class_name = simpledialog.askstring(title="New Class", prompt="Enter class name:\t\t\n")
        class_id = len(self.profile_manager.active_profile.class_list)
        class_color = colorchooser.askcolor(title="Choose Color for class:\t\t\n")
        self.profile_manager.create_new_classification(
            class_name,
            class_id,
            class_color[1])

    def update_class_options(self):
        options = self.profile_manager.get_class_option_strings()
        if self.class_combobox is not None:
            self.class_combobox.config(values=options)

    def update_dataset_options(self):
        options = self.profile_manager.get_dataset_option_strings()
        if self.dataset_combobox is not None:
            self.dataset_combobox.config(values=options)


    def dummy(self):
        print("dummy")