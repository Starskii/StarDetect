from Views import MainView
from Models.ProfileManager import ProfileManager
import threading
from Models.DataCollection import ObjectDataGatherer


class CollectController:
    def __init__(self, main_view: MainView, profile_manager: ProfileManager):
        self.profile_manager = profile_manager
        self.main_view = main_view
        self.collect_tab = main_view.create_new_tab("Collect")
        self.entry_dataset_name = main_view.add_input_to_tab(self.collect_tab, "Dataset name:")
        self.entry_number_of_images = main_view.add_input_to_tab(self.collect_tab, "Number of images:")
        self.entry_image_capture_delay = main_view.add_input_to_tab(self.collect_tab, "Image Capture Delay:")
        self.start_collection_button = main_view.add_button_to_tab(self.collect_tab, "Start collection",
                                                                   self.start_collection_event)
        self.progress_bar = None
        self.image_capture_count = 0
        self.image_capture_total = 0

    def image_gathered_callback(self):
        self.image_capture_count += 1
        self.main_view.update_progress_bar(self.progress_bar, self.image_capture_count / self.image_capture_total * 100)
        if self.image_capture_total == self.image_capture_count:
            MainView.enable_button(self.start_collection_button)

    def start_collection_event(self):
        # Perform validation to ensure # of image > 0
        if self.entry_number_of_images.get() == '':
            return
        if not self.entry_number_of_images.get().isdigit():
            return
        if int(self.entry_number_of_images.get()) < 1:
            return

        # Reset image capture count
        self.image_capture_count = 0
        self.image_capture_total = int(self.entry_number_of_images.get())

        # Disable button and show progress bar
        MainView.disable_button(self.start_collection_button)
        self.progress_bar = self.main_view.add_progress_bar_to_tab(self.collect_tab)

        # Start the dataset collection in a new thread
        threading.Thread(
            target=ObjectDataGatherer.gather_dataset,
            args=(
                self.entry_dataset_name.get(),
                int(self.entry_number_of_images.get()),
                float(self.entry_image_capture_delay.get()),
                self.image_gathered_callback,
                self.profile_manager),
            daemon=True
        ).start()