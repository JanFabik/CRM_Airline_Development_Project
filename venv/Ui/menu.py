import tkinter as tk
import constants as const
from utils import record_count
import sqlite3
import settings

def menu(root, passengers_tab, book_flights_tab, style):
    my_menu = tk.Menu(root)
    root.config(menu=my_menu)

    options_menu = tk.Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Options", menu=options_menu)

    options_menu.add_command(label="Reset Passengers List",
                             command=lambda: passengers_tab.update_passengers_treeview(passengers_tab.passengers_tree, passengers_tab.tree_frame))

    options_menu.add_separator()

    options_menu.add_command(label="Primary Color",
                             command=lambda: settings.primary_color(passengers_tab.passengers_tree, book_flights_tab.scheduled_flights_tree, book_flights_tab.passengers_on_flight_tree))

    options_menu.add_command(label="Secondary Color",
                             command=lambda: settings.secondary_color(passengers_tab.passengers_tree, book_flights_tab.scheduled_flights_tree, book_flights_tab.passengers_on_flight_tree))

    options_menu.add_command(label="Highlight Color",
                             command=lambda: settings.treeview_highlight_color(style))

    options_menu.add_separator()

    options_menu.add_command(label="Reset Colors",
                             command=lambda: settings.reset_colors(style, passengers_tab.passengers_tree, book_flights_tab.scheduled_flights_tree, book_flights_tab.passengers_on_flight_tree))

    options_menu.add_separator()

    options_menu.add_command(label="Exit", command=root.quit)

    search_menu = tk.Menu(my_menu, tearoff=0)

    my_menu.add_cascade(label="Search", menu=search_menu)

    search_menu.add_command(label="Passenger ID", command=lambda: find_records(root, passengers_tab.passengers_tree, passengers_tab.tree_frame, "Passenger ID", "passenger_id"))

    search_menu.add_command(label="Email Address", command=lambda: find_records(root, passengers_tab.passengers_tree, passengers_tab.tree_frame, "Email Address", "email"))

# creates passenger search window from menu
def find_records(window, passengers_tree, passengers_tree_frame, search_name, search_column):
    search = tk.Toplevel(window)
    search.title("Find Records")
    search.geometry("400x200")
    search.iconbitmap(const.MAIN_ICON)

    search_frame = tk.LabelFrame(search, text=search_name)
    search_frame.pack(padx=10, pady=10)

    search_entry = tk.Entry(search_frame, font=("Calibri", 12))
    search_entry.pack(padx=20, pady=20)

    search_button = tk.Button(search, text="Search Records", command=lambda: (search_records(passengers_tree, passengers_tree_frame, search_entry.get(), search_column), search.destroy()))
    search_button.pack(padx=20, pady=20)

# search passengers from passenger search window
def search_records(passengers_tree, passengers_tree_frame, record_to_find, column_to_search):

    for record in passengers_tree.get_children():
        passengers_tree.delete(record)

    conn = sqlite3.connect(const.DATABASE_PATH)
    cur = conn.cursor()

    cur.execute(f"""SELECT passenger_id, first_name, last_name, email, street_number, street, city, zip, countries.country
                FROM passengers
                JOIN countries ON countries.country_id = passengers.country_id
                WHERE {column_to_search} LIKE ?
                ORDER BY passenger_id DESC
                """, (record_to_find,))
    records = cur.fetchall()
    conn.close()

    count = 0

    for record in records:
        if count % 2 == 0:
            passengers_tree.insert(parent="", index="end", iid=count, text="", values=(
                record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8]),
                                   tags=("evenrow",))
        else:
            passengers_tree.insert(parent="", index="end", iid=count, text="", values=(
                record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8]),
                                   tags=("oddrow",))

        count += 1

    record_count(tree=passengers_tree, frame=passengers_tree_frame)
