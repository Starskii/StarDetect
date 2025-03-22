from tkinter import simpledialog, colorchooser
from PIL import Image, ImageTk

from Views import MainView
from Models.ProfileManager import ProfileManager
import threading
from functools import partial
from Models.DataClasses.Classification import Classification
import os


class AnnotateController:
    def __init__(self, main_view: MainView, profile_manager: ProfileManager):
        # When classes are selected
        self.first_point = None
        self.second_point = None

        self.profile_manager = profile_manager
        self.annotate_tab = main_view.create_new_tab("Annotate")
        self.main_view = main_view

        self.dataset_combobox = self.main_view.add_dropdown_to_tab(
            self.annotate_tab,
            self.update_dataset_options,
            self.dataset_selected_event,
            "Dataset Options:",
            self.update_dataset_options)

        self.class_combobox = self.main_view.add_dropdown_to_tab(
            self.annotate_tab,
            self.update_class_options,
            self.class_selected_event,
            "Class Options:",
            self.update_class_options,
            ["New Class"],
            [self.create_new_class_event])

        self.image_combobox = self.main_view.add_dropdown_to_tab(
            self.annotate_tab,
            self.update_image_options,
            self.image_selected_event,
            "Image Options:",
            self.update_image_options,
            ["Previous Image", "Next Image"],
            [self.prev_image_event, self.next_image_event])

        self.canvas = self.main_view.add_canvas_to_tab(self.annotate_tab, self.canvas_clicked_event)

        self.cancel_button = self.main_view.add_button_to_tab(self.annotate_tab, 
                                                              "Cancel", 
                                                              self.cancel_action_event)
        
        self.undo_button = self.main_view.add_button_to_tab(self.annotate_tab, 
                                                              "Undo", 
                                                              self.undo_action_event)

        # Add signal listeners
        # Profile Changed
        self.profile_manager.create_state_change_listener(profile_manager.EventType.PROFILE_CHANGED,
                                                          self.clear_dataset_combobox)
        self.profile_manager.create_state_change_listener(profile_manager.EventType.PROFILE_CHANGED,
                                                          self.clear_class_combobox)
        self.profile_manager.create_state_change_listener(profile_manager.EventType.PROFILE_CHANGED,
                                                          self.clear_image_combobox)
        self.profile_manager.create_state_change_listener(profile_manager.EventType.PROFILE_CHANGED,
                                                          self.clear_canvas)

        # Dataset changed
        self.profile_manager.create_state_change_listener(profile_manager.EventType.DATASET_CHANGED,
                                                          self.clear_image_combobox)
        self.profile_manager.create_state_change_listener(profile_manager.EventType.DATASET_CHANGED,
                                                          self.clear_image_combobox)
        self.profile_manager.create_state_change_listener(profile_manager.EventType.DATASET_CHANGED,
                                                          self.clear_canvas)

        # Image Changed
        self.profile_manager.create_state_change_listener(profile_manager.EventType.IMAGE_CHANGED,
                                                          self.update_canvas_image_event)

    def dataset_selected_event(self, event):
        self.profile_manager.update_selected_dataset(str(self.dataset_combobox.get()))
        self.signal_dataset_changed()

    def class_selected_event(self, event):
        # alert profilemanager
        self.profile_manager.update_selected_class(str(self.class_combobox.get()))
        self.signal_class_changed()

    def image_selected_event(self, event):
        # alert profilemanager
        self.profile_manager.update_selected_image(int(str(self.image_combobox.get()).split(".")[0]))
        self.signal_image_changed()

    def next_image_event(self):
        current_value = str(self.image_combobox.get())
        image_index = None
        # Guard against empty image list or None selected_dataset
        if self.profile_manager.selected_dataset is None:
            return
        if len(self.profile_manager.selected_dataset.annotated_images) == 0:
            return
        if current_value == '' or current_value is None:
            current_value = '0.png'
            image_index = 0
            self.image_combobox.set(current_value)
        else:
            image_index = (int(current_value.split('.')[0]) + 1) % len(self.profile_manager.get_image_option_strings())
            self.image_combobox.set(f'{str(image_index)}.png')
        self.profile_manager.update_selected_image(image_index)
        self.signal_image_changed()

    def prev_image_event(self):
        current_value = str(self.image_combobox.get())
        image_index = None
        # Guard against empty image list
        if self.profile_manager.selected_dataset is None:
            return
        if len(self.profile_manager.selected_dataset.annotated_images) == 0:
            return
        if current_value == '' or current_value is None:
            current_value = '0.png'
            image_index = 0
            self.image_combobox.set(current_value)
        else:
            image_index = (int(current_value.split('.')[0]) - 1) % len(self.profile_manager.get_image_option_strings())
            self.image_combobox.set(f'{str(image_index)}.png')
        self.profile_manager.update_selected_image(image_index)
        self.signal_image_changed()

    def clear_dataset_combobox(self):
        self.dataset_combobox.set("")
        self.profile_manager.update_selected_dataset("")
        self.signal_dataset_changed()

    def clear_class_combobox(self):
        self.class_combobox.set("")
        self.profile_manager.update_selected_class("")
        self.signal_class_changed()

    def clear_image_combobox(self):
        self.image_combobox.set("")
        self.profile_manager.update_selected_image(None)
        self.signal_image_changed()

    def clear_canvas(self):
        self.canvas.delete("all")  # Removes all drawn elements from the canvas

    def create_new_class_event(self):
        class_name = simpledialog.askstring(title="New Class", prompt="Enter class name:\t\t\n")
        class_id = len(self.profile_manager.active_profile.class_list)
        class_color = colorchooser.askcolor(title="Choose Color for class:\t\t\n")
        self.profile_manager.create_new_classification(
            class_name,
            class_id,
            class_color[1])
        
    def cancel_action_event(self):
        self.first_point = None
        self.second_point = None

    def undo_action_event(self):
        self.profile_manager.remove_last_annotation()
        self.signal_image_changed()

    def update_class_options(self):
        options = self.profile_manager.get_class_option_strings()
        if self.class_combobox is not None:
            self.class_combobox.config(values=options)

    def update_dataset_options(self):
        options = self.profile_manager.get_dataset_option_strings()
        if self.dataset_combobox is not None:
            self.dataset_combobox.config(values=options)

    def update_image_options(self):
        options = self.profile_manager.get_image_option_strings()
        if self.image_combobox is not None:
            self.image_combobox.config(values=options)

    def update_canvas_image_event(self):
        # Guard against none image
        if self.profile_manager.selected_image is None:
            return
        image_path = self.profile_manager.selected_image.path

        # Get canvas dimensions
        canvas_width = self.main_view.canvas_size_width
        canvas_height = self.main_view.canvas_size_height

        # Open and resize the image
        img = Image.open(image_path)
        img = img.resize((canvas_width + 1, canvas_height + 1), Image.Resampling.LANCZOS)

        # Convert to a format tkinter can use
        img_tk = ImageTk.PhotoImage(img)

        # Display image on canvas
        self.canvas.create_image(1, 1, image=img_tk, anchor='nw')
        self.img_tk = img_tk

        # Draw annotations
        self.main_view.draw_annotations_on_canvas(self.canvas, self.profile_manager.selected_image.annotations)

    def signal_dataset_changed(self):
        self.profile_manager.signal_state_change_listener(self.profile_manager.EventType.DATASET_CHANGED)

    def signal_class_changed(self):
        self.profile_manager.signal_state_change_listener(self.profile_manager.EventType.CLASS_CHANGED)

    def signal_image_changed(self):
        self.profile_manager.signal_state_change_listener(self.profile_manager.EventType.IMAGE_CHANGED)

    def canvas_clicked_event(self, event):
        print(f"Clicked at: ({event.x}, {event.y})")
        if self.first_point is None:
            self.first_point = (event.x, event.y)
        else:
            self.second_point = (event.x, event.y)
            self.profile_manager.create_new_annotation(
                self.first_point,
                self.second_point,
                (self.main_view.canvas_size_width, self.main_view.canvas_size_height)
            )
            self.cancel_action_event()
            self.signal_image_changed()



