from Models.DataClasses.Classification import Classification
from Models.DataClasses.Profile import Profile
from dacite import from_dict
from dataclasses import asdict
from Models.DataClasses.Dataset import Dataset
import os
from typing import Optional
import json

class ProfileManager:
    def __init__(self):
        self.active_profile: Profile = None
        self.profiles = []
        self.selected_dataset: Optional[Dataset] = None

# Create methods are called to create a new data object and store it in the profile obj which will be written to JSON.
# Create methods call the profile_change_event_handler() to store the updated profile object to persisted JSON file.
    def create_new_profile(self, profile_name):
        new_profile = Profile(profile_name, [], [])
        self.update_profiles()
        self.profiles.append(new_profile)
        self.profile_change_event_handler()

    def create_image_collection(self, collection_name: str) -> Dataset:
        dataset = Dataset(collection_name, [])
        self.active_profile.dataset_list.append(dataset)
        self.profile_change_event_handler()
        return dataset

    def create_new_classification(self, classification_name: str,
                                  classification_id: int,
                                  classification_color: str):
        new_class = Classification(classification_name, classification_id, classification_color)
        self.active_profile.class_list.append(new_class)
        self.profile_change_event_handler()

    def update_profiles(self):
        updated_profiles = self.get_profiles()
        self.profiles = updated_profiles

    def get_profiles(self) -> [Profile]:
        updated_profiles = []
        with open('./PersistedData/profiles.json', 'r') as profiles_file:
            profiles_dict = json.load(profiles_file)
            for profile in profiles_dict:
                updated_profiles.append(from_dict(Profile, profile))
        return updated_profiles

    def set_active_profile(self, active_profile_index: int):
        self.update_profiles()
        self.active_profile = self.profiles[active_profile_index]

    def profile_change_event_handler(self):
        with open('./PersistedData/profiles.json', 'w') as profiles_file:
            profiles_dict = [asdict(profile) for profile in self.profiles]
            json.dump(profiles_dict, profiles_file, indent=4)

    def delete_active_profile(self):
        if self.active_profile in self.profiles:
            self.profiles.remove(self.active_profile)
            self.profile_change_event_handler()

    def get_dataset_option_strings(self) -> [str]:
        dataset_list = []
        if self.active_profile is None:
            return dataset_list
        for dataset in self.active_profile.dataset_list:
            dataset_list.append(dataset.dataset_name)
        return dataset_list

    def update_selected_dataset(self, dataset_name: str):
        for dataset in self.active_profile.dataset_list:
            if dataset.dataset_name == dataset_name:
                self.selected_dataset = dataset

    def get_class_option_strings(self) -> str:
        class_list = []
        if self.active_profile is None:
            return class_list
        for classification in self.active_profile.class_list:
            class_list.append(classification.classification_name)

