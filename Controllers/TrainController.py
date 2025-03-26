import os
import random
from Views import MainView
import threading
from functools import partial
from Models.ProfileManager import ProfileManager
from Utilities import utilities
import yaml
from typing import List, Tuple, Optional
from Models.DataClasses.AnnotatedImage import AnnotatedImage
import shutil
from ultralytics import YOLO, SETTINGS


class TrainController:
    def __init__(self, main_view: MainView, profile_manager: ProfileManager):
        # Override settings.json
        SETTINGS.defaults['datasets_dir'] = os.getcwd()
        self.train_tab = main_view.create_new_tab("Train")
        self.profile_manager = profile_manager
        self.main_view = main_view

        self.entry_percent_validation = main_view.add_input_to_tab(self.train_tab, "Validation Split (0 <= x <= 1):")
        self.generate_training_set_button = self.main_view.add_button_to_tab(
            self.train_tab,
            "Generate Training Set",
            self.generate_button_event
        )

        self.training_data_set_combobox = self.main_view.add_dropdown_to_tab(
            self.train_tab,
            self.update_training_set_options,
            self.training_data_set_selected_event,
            "Training Set Options:",
            self.update_training_set_options,
            [],
            [])

        self.entry_number_of_epoches = main_view.add_input_to_tab(self.train_tab, "Number of Epochs:")

        self.train_button = main_view.add_button_to_tab(
            self.train_tab,
            "Train",
            self.train_button_event
        )

    def update_training_set_options(self):
        options = self.profile_manager.get_training_set_option_strings()
        if self.training_data_set_combobox is not None:
            self.training_data_set_combobox.config(values=options)

    def training_data_set_selected_event(self, event):
        print(event)
        self.profile_manager.update_selected_training_set(str(self.training_data_set_combobox.get()))
        self.signal_training_data_set_changed()

    def signal_training_data_set_changed(self):
        self.profile_manager.signal_state_change_listener(self.profile_manager.EventType.TRAINING_SET_CHANGED)

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
            f'./PersistedData/TrainingSets/{self.profile_manager.active_profile.profile_name}')
        images_path = utilities.create_directory(
            f'{directory_path}/images')
        images_train_path = utilities.create_directory(
            f'{images_path}/train')
        images_val_path = utilities.create_directory(
            f'{images_path}/val')

        labels_path = utilities.create_directory(
            f'{directory_path}/labels')
        labels_train_path = utilities.create_directory(
            f'{labels_path}/train')
        labels_val_path = utilities.create_directory(
            f'{labels_path}/val')
        training_set, validation_set = self.split_sets(self.get_image_list(), float(self.entry_percent_validation.get()))

        # Setup training set directory
        training_set_count = 0
        for image in training_set:
            shutil.copy(image.path, f'{images_train_path}/{training_set_count}.png')
            with open(f'{labels_train_path}/{training_set_count}.txt', 'w') as label_file:
                data_string = ''
                for annotation in image.annotations:
                    data_string += f'{annotation.class_identifier} {annotation.center_x} {annotation.center_y} {annotation.width} {annotation.height}\n'
                label_file.write(data_string)
            training_set_count += 1

            # Setup val set directory
            val_set_count = 0
            for image in validation_set:
                shutil.copy(image.path, f'{images_val_path}/{val_set_count}.png')
                with open(f'{labels_val_path}/{val_set_count}.txt', 'w') as label_file:
                    data_string = ''
                    for annotation in image.annotations:
                        data_string += f'{annotation.class_identifier} {annotation.center_x} {annotation.center_y} {annotation.width} {annotation.height}\n'
                    label_file.write(data_string)
                val_set_count += 1

        self.profile_manager.create_new_training_set(
            name=directory_path.split("/")[-1],
            path=directory_path,
            number_of_images_training=training_set_count,
            number_of_images_validation=val_set_count,
            validation_split_percentage=float(self.entry_percent_validation.get())
        )
        self.signal_training_data_set_changed()

        class_names_dictionary = {}
        for classification in self.profile_manager.active_profile.class_list:
            class_names_dictionary[classification.classification_id] = classification.classification_name
        data = {
            'path': directory_path,
            'train': 'images/train',
            'val': 'images/val',
            'names': class_names_dictionary
        }
        with open(f'{directory_path}/data.yaml', 'w') as file:
            yaml.dump(data, file)

    def train_button_event(self):
        print(self.profile_manager.selected_training_set)

        model = YOLO('yolo11n.pt')

        # Define the custom save directory
        save_dir = f'{self.profile_manager.selected_training_set.training_set_path}/trained_models'

        # Train the model and specify the project directory
        results = model.train(
            data=f'{self.profile_manager.selected_training_set.training_set_path}/data.yaml',
            epochs=int(self.entry_number_of_epoches.get()),
            imgsz=640,
            project=save_dir,  # Specify the directory to save the trained model
            name="yolo_model"  # Name of the experiment
        )



