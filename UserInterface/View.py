import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


# Function that will be triggered when the "Start Collection" button is clicked
def start_collection():
    object_height = entry_height.get()
    object_width = entry_width.get()

    # You can add your dataset collection logic here
    print(f"Starting data collection with object height: {object_height} and width: {object_width}")


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

# Create and place the "Start Collection" button
start_button = tk.Button(gather_dataset_tab, text="Start Collection", command=start_collection)
start_button.pack(pady=10)

# Create a canvas to display the latest screenshot
canvas = tk.Canvas(gather_dataset_tab, width=720, height=480)
canvas.pack(pady=20)

# Initial placeholder image
initial_image = Image.new('RGB', (1080, 1920), color='gray')  # Placeholder image (gray)
initial_image_tk = ImageTk.PhotoImage(initial_image)
image_on_canvas = canvas.create_image(0, 0, anchor=tk.NW, image=initial_image_tk)

# Pack the notebook into the main window
notebook.pack(expand=True, fill="both")

# Start the main loop
root.mainloop()
