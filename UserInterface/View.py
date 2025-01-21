import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from GatheringData import ObjectDataGatherer
import threading

# Global variables
current_image_tk = None
canvas_image_id = None
progress_bar = None
start_button = None
capture_total = 0


# Function to update the image on the canvas
def update_image(image_path):
    global current_image_tk, canvas_image_id

    # Open the new image using PIL
    img = Image.open(image_path)
    img.thumbnail((854, 480))  # Resize image to fit the canvas size

    # Convert the image to a format Tkinter can handle
    current_image_tk = ImageTk.PhotoImage(img)

    # Update the canvas with the new image
    if canvas_image_id:
        canvas.itemconfig(canvas_image_id, image=current_image_tk)
    else:
        canvas_image_id = canvas.create_image(0, 0, anchor=tk.NW, image=current_image_tk)

    # Keep a reference to the image to prevent garbage collection
    canvas.image = current_image_tk

    current = int(image_path.split('/')[-1].split('.')[0]) + 1
    update_progress(current)


def update_progress(current):
    total = int(entry_number_of_images.get())
    progress_bar["value"] = (current / total) * 100  # Update progress bar value
    root.update_idletasks()  # Force the UI to update

    # If the process is complete, restore the start button and hide the progress bar
    if current == total:
        start_button.pack(pady=20)  # Repack the Start Collection button
        progress_bar.pack_forget()  # Remove the progress bar


# Function that will be triggered when the "Start Collection" button is clicked
def start_collection():
    # Perform validation to ensure # of image > 0
    if entry_number_of_images.get() == '':
        return
    if not entry_number_of_images.get().isdigit():
        return
    if int(entry_number_of_images.get()) < 1:
        return
    # Hide the Start Collection button and show the progress bar
    start_button.pack_forget()  # Remove the Start button
    progress_bar.pack(pady=20)  # Display progress bar

    # Start the dataset collection in a new thread
    threading.Thread(
        target=ObjectDataGatherer.gather_dataset,
        args=(
            entry_dataset_name.get(), int(entry_number_of_images.get()), int(entry_height.get()),
            int(entry_width.get()),
            0, update_image),
        daemon=True
    ).start()


# Create the main window
root = tk.Tk()
root.title("Starskii Bot")
root.geometry("1920x1080")  # Set window size

# Create a Notebook (tab container)
notebook = ttk.Notebook(root)

# Create the "Gather Dataset" tab
gather_dataset_tab = ttk.Frame(notebook)

# Add the "Gather Dataset" tab to the notebook
notebook.add(gather_dataset_tab, text="Gather Dataset")

# Create and place the "Dataset Name" label and entry field
label_dataset_name = tk.Label(gather_dataset_tab, text="Dataset name:")
label_dataset_name.pack(pady=(10, 0))  # Top padding, no bottom padding
entry_dataset_name = tk.Entry(gather_dataset_tab)
entry_dataset_name.pack(pady=5)

# Create and place the "Number of images" label and entry field
label_number_of_images = tk.Label(gather_dataset_tab, text="Number of images:")
label_number_of_images.pack(pady=(10, 0))  # Top padding, no bottom padding
entry_number_of_images = tk.Entry(gather_dataset_tab)
entry_number_of_images.pack(pady=5)

# Create and place the "Object Height" label and entry field
label_height = tk.Label(gather_dataset_tab, text="Object Height:")
label_height.pack(pady=(10, 0))  # Top padding, no bottom padding
entry_height = tk.Entry(gather_dataset_tab)
entry_height.pack(pady=5)

# Create and place the "Object Width" label and entry field
label_width = tk.Label(gather_dataset_tab, text="Object Width:")
label_width.pack(pady=(10, 0))  # Top padding, no bottom padding
entry_width = tk.Entry(gather_dataset_tab)
entry_width.pack(pady=5)

# Create a canvas to display the latest screenshot
canvas = tk.Canvas(gather_dataset_tab, width=854, height=480)
canvas.pack(pady=20)

# Initial placeholder image
initial_image = Image.new('RGB', (854, 480), color='gray')  # Placeholder image (gray)
initial_image_tk = ImageTk.PhotoImage(initial_image)
canvas.create_image(0, 0, anchor=tk.NW, image=initial_image_tk)

# Create and place the "Start Collection" button
start_button = tk.Button(gather_dataset_tab, text="Start Collection", command=start_collection)
start_button.pack(pady=10)

# Create a progress bar for the image capture process
progress_bar = ttk.Progressbar(gather_dataset_tab, length=300, mode='determinate')



# Pack the notebook into the main window
notebook.pack(expand=True, fill="both")

# Start the main loop
root.mainloop()
