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
    dataset = profile_manager.create_new_image_collection(dataset_name)
    for image_index in range(number_of_images):
        start = time.time()
        while start + image_capture_delay > time.time():
            pass
        image = ImageGrab.grab()
        image.save(f'{directory_path}/{image_index}.png')
        update_function()
        # Create image JSON object and store it in the correct spot in the current_active_profile
        """
        TODO: This should probably be done in the profile manager somehow. Also, the saving of data could be
        optimized some way by either batching these together at the end or by using some producer consumer type 
        architecture so taking new images is not delayed by io processes.  
        """
        dataset.annotated_images.append(AnnotatedImage(f'{directory_path}/{image_index}.png', image.width, image.height, []))
    profile_manager.update_profile_json()
