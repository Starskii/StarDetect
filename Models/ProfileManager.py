from Models.DataClasses.Profile import Profile
from dacite import from_dict
from dataclasses import asdict
import os
import json

class ProfileManager:
    def __init__(self):
        self.active_profile = None
        self.profiles = []

    def update_profiles(self):
        updated_profiles = self.get_profiles()
        self.profiles = updated_profiles

    def get_profiles(self) -> [Profile]:
        updated_profiles = []
        with open('../PersistedData/profiles.json', 'r') as profiles_file:
            profiles_dict = json.load(profiles_file)
            for profile in profiles_dict:
                updated_profiles.append(from_dict(Profile, profile))
        return updated_profiles

    def set_active_profile(self, active_profile_index: int):
        self.update_profiles()
        self.active_profile = self.profiles[active_profile_index]

    def create_new_profile(self, profile_name):
        new_profile = Profile(profile_name, [], [])
        self.update_profiles()
        self.profiles.append(new_profile)
        self.profile_change_event_handler()

    def profile_change_event_handler(self):
        with open('../PersistedData/profiles.json', 'w') as profiles_file:
            profiles_dict = [asdict(profile) for profile in self.profiles]
            json.dump(profiles_dict, profiles_file, indent=4)

    def delete_active_profile(self):
        if self.active_profile in self.profiles:
            self.profiles.remove(self.active_profile)
            self.profile_change_event_handler()
