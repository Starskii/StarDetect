from Views import MainView
from tkinter import simpledialog
from Models.ProfileManager import ProfileManager
import threading
from functools import partial


class HomeController:
    def __init__(self, main_view: MainView, profile_manager: ProfileManager):
        self.profile_manager = profile_manager
        self.home_tab = main_view.create_new_tab("Home")
        self.main_view = main_view
        self.profile_combobox = self.main_view.add_dropdown_to_tab(
            self.home_tab,
            [],
            self.profile_selected_event,
            "Select Profile:",
            self.retrieve_profiles_event,
            ["New Profile", "Delete Profile"],
            [self.create_new_profile_event, self.delete_profile_event])

    def delete_profile_event(self):
        self.profile_manager.delete_active_profile()
        self.profile_combobox.set('')

    def create_new_profile_event(self):
        profile_name = simpledialog.askstring(title="New Profile", prompt="Enter profile name:\t\t\n")
        if len(profile_name) < 1:
            return
        self.profile_manager.create_new_profile(profile_name)

    def retrieve_profiles_event(self):
        profiles = self.profile_manager.get_profiles()
        profile_options = []
        for profile in profiles:
            profile_options.append(profile.profile_name)
        if self.profile_combobox is not None:
            self.profile_combobox.config(values=profile_options)

    def profile_selected_event(self, event):
        self.profile_manager.set_active_profile(self.profile_combobox.current())
        self.profile_manager.signal_state_change_listener(self.profile_manager.EventType.PROFILE_CHANGED)

    def update_profile_options(self):
        self.annotator.update_dataset_options()
        if self.dataset_combobox is not None:
            self.dataset_combobox.config(values=self.annotator.dataset_options)
