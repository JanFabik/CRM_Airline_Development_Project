import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import sqlite3
import constants as const
from PIL import Image, ImageTk
from datetime import datetime


def popup_message_1(window, message_title, message_text, button_text, image_filename, command=None):
    message_window = tk.Toplevel(window)
    message_window.title(message_title)
    message_window.iconbitmap(const.MAIN_ICON)

    window_width = 400
    window_height = 240
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2
    message_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    message_label = tk.Label(message_window, text=message_text)
    message_label.pack(padx=20, pady=20)

    sign_image = tk.PhotoImage(file=image_filename)

    sign_image_label = tk.Label(message_window, image=sign_image)
    sign_image_label.image = sign_image
    sign_image_label.pack()

    if command is None:
        command = lambda: message_window.destroy()

    button = tk.Button(message_window, text=button_text, command= command, padx=30)
    button.pack(pady=20)

    return message_window


def popup_message_2(window, message_title, message_text, button_1_text, button_2_text, image_filename, command_1=None, command_2=None):
    message_window = tk.Toplevel(window)
    message_window.title(message_title)
    message_window.iconbitmap(const.MAIN_ICON)

    window_width = 400
    window_height = 240
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2
    message_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    message_label = tk.Label(message_window, text=message_text)
    message_label.pack(padx=20, pady=20)

    sign_image = tk.PhotoImage(file=image_filename)

    sign_image_label = tk.Label(message_window, image=sign_image)
    sign_image_label.image = sign_image
    sign_image_label.pack()

    command_1 = command_1 or (lambda: message_window.destroy())
    command_2 = command_2 or (lambda: message_window.destroy())

    button_1 = tk.Button(message_window, text=button_1_text, command= command_1, padx=30)
    button_1.pack(side=tk.LEFT, padx=40, pady=20)

    button_2 = tk.Button(message_window, text=button_2_text, command=command_2, padx=30)
    button_2.pack(side=tk.RIGHT, padx=40, pady=20)

    return message_window


def clear_entries(window):
    for widget in window.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.config(state="normal")
            widget.delete(0, "end")


def record_count(tree, frame):
    """
    Display number of records present in a specific treeview.

    Parameters:
    tree (tkinter.Treeview): The treeview widget instance whose records are counted.
    frame (tkinter.Frame): The frame in which the record count label is displayed.

    Returns:
    None
    """
    existing_label = tree.winfo_children()
    for widget in existing_label:
        if isinstance(widget, tk.Label) and widget.winfo_name() == "record_count_label":
            widget.destroy()

    number_of_records = len(tree.get_children())

    record_count_label = tk.Label(frame, text=f"Number of Records: {number_of_records}", name="record_count_label",
                               font=("Calibri 11"))
    record_count_label.pack(anchor=tk.E)


def update_treeview(treeview, data):
    """
    Updates a treeview with the provided data.

    Parameters:
    treeview (tkinter.ttk.Treeview): Treeview widget instance to update.
    data (list of tuples): Data to populate in the treeview.

    Returns:
    None
    """
    for record in treeview.get_children():
        treeview.delete(record)

    for count, record in enumerate(data):
        tag = "evenrow" if count % 2 == 0 else "oddrow"
        treeview.insert("", "end", iid=count, text="", values=record, tags=(tag,))


class AutofillDropdown:
    def __init__(self, entry_parent, options_list_parent, row, column, width, options, padx=None, pady=None, sticky=None):
        self.entry_parent = entry_parent
        self.options_list_parent = options_list_parent
        self.row = row
        self.column = column
        self.width = width
        self.options = options
        self.padx = padx
        self.pady = pady
        self.sticky = sticky
        self.dropdown_id = None
        self.setup_widget()

    def setup_widget(self):
        # Create a frame for the widgets
        self.wrapper = tk.Frame(self.entry_parent)
        self.wrapper.grid(row=self.row, column=self.column, padx=self.padx, pady=self.pady, sticky=self.sticky)

        # Create a text widget for the entry field
        self.entry = tk.Entry(self.wrapper, width=self.width)
        self.entry.pack(side=tk.LEFT)
        self.entry.bind("<KeyRelease>", self.on_entry_key)
        self.entry.bind("<FocusIn>", self.show_dropdown)

        # Dropdown icon/button
        self.icon = ImageTk.PhotoImage(Image.open(const.DROP_DOWN_ICON).resize((16, 16)))
        tk.Button(self.wrapper, image=self.icon, command=self.show_dropdown).pack(side=tk.LEFT)

        # Create a Listbox widget for the dropdown menu
        self.listbox = tk.Listbox(self.options_list_parent, height=5, width=30)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.listbox.bind("<MouseWheel>", self.on_mouse_wheel)
        for option in self.options:
            self.listbox.insert(tk.END, option)

    def on_entry_key(self, event):
        typed_value = event.widget.get().strip().lower()
        if not typed_value:
            # If the entry is empty, display all options
            self.listbox.delete(0, tk.END)
            for option in self.options:
                self.listbox.insert(tk.END, option)
        else:
            # Filter options based on the typed value
            self.listbox.delete(0, tk.END)
            filtered_options = [option for option in self.options if option.lower().startswith(typed_value)]
            for option in filtered_options:
                self.listbox.insert(tk.END, option)
        self.show_dropdown()

    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_option = self.listbox.get(selected_index)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selected_option)

    def show_dropdown(self, event=None):
        self.listbox.place(in_=self.entry, x=0, rely=1, relwidth=1.0, anchor="nw")
        self.listbox.lift()

        # Show dropdown for 2 seconds
        if self.dropdown_id: # Cancel any old events
            self.listbox.after_cancel(self.dropdown_id)
        self.dropdown_id = self.listbox.after(2000, self.hide_dropdown)

    def hide_dropdown(self):
        self.listbox.place_forget()

    def on_mouse_wheel(self, event):
        # Show dropdown for 2 seconds
        if self.dropdown_id: # Cancel any old events
            self.listbox.after_cancel(self.dropdown_id)
        self.dropdown_id = self.listbox.after(2000, self.hide_dropdown)

    def get(self):
        return self.entry.get()

    def insert(self, index, value):
        self.entry.insert(index, value)

    def delete(self, first, last):
        self.entry.delete(first, last)

    def config(self, state):
        self.entry.config(state=state)


class TimePicker(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Variables to hold time values
        self.hour_var = tk.StringVar(value='12')
        self.minute_var = tk.StringVar(value='00')

        # Spinbox for hours
        self.hour_spinbox = ttk.Spinbox(self, from_=0, to=23, wrap=True, textvariable=self.hour_var, width=2, font=("Calibri", 12))
        self.hour_spinbox.grid(row=0, column=0)

        # Label for separator
        tk.Label(self, text=":", font=('Arial', 20)).grid(row=0, column=1)

        # Spinbox for minutes
        self.minute_spinbox = ttk.Spinbox(self, from_=0, to=59, wrap=True, textvariable=self.minute_var, format='%02.0f', width=2, font=("Calibri", 12))
        self.minute_spinbox.grid(row=0, column=2)

    def get_time(self):
        return f"{self.hour_var.get()}:{self.minute_var.get()}"


class DatePickerEntry(tk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Button-1>', self.show_calendar)
        self.calendar = None

    def show_calendar(self, event=None):
        if self.calendar:
            return

        self.calendar_win = tk.Toplevel(self)
        self.calendar_win.wm_overrideredirect(True)

        # Get today's date
        today = datetime.today()

        # Create a Calendar widget with today's date
        self.calendar = Calendar(self.calendar_win, selectmode='day',
                                 year=today.year, month=today.month, day=today.day)
        self.calendar.pack(padx=10, pady=10)
        self.calendar.bind("<<CalendarSelected>>", self.on_date_selected)
        self.position_calendar()

    def on_date_selected(self, event=None):
        self.insert(0, self.calendar.selection_get())
        self.calendar_win.destroy()
        self.calendar = None

    def position_calendar(self):
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        self.calendar_win.geometry(f'+{x}+{y}')

    def insert(self, index, string):
        # Clear the existing value
        self.delete(0, tk.END)
        # Insert the new value
        super().insert(index, string)