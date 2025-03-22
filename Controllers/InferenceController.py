from Views import MainView
import threading
from functools import partial
from Models.ProfileManager import ProfileManager
from PIL import Image, ImageTk
from ultralytics import YOLO
import pyautogui

class InferenceController:
    def __init__(self, main_view: MainView, profile_manager: ProfileManager):
        self.profile_manager = profile_manager
        self.inference_tab = main_view.create_new_tab("Inference")
        self.main_view = main_view
        # Add button "start inference"
        self.generate_training_set_button = self.main_view.add_button_to_tab(
            self.inference_tab,
            "Start",
            self.start_inference_button_event
        )
        # Add canvas
        self.canvas = self.main_view.add_canvas_to_tab(self.inference_tab)

    def start_inference_button_event(self):
        # Run inference in a separate thread to avoid freezing the UI
        threading.Thread(target=self.run_inference, daemon=True).start()

    def run_inference(self):
        # Take a screenshot
        screenshot = pyautogui.screenshot()

        # Save the screenshot temporarily
        screenshot_path = "./temp_screenshot.png"
        screenshot.save(screenshot_path)

        # Load YOLO model
        model = YOLO("./PersistedData/TrainingSets/example/trained_models/yolo_model/weights/best.pt")

        # Run inference on the screenshot
        results = model(screenshot_path)

        # Draw annotations on the image
        annotated_image = results[0].plot()  # YOLO outputs an annotated image

        # Save the annotated image
        annotated_image_path = "./temp_annotated.png"
        Image.fromarray(annotated_image).save(annotated_image_path)

        # Update the canvas with the annotated image
        self.update_canvas_image(annotated_image_path)

    def update_canvas_image(self, image_path):
        # Ensure UI updates happen on the main thread
        self.main_view.root.after(0, lambda: self._update_canvas(image_path))

    def _update_canvas(self, image_path):
        # Get canvas dimensions
        canvas_width = self.main_view.canvas_size_width
        canvas_height = self.main_view.canvas_size_height

        # Open and resize the image
        img = Image.open(image_path)
        img = img.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)

        # Convert to a format tkinter can use
        img_tk = ImageTk.PhotoImage(img)

        # Display image on canvas
        self.canvas.create_image(0, 0, image=img_tk, anchor='nw')
        self.img_tk = img_tk  # Prevent garbage collection


