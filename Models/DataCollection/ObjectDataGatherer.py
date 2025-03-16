from PIL import ImageGrab
import time
from Utilities import utilities
from typing import Callable
from Models.DataClasses.AnnotatedImage import AnnotatedImage
from Models.ProfileManager import ProfileManager


def gather_dataset(dataset_name: str, number_of_images: int, image_capture_delay: float, update_function, profile_manager: ProfileManager):
    directory_path = f'./PersistedData/ImageSets/{profile_manager.active_profile.profile_name}/{dataset_name}'
    directory_path = utilities.create_directory(directory_path)
    dataset_name = directory_path.split('/')[-1]
    dataset = profile_manager.create_image_collection(dataset_name)
    for image_index in range(number_of_images):
        start = time.time()
        while start + image_capture_delay > time.time():
            pass
        image = ImageGrab.grab()
        image.save(f'{directory_path}/{image_index}.png')
        update_function(f'{directory_path}/{image_index}.png')
        # Create image JSON object and store it in the correct spot in the current_active_profile
        dataset.annotated_images.append(AnnotatedImage(f'{directory_path}/{image_index}', image.width, image.height, []))
    profile_manager.profile_change_event_handler()
