import random
from Views import MainView
import threading
from functools import partial
from Models.ProfileManager import ProfileManager
from Utilities import utilities
import yaml
from typing import List, Tuple, Optional
from Models.DataClasses.AnnotatedImage import AnnotatedImage


class TrainController:
    def __init__(self, main_view: MainView, profile_manager: ProfileManager):
        self.train_tab = main_view.create_new_tab("Train")
        self.profile_manager = profile_manager
        self.main_view = main_view
        self.generate_training_set_button = self.main_view.add_button_to_tab(
            self.train_tab,
            "Generate",
            self.generate_button_event
        )

    def get_image_list(self) -> List[AnnotatedImage]:
        path_list = []
        for dataset in self.profile_manager.active_profile.dataset_list:
            for image in dataset.annotated_images:
                path_list.append(image)
        return path_list

    def split_sets(self, image_list: List[AnnotatedImage], validation_percentage: float) \
            -> Tuple[List[AnnotatedImage], List[AnnotatedImage]]:
        if not 0 <= validation_percentage <= 1:
            raise ValueError("validation_percentage must be between 0 and 1")

        shuffled_images = image_list[:]
        random.shuffle(shuffled_images)

        split_index = int(len(shuffled_images) * (1 - validation_percentage))
        training_set = shuffled_images[:split_index]
        validation_set = shuffled_images[split_index:]
        return training_set, validation_set

    def generate_button_event(self):
        directory_path = utilities.create_directory(
            f'./TrainingSets/{self.profile_manager.active_profile.profile_name}')
        training_set, validation_set = self.split_sets(self.get_image_list(), .1)
        class_names_dictionary = {}
        for classification in self.profile_manager.active_profile.class_list:
            class_names_dictionary[classification.classification_id] = classification.classification_name
        data = {
            'path': directory_path,
            'train': [image.path for image in training_set],
            'val': [image.path for image in validation_set],
            'names': class_names_dictionary
        }
        with open(f'{directory_path}/data.yaml', 'w') as file:
            yaml.dump(data, file)
