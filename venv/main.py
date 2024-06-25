from tkinter import ttk
import tkinter as tk
import settings
import constants as const
from Ui import menu, PassengerUI, BookFlightsUI, ScheduleFlightsUI


def configure_style():
    """Configure the style for the application."""
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    rowheight=25,
                    font=("Calibri", 12))
    style.map("Treeview", background=[("selected", settings.saved_highlight_color)])


def create_main_window():
    """Create and configure the main application window."""
    root = tk.Tk()
    root.title("Airline CRM")
    root.geometry("1500x700")
    root.option_add("*Font", "Calibri 12")
    root.iconbitmap(const.MAIN_ICON)
    return root


def create_scrollable_canvas(parent):
    """Create a scrollable canvas within the parent widget."""
    canvas = tk.Canvas(parent)
    scrollbar_y = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollbar_x = ttk.Scrollbar(parent, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")
    canvas.pack(fill="both", expand=True)
    return canvas


def add_scrollable_frame_to_canvas(canvas):
    """Add a scrollable frame inside the canvas."""
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    return frame


def add_tabs_to_notebook(notebook):
    """Add tabs to the notebook and return the main frames of each tab."""
    tabs = {}

    for tab_name in ['Passengers', 'Book Flights', 'Schedule Flights']:
        tab = tk.Frame(notebook)
        notebook.add(tab, text=tab_name)

        # Create a scrollable canvas in each tab
        canvas = create_scrollable_canvas(tab)
        frame = add_scrollable_frame_to_canvas(canvas)

        tabs[tab_name] = frame

    return tabs


def main():
    root = create_main_window()
    configure_style()

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=1)

    tabs = add_tabs_to_notebook(notebook)

    passengers_tab = PassengerUI(tabs['Passengers'])
    book_flights_tab = BookFlightsUI(tabs['Book Flights'])
    schedule_flights_tab = ScheduleFlightsUI(tabs['Schedule Flights'])

    menu(root, passengers_tab, book_flights_tab, ttk.Style())

    root.mainloop()


if __name__ == "__main__":
    main()
