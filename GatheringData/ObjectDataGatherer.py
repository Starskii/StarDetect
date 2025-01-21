from PIL import ImageGrab
import time
from Utilities import utilities


def gather_dataset(dataset_name: str, number_of_images: int, object_height_px: int, object_width_px: int,
                   image_capture_delay: float, update_function):
    print("Starting")
    directory_path = f'./GatheringData/data/{dataset_name}'
    directory_path = utilities.create_directory(directory_path)
    for image_index in range(number_of_images):
        start = time.time()
        while start + image_capture_delay > time.time():
            pass
        image = ImageGrab.grab()
        image.save(f'{directory_path}/{image_index}.png')
        update_function(f'{directory_path}/{image_index}.png')