import tkinter as tk
from tkinter import ttk
from typing import Callable


class MainView:
    def __init__(self, title: str, width_px: int, height_px: int):
        # Create root of GUI
        self.root = tk.Tk()
        self.root.title(f'{title}')
        self.root.geometry(f'{width_px}x{height_px}')

        # Create TabContainer
        self.tab_container = ttk.Notebook(self.root)
        self.tab_container.pack(expand=True, fill="both")

        # Create tab row counter dictionary
        # Keys are tab_identifiers and values are the int count of rows
        self.tab_row_counter = {}

    def create_new_tab(self, tab_title: str) -> ttk.Frame:
        new_tab = ttk.Frame(self.tab_container)
        self.tab_container.add(new_tab, text=f'{tab_title}')
        self.tab_row_counter[new_tab] = 0
        return new_tab

    def add_input_to_tab(self, tab_identifier: ttk.Frame, label_text: str = None) -> tk.Entry:
        if label_text is not None:
            new_label = tk.Label(tab_identifier, text=f'{label_text}')
            new_label.grid(row=self.tab_row_counter[tab_identifier], column=0, padx=10, pady=5, sticky='w')
        new_entry = tk.Entry(tab_identifier)
        new_entry.grid(row=self.tab_row_counter[tab_identifier], column=1, padx=10, pady=5)
        self.tab_row_counter[tab_identifier] += 1
        return new_entry

    def add_button_to_tab(self, tab_identifier: ttk.Frame, button_text: str, action: Callable) -> tk.Button:
        new_button = tk.Button(tab_identifier, text=f'{button_text}', command=action)
        new_button.grid(row=self.tab_row_counter[tab_identifier], column=0, padx=10, pady=5)
        self.tab_row_counter[tab_identifier] += 1
        return new_button

    def add_progress_bar_to_tab(self, tab_identifier: ttk.Frame) -> ttk.Progressbar:
        new_progress_bar = ttk.Progressbar(tab_identifier, length=100, mode='determinate')
        new_progress_bar["value"] = 0
        new_progress_bar.grid(row=self.tab_row_counter[tab_identifier], column=0, padx=10, pady=5)
        self.tab_row_counter[tab_identifier] += 1
        return new_progress_bar

    def update_progress_bar(self, progress_bar_identifier: ttk.Progressbar, value: float):
        progress_bar_identifier["value"] = value
        self.root.update_idletasks()
        if value >= 100:
            progress_bar_identifier.grid_forget()

    def add_dropdown_to_tab(self,
                            tab_identifier: ttk.Frame,
                            options: [str],
                            option_selected_callback: Callable,
                            label_text: str = None,
                            dropdown_event_callback: Callable = None,
                            button_text: [str] = None,
                            button_event_handler: [Callable] = None) -> ttk.Combobox:
        column_counter = 0

        if label_text is not None:
            new_label = tk.Label(tab_identifier, text=f'{label_text}')
            new_label.grid(row=self.tab_row_counter[tab_identifier], column=column_counter, padx=10, pady=5)
            column_counter += 1

        new_dropdown = ttk.Combobox(tab_identifier, values=options, state="readonly",
                                    postcommand=dropdown_event_callback)
        new_dropdown.bind("<<ComboboxSelected>>", option_selected_callback)
        new_dropdown.grid(row=self.tab_row_counter[tab_identifier], column=column_counter, padx=10, pady=5)
        column_counter += 1
        if button_text is not None:
            if len(button_text) > 0:
                for index in range(len(button_text)):
                    new_button = tk.Button(tab_identifier, text=f'{button_text[index]}', command=button_event_handler[index])
                    new_button.grid(row=self.tab_row_counter[tab_identifier], column=column_counter, padx=10, pady=5)
                    column_counter += 1

        self.tab_row_counter[tab_identifier] += 1
        return new_dropdown

    def start(self):
        self.root.mainloop()


def disable_button(button_identifier: tk.Button):
    button_identifier.config(state="disabled")


def enable_button(button_identifier: tk.Button):
    button_identifier.config(state="active")


def remove_element(element_identifier: any):
    element_identifier.grid_forget()
