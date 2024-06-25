import tkinter as tk
from tkinter import ttk
import re
import sqlite3
import constants as const
import utils
import settings

class PassengerUI:
    def __init__(self, master):
        self.master = master
        self.setup_ui()
        self.update_passengers_treeview(self.passengers_tree, self.tree_frame)

    def setup_ui(self):
        self.tree_frame = tk.LabelFrame(self.master, text="Passengers")
        self.tree_frame.pack(padx=20, pady=10, fill="x")

        # Setup Treeview
        self.tree_scroll = tk.Scrollbar(self.tree_frame, width=25)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.passengers_tree = ttk.Treeview(self.tree_frame, show="headings", selectmode="extended")
        self.passengers_tree["columns"] = ("Passenger ID", "First Name", "Last Name", "Email", "Street Number", "Street Name", "City", "ZIP Code", "Country")
        self.passengers_tree.pack(pady=10)

        self.passengers_tree.tag_configure("oddrow", background=settings.saved_secondary_color)  # "#EEF2FF"
        self.passengers_tree.tag_configure("evenrow", background=settings.saved_primary_color)

        self.tree_scroll.config(command=self.passengers_tree.yview)


        self.passengers_tree.column("#0", width=0, stretch=tk.NO)
        self.passengers_tree.column("Passenger ID", anchor=tk.W, width=120)
        self.passengers_tree.column("First Name", anchor=tk.W, width=140)
        self.passengers_tree.column("Last Name", anchor=tk.W, width=160)
        self.passengers_tree.column("Email", anchor=tk.W, width=240)
        self.passengers_tree.column("Street Number", anchor=tk.W, width=100)
        self.passengers_tree.column("Street Name", anchor=tk.W, width=140)
        self.passengers_tree.column("City", anchor=tk.W, width=140)
        self.passengers_tree.column("ZIP Code", anchor=tk.W, width=80)
        self.passengers_tree.column("Country", anchor=tk.W, width=240)

        self.passengers_tree.heading("#0", text="", anchor=tk.W)
        self.passengers_tree.heading("Passenger ID", text="Passenger ID", anchor=tk.W)
        self.passengers_tree.heading("First Name", text="First Name", anchor=tk.W)
        self.passengers_tree.heading("Last Name", text="Last Name", anchor=tk.W)
        self.passengers_tree.heading("Email", text="Email", anchor=tk.W)
        self.passengers_tree.heading("Street Number", text="Street Number", anchor=tk.W)
        self.passengers_tree.heading("Street Name", text="Street Name", anchor=tk.W)
        self.passengers_tree.heading("City", text="City", anchor=tk.W)
        self.passengers_tree.heading("ZIP Code", text="ZIP Code", anchor=tk.W)
        self.passengers_tree.heading("Country", text="Country", anchor=tk.W)


        # Bind the select event
        self.passengers_tree.bind("<ButtonRelease-1>", self.on_tree_select)

        # Data Entry Frame
        self.entry_frame = tk.LabelFrame(self.master, text="Passenger Detail")
        self.entry_frame.pack(fill="x", expand=1, padx=20)

        # Entries for passenger data
        self.passenger_id_label = tk.Label(self.entry_frame, text="Passenger ID")
        self.passenger_id_label.grid(row=0, column=0, padx=10, pady=10)
        self.passenger_id_entry = tk.Entry(self.entry_frame)
        self.passenger_id_entry.grid(row=0, column=1, padx=10, pady=10)

        self.email_label = tk.Label(self.entry_frame, text="Email")
        self.email_label.grid(row=0, column=2, padx=10, pady=10)
        self.email_entry = tk.Entry(self.entry_frame)
        self.email_entry.grid(row=0, column=3, padx=10, pady=10)

        self.fn_label = tk.Label(self.entry_frame, text="First Name")
        self.fn_label.grid(row=1, column=0, padx=10, pady=10)
        self.fn_entry = tk.Entry(self.entry_frame)
        self.fn_entry.grid(row=1, column=1, padx=10, pady=10)

        self.ln_label = tk.Label(self.entry_frame, text="Last Name")
        self.ln_label.grid(row=1, column=2, padx=10, pady=10)
        self.ln_entry = tk.Entry(self.entry_frame)
        self.ln_entry.grid(row=1, column=3, padx=10, pady=10)

        self.street_number_label = tk.Label(self.entry_frame, text="Street Number")
        self.street_number_label.grid(row=2, column=0, padx=10, pady=10)
        self.street_number_entry = tk.Entry(self.entry_frame)
        self.street_number_entry.grid(row=2, column=1, padx=10, pady=10)

        self.street_name_label = tk.Label(self.entry_frame, text="Street Name")
        self.street_name_label.grid(row=2, column=2, padx=10, pady=10)
        self.street_name_entry = tk.Entry(self.entry_frame)
        self.street_name_entry.grid(row=2, column=3, padx=10, pady=10)

        self.city_label = tk.Label(self.entry_frame, text="City")
        self.city_label.grid(row=3, column=0, padx=10, pady=10)
        self.city_entry = tk.Entry(self.entry_frame)
        self.city_entry.grid(row=3, column=1, padx=10, pady=10)

        self.zip_code_label = tk.Label(self.entry_frame, text="ZIP Code")
        self.zip_code_label.grid(row=3, column=2, padx=10, pady=10)
        self.zip_code_entry = tk.Entry(self.entry_frame)
        self.zip_code_entry.grid(row=3, column=3, padx=10, pady=10)

        self.country_label = tk.Label(self.entry_frame, text="Country")
        self.country_label.grid(row=4, column=0, padx=10, pady=10)
        # self.conn = sqlite3.connect(const.DATABASE_PATH)
        # self.cur = self.conn.cursor()
        # self.cur.execute("""SELECT country FROM countries""")
        # self.countries = [row[0] for row in self.cur.fetchall()]
        # self.conn.close()
        self.countries = const.countries_list()
        self.country_entry = utils.AutofillDropdown(entry_parent=self.entry_frame, options_list_parent=self.master, row=4, column=1, width=30, options=self.countries)
        # self.country_dropdown = ttk.Combobox(self.entry_frame, values=self.countries)
        # self.country_dropdown.grid(row=4, column=1)

        self.clear_button = tk.Button(self.entry_frame, text="Clear", padx=30,
                                     command=lambda:
                                     (utils.clear_entries(self.entry_frame),
                                      self.country_entry.config(state="normal"),
                                      self.country_entry.delete(0, "end"),
                                      self.number_of_flights_entry.config(state="readonly"),
                                      self.total_distance_entry.config(state="readonly"),
                                      self.avg_distance_entry.config(state="readonly"),
                                      self.total_amount_entry.config(state="readonly"),
                                      self.avg_ticket_cost_entry.config(state="readonly")
                                      ))
        self.clear_button.grid(row=4, column=3, padx=10, pady=10)

        self.search_button = tk.Button(self.entry_frame, text="Search", padx=20, command=lambda: self.search_passengers())
        self.search_button.grid(row=4, column=4, padx=10, pady=10)

        self.empty_column_label = tk.Label(self.entry_frame, text="")
        self.empty_column_label.grid(row=0, column=4, padx=30)

        self.number_of_flights_label = tk.Label(self.entry_frame, text="Number of Flights")
        self.number_of_flights_label.grid(row=0, column=5, padx=10, pady=10)
        self.number_of_flights_entry = tk.Entry(self.entry_frame, state="readonly")
        self.number_of_flights_entry.grid(row=0, column=6, padx=10, pady=10)

        self.total_distance_label = tk.Label(self.entry_frame, text="Total Distance")
        self.total_distance_label.grid(row=1, column=5, padx=10, pady=10)
        self.total_distance_entry = tk.Entry(self.entry_frame, state="readonly")
        self.total_distance_entry.grid(row=1, column=6, padx=10, pady=10)

        self.avg_distance_label = tk.Label(self.entry_frame, text="Avg Distance")
        self.avg_distance_label.grid(row=2, column=5, padx=10, pady=10)
        self.avg_distance_entry = tk.Entry(self.entry_frame, state="readonly")
        self.avg_distance_entry.grid(row=2, column=6, padx=10, pady=10)

        self.total_amount_label = tk.Label(self.entry_frame, text="Total Amount")
        self.total_amount_label.grid(row=1, column=7, padx=10, pady=10)
        self.total_amount_entry = tk.Entry(self.entry_frame, state="readonly")
        self.total_amount_entry.grid(row=1, column=8, padx=10, pady=10)

        self.avg_ticket_cost_label = tk.Label(self.entry_frame, text="Avg Ticket Cost")
        self.avg_ticket_cost_label.grid(row=2, column=7, padx=10, pady=10)
        self.avg_ticket_cost_entry = tk.Entry(self.entry_frame, state="readonly")
        self.avg_ticket_cost_entry.grid(row=2, column=8, padx=10, pady=10)

        # Button Frame
        self.button_frame = tk.LabelFrame(self.master, text="Command")
        self.button_frame.pack(fill=tk.X,  expand=1, padx=20, pady=10)
        for i in range(5):
            self.button_frame.columnconfigure(i, weight=1)

        # Buttons for operations
        self.new_passenger_button = tk.Button(self.button_frame, text="New Passenger", padx=10, command=self.new_passenger)
        self.new_passenger_button.grid(row=0, column=0, padx=10, pady=10)

        self.update_button = tk.Button(self.button_frame, text="Update Passenger", command=self.update_passenger)
        self.update_button.grid(row=0, column=1, padx=10, pady=10)

        self.delete_record_button = tk.Button(self.button_frame, text="Delete Passenger", command=self.delete_passenger)
        self.delete_record_button.grid(row=0, column=2, padx=10, pady=10)

        self.import_passengers_button = tk.Button(self.button_frame, text="Import .csv", padx=10)
        self.import_passengers_button.grid(row=0, column=3, padx=10, pady=10)

        self.export_passengers_button = tk.Button(self.button_frame, text="Export .csv", padx=10)
        self.export_passengers_button.grid(row=0, column=4, padx=10, pady=10)

    def on_tree_select(self, event):
        utils.clear_entries(self.entry_frame)
        self.country_entry.config(state="normal")
        self.country_entry.delete(0, "end")

        selected_item = self.passengers_tree.focus()
        values = self.passengers_tree.item(selected_item, "values")

        self.passenger_id_entry.insert(0, values[0])
        self.passenger_id_entry.config(state="readonly")
        self.fn_entry.insert(0, values[1])
        self.fn_entry.config(state="readonly")
        self.ln_entry.insert(0, values[2])
        self.ln_entry.config(state="readonly")
        self.email_entry.insert(0, values[3])
        self.email_entry.config(state="readonly")
        self.street_number_entry.insert(0, values[4])
        self.street_number_entry.config(state="readonly")
        self.street_name_entry.insert(0, values[5])
        self.street_name_entry.config(state="readonly")
        self.city_entry.insert(0, values[6])
        self.city_entry.config(state="readonly")
        self.zip_code_entry.insert(0, values[7])
        self.zip_code_entry.config(state="readonly")
        self.country_entry.insert(0, values[8])
        self.country_entry.config(state="readonly")

        self.conn = sqlite3.connect(const.DATABASE_PATH)
        self.cur = self.conn.cursor()
        self.cur.execute("""SELECT flights.flight_id, tickets.passenger_id FROM flights
                            JOIN ticket_flights ON flights.flight_id = ticket_flights.flight_id
                            JOIN tickets ON ticket_flights.ticket_no = tickets.ticket_no
                            WHERE tickets.passenger_id = ? AND status = 'Arrived'"""
                    , (values[0],))
        flights = len(self.cur.fetchall())

        self.number_of_flights_entry.insert(0, flights)
        self.number_of_flights_entry.config(state="readonly")

        self.cur.execute("""SELECT SUM(distance_km) AS total_distance FROM flights
                                JOIN ticket_flights ON flights.flight_id = ticket_flights.flight_id
                                JOIN tickets ON ticket_flights.ticket_no = tickets.ticket_no
                                JOIN distances ON flights.departure_airport = distances.airport_code_1
                                     AND flights.arrival_airport = distances.airport_code_2
                                WHERE tickets.passenger_id = ? AND status = 'Arrived'"""
                    , (values[0],))
        total_distance = self.cur.fetchone()

        if total_distance[0]:
            a = int(round(total_distance[0]))
        else:
            a = 0

        self.total_distance_entry.insert(0, a)
        self.total_distance_entry.config(state="readonly")

        if a != 0:
            avg_distance = round(a / flights, 2)
        else:
            avg_distance = 0
        self.avg_distance_entry.insert(0, avg_distance)
        self.avg_distance_entry.config(state="readonly")

        self.cur.execute("""SELECT SUM(amount)
                                FROM ticket_flights
                                JOIN tickets ON ticket_flights.ticket_no = tickets.ticket_no
                                WHERE tickets.passenger_id = ?"""
                    , (values[0],))
        total_amount = self.cur.fetchone()[0]

        if total_amount:
            b = int(round(total_amount, 2))
        else:
            b = 0

        self.total_amount_entry.insert(0, b)
        self.total_amount_entry.config(state="readonly")

        if b != 0:
            self.cur.execute("""SELECT COUNT(ticket_flights.ticket_no) FROM ticket_flights
                                    JOIN tickets ON tickets.ticket_no = ticket_flights.ticket_no
                                    WHERE tickets.passenger_id = ?"""
                        , (values[0],))
            number_of_tickets = self.cur.fetchone()[0]

            avg_amount = round(total_amount / number_of_tickets, 2)
        else:
            avg_amount = 0
        self.avg_ticket_cost_entry.insert(0, avg_amount)
        self.avg_ticket_cost_entry.config(state="readonly")

        self.conn.close()

    def search_passengers(self):
        for record in self.passengers_tree.get_children():
            self.passengers_tree.delete(record)

        self.conn = sqlite3.connect(const.DATABASE_PATH)
        self.cur = self.conn.cursor()

        self.cur.execute(f"""SELECT passenger_id, first_name, last_name, email, street_number, street, city, zip, country
                    FROM passengers
                    JOIN countries ON passengers.country_id = countries.country_id
                    WHERE 
                    passenger_id LIKE COALESCE (?, "%")
                    AND first_name LIKE COALESCE (?, "%")
                    AND last_name LIKE COALESCE (?, "%")
                    AND email LIKE COALESCE (?, "%")
                    AND street_number LIKE COALESCE (?, "%")
                    AND street LIKE COALESCE (?, "%")
                    AND city LIKE COALESCE (?, "%")
                    AND zip LIKE COALESCE (?, "%")
                    AND countries.country LIKE COALESCE (?, "%")
                    ORDER BY passenger_id DESC
                    """,
                    (self.passenger_id_entry.get() or '%',
                     self.fn_entry.get() or '%',
                     self.ln_entry.get() or '%',
                     self.email_entry.get() or '%',
                     self.street_number_entry.get() or '%',
                     self.street_name_entry.get() or '%',
                     self.city_entry.get() or '%',
                     self.zip_code_entry.get() or '%',
                     self.country_entry.get() or '%'
                     ))
        records = self.cur.fetchall()
        self.conn.close()

        count = 0

        for record in records:
            if count % 2 == 0:
                self.passengers_tree.insert(parent="", index="end", iid=count, text="", values=(
                    record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8]),
                                            tags=("evenrow",))
            else:
                self.passengers_tree.insert(parent="", index="end", iid=count, text="", values=(
                    record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8]),
                                            tags=("oddrow",))

            count += 1

        utils.record_count(tree=self.passengers_tree, frame=self.tree_frame)

    def new_passenger(self):
        self.new_passenger_window = tk.Toplevel(self.master)
        self.new_passenger_window.title("New Passenger")
        self.new_passenger_window.geometry("700x400")
        self.new_passenger_window.iconbitmap(const.MAIN_ICON)

        self.new_passenger_frame = tk.LabelFrame(self.new_passenger_window, text="Passenger Details")
        self.new_passenger_frame.pack(fill="x", expand=1, padx=20)

        self.new_passenger_email_label = tk.Label(self.new_passenger_frame, text="Email")
        self.new_passenger_email_label.grid(row=0, column=0, padx=10, pady=10)
        self.new_passenger_email_entry = tk.Entry(self.new_passenger_frame)
        self.new_passenger_email_entry.grid(row=0, column=1, padx=10, pady=10)

        self.new_passenger_fn_label = tk.Label(self.new_passenger_frame, text="First Name")
        self.new_passenger_fn_label.grid(row=1, column=0, padx=10, pady=10)
        self.new_passenger_fn_entry = tk.Entry(self.new_passenger_frame)
        self.new_passenger_fn_entry.grid(row=1, column=1, padx=10, pady=10)

        self.new_passenger_ln_label = tk.Label(self.new_passenger_frame, text="Last Name")
        self.new_passenger_ln_label.grid(row=1, column=2, padx=10, pady=10)
        self.new_passenger_ln_entry = tk.Entry(self.new_passenger_frame)
        self.new_passenger_ln_entry.grid(row=1, column=3, padx=10, pady=10)

        self.new_passenger_street_number_label = tk.Label(self.new_passenger_frame, text="Street Number")
        self.new_passenger_street_number_label.grid(row=2, column=0, padx=10, pady=10)
        self.new_passenger_street_number_entry = tk.Entry(self.new_passenger_frame)
        self.new_passenger_street_number_entry.grid(row=2, column=1, padx=10, pady=10)

        self.new_passenger_street_name_label = tk.Label(self.new_passenger_frame, text="Street Name")
        self.new_passenger_street_name_label.grid(row=2, column=2, padx=10, pady=10)
        self.new_passenger_street_name_entry = tk.Entry(self.new_passenger_frame)
        self.new_passenger_street_name_entry.grid(row=2, column=3, padx=10, pady=10)

        self.new_passenger_city_label = tk.Label(self.new_passenger_frame, text="City")
        self.new_passenger_city_label.grid(row=3, column=0, padx=10, pady=10)
        self.new_passenger_city_entry = tk.Entry(self.new_passenger_frame)
        self.new_passenger_city_entry.grid(row=3, column=1, padx=10, pady=10)

        self.new_passenger_zip_code_label = tk.Label(self.new_passenger_frame, text="ZIP Code")
        self.new_passenger_zip_code_label.grid(row=3, column=2, padx=10, pady=10)
        self.new_passenger_zip_code_entry = tk.Entry(self.new_passenger_frame)
        self.new_passenger_zip_code_entry.grid(row=3, column=3, padx=10, pady=10)

        self.new_passenger_country_label = tk.Label(self.new_passenger_frame, text="Country")
        self.new_passenger_country_label.grid(row=4, column=0, padx=10, pady=10)

        self.new_passenger_country_entry = utils.AutofillDropdown(self.new_passenger_frame, self.new_passenger_window, row=4, column=1, width=26, options=const.countries_list())
        # self.new_passenger_country_entry = ttk.Combobox(self.new_passenger_frame, values=self.countries)
        # self.new_passenger_country_entry.grid(row=4, column=1)

        self.button_frame = tk.LabelFrame(self.new_passenger_window)
        self.button_frame.pack(fill="x", expand=1, padx=20)
        for i in range(2):
            self.button_frame.columnconfigure(i, weight=1)

        def keep_or_clear_entries():
            email_exists = self.add_passenger()
            if email_exists == False:
                utils.clear_entries(self.new_passenger_frame)
                self.new_passenger_country_entry.delete(0, "end")
                self.update_passengers_treeview(self.passengers_tree, self.tree_frame)

        self.save_and_add_another_button = tk.Button(self.button_frame, text="Save & Add Another",
                                             command=lambda: keep_or_clear_entries())
        self.save_and_add_another_button.grid(row=0, column=0, padx=10, pady=10)

        def show_or_close():
            email_exists = self.add_passenger()
            if email_exists == False:
                self.new_passenger_window.destroy()
                self.update_passengers_treeview(self.passengers_tree, self.tree_frame)

        self.save_and_close_button = tk.Button(self.button_frame, text="Save & Close", command=lambda: show_or_close())
        self.save_and_close_button.grid(row=0, column=1, padx=10, pady=10)

    def add_passenger(self):
        self.conn = sqlite3.connect(const.DATABASE_PATH)
        self.cur = self.conn.cursor()

        # Check if all required entries contain data
        required_entries = [
            self.new_passenger_fn_entry.get(),
            self.new_passenger_ln_entry.get(),
            self.new_passenger_email_entry.get(),
            self.new_passenger_street_number_entry.get(),
            self.new_passenger_street_name_entry.get(),
            self.new_passenger_city_entry.get(),
            self.new_passenger_zip_code_entry.get(),
            self.new_passenger_country_entry.get()
        ]

        if not all(required_entries):
            utils.popup_message_1(self.new_passenger_window,
                                  "Add Missing Details",
                                  "Please complete all reqired fileds to proceed.",
                                  "OK",
                                  const.ERROR_ICON
                                  )
            return

        # Validate email format
        email = self.new_passenger_email_entry.get()
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            utils.popup_message_1(self.new_passenger_window,
                                  "Invalid Email Format",
                                  "Please enter a valid email address.",
                                  "OK",
                                  const.ERROR_ICON
                                  )
            return

        self.cur.execute("SELECT country FROM countries")
        existing_countries = [country[0] for country in self.cur.fetchall()]

        if self.new_passenger_country_entry.get() not in existing_countries:
            utils.popup_message_1(self.new_passenger_window,
                                  "Incorrect Country Name",
                                  """Provided country name does not exist.
Please select a country from the list.""",
                                  "OK",
                                  const.ERROR_ICON
                                  )
            return

        try:
            # get country_id from the countries table
            country = self.new_passenger_country_entry.get()
            self.cur.execute("SELECT country_id FROM countries WHERE country = ?", (country,))
            country_id = self.cur.fetchone()[0]

            self.cur.execute(
                "INSERT INTO passengers (first_name, last_name, email, street_number, street, city, zip, country_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    self.new_passenger_fn_entry.get(),
                    self.new_passenger_ln_entry.get(),
                    self.new_passenger_email_entry.get(),
                    self.new_passenger_street_number_entry.get(),
                    self.new_passenger_street_name_entry.get(),
                    self.new_passenger_city_entry.get(),
                    self.new_passenger_zip_code_entry.get(),
                    country_id
                ))

            self.conn.commit()

            return False  # No error, email does not exist.

        except sqlite3.IntegrityError:
            existing_email = self.new_passenger_email_entry.get()
            utils.popup_message_1(window=self.new_passenger_window,
                            message_title="Add Record Failed",
                            message_text=f"""Email address {existing_email}
        already exists.
        Please use a different email.""",
                            button_text="OK",
                            image_filename=const.ERROR_ICON)

            return True  # Error, email already exists.

        finally:
            self.conn.close()

        self.passengers_tree.delete(*self.passengers_tree.get_children())

        self.update_passengers_treeview(self.passengers_tree, self.tree_frame)

    def update_passenger(self):
        selected = self.passengers_tree.focus()
        values = self.passengers_tree.item(selected, "values")

        if not selected:
            utils.popup_message_1(window=self.master,
                                message_title="No Record Selected",
                                message_text="Please select a record to edit.",
                                button_text="OK",
                                image_filename=const.ERROR_ICON)
            return

        utils.clear_entries(self.entry_frame)
        self.country_entry.config(state="normal")
        self.country_entry.delete(0, "end")

        self.update_record_window = tk.Toplevel(self.master)
        self.update_record_window.title("Edit Record")
        self.update_record_window.geometry("700x400")
        self.update_record_window.iconbitmap(const.MAIN_ICON)

        self.update_record_frame = tk.LabelFrame(self.update_record_window, text="Passenger Details")
        self.update_record_frame.pack(fill=tk.X, expand=1, padx=20)

        self.update_record_email_label = tk.Label(self.update_record_frame, text="Email")
        self.update_record_email_label.grid(row=0, column=0, padx=10, pady=10)
        self.update_record_email_entry = tk.Entry(self.update_record_frame)
        self.update_record_email_entry.grid(row=0, column=1, padx=10, pady=10)

        self.update_record_fn_label = tk.Label(self.update_record_frame, text="First Name")
        self.update_record_fn_label.grid(row=1, column=0, padx=10, pady=10)
        self.update_record_fn_entry = tk.Entry(self.update_record_frame)
        self.update_record_fn_entry.grid(row=1, column=1, padx=10, pady=10)

        self.update_record_ln_label = tk.Label(self.update_record_frame, text="Last Name")
        self.update_record_ln_label.grid(row=1, column=2, padx=10, pady=10)
        self.update_record_ln_entry = tk.Entry(self.update_record_frame)
        self.update_record_ln_entry.grid(row=1, column=3, padx=10, pady=10)

        self.update_record_street_number_label = tk.Label(self.update_record_frame, text="Street Number")
        self.update_record_street_number_label.grid(row=2, column=0, padx=10, pady=10)
        self.update_record_street_number_entry = tk.Entry(self.update_record_frame)
        self.update_record_street_number_entry.grid(row=2, column=1, padx=10, pady=10)

        self.update_record_street_name_label = tk.Label(self.update_record_frame, text="Street Name")
        self.update_record_street_name_label.grid(row=2, column=2, padx=10, pady=10)
        self.update_record_street_name_entry = tk.Entry(self.update_record_frame)
        self.update_record_street_name_entry.grid(row=2, column=3, padx=10, pady=10)

        self.update_record_city_label = tk.Label(self.update_record_frame, text="City")
        self.update_record_city_label.grid(row=3, column=0, padx=10, pady=10)
        self.update_record_city_entry = tk.Entry(self.update_record_frame)
        self.update_record_city_entry.grid(row=3, column=1, padx=10, pady=10)

        self.update_record_zip_code_label = tk.Label(self.update_record_frame, text="ZIP Code")
        self.update_record_zip_code_label.grid(row=3, column=2, padx=10, pady=10)
        self.update_record_zip_code_entry = tk.Entry(self.update_record_frame)
        self.update_record_zip_code_entry.grid(row=3, column=3, padx=10, pady=10)

        self.update_record_country_label = tk.Label(self.update_record_frame, text="Country")
        self.update_record_country_label.grid(row=4, column=0, padx=10, pady=10)
        self.update_record_country_entry = utils.AutofillDropdown(self.update_record_frame, self.update_record_window, row=4, column=1, width=26, options=const.countries_list())

        self.passenger_id_to_update = values[0]
        self.update_record_fn_entry.insert(0, values[1])
        self.update_record_ln_entry.insert(0, values[2])
        self.update_record_email_entry.insert(0, values[3])
        self.update_record_street_number_entry.insert(0, values[4])
        self.update_record_street_name_entry.insert(0, values[5])
        self.update_record_city_entry.insert(0, values[6])
        self.update_record_zip_code_entry.insert(0, values[7])
        self.update_record_country_entry.insert(0, values[8])

        def save_updated_record():
            # Check if all required entries contain data
            required_entries = [
                self.update_record_fn_entry.get(),
                self.update_record_ln_entry.get(),
                self.update_record_email_entry.get(),
                self.update_record_street_number_entry.get(),
                self.update_record_street_name_entry.get(),
                self.update_record_city_entry.get(),
                self.update_record_zip_code_entry.get(),
                self.update_record_country_entry.get()
            ]

            if not all(required_entries):
                utils.popup_message_1(self.update_record_window,
                                      "Add Missing Details",
                                      "Please complete all reqired fileds to proceed.",
                                      "OK",
                                      const.ERROR_ICON
                                      )
                return

            # Validate email format
            email = self.update_record_email_entry.get()
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                utils.popup_message_1(self.update_record_window,
                                      "Invalid Email Format",
                                      "Please enter a valid email address.",
                                      "OK",
                                      const.ERROR_ICON
                                      )
                return

            self.conn = sqlite3.connect(const.DATABASE_PATH)
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT country FROM countries")
            existing_countries = [country[0] for country in self.cur.fetchall()]
            self.conn.close()

            if self.update_record_country_entry.get() not in existing_countries:
                utils.popup_message_1(self.update_record_window,
                                      "Incorrect Country Name",
                                      """Provided country name does not exist.
Please select a country from the list.""",
                                      "OK",
                                      const.ERROR_ICON
                                      )
                return

            self.passengers_tree.item(selected, text="", values=(
                self.passenger_id_to_update, self.update_record_fn_entry.get(), self.update_record_ln_entry.get(),
                self.update_record_email_entry.get(), self.update_record_street_number_entry.get(),
                self.update_record_street_name_entry.get(), self.update_record_city_entry.get(),
                self.update_record_zip_code_entry.get(),
                self.update_record_country_entry.get()
            ))

            self.conn = sqlite3.connect(const.DATABASE_PATH)
            self.cur = self.conn.cursor()

            try:
                # get the country_id from countries table
                self.cur.execute("SELECT country_id FROM countries WHERE country = ?", (self.update_record_country_entry.get(),))
                self.country_id = self.cur.fetchone()[0]

                self.cur.execute("""UPDATE passengers 
                        SET
                        first_name = :first_name,
                        last_name = :last_name,
                        email = :email,
                        street_number = :street_number,
                        street = :street_name,
                        city = :city,
                        zip = :zip_code,
                        country_id = :country

                        WHERE passenger_id = :passenger_id""",
                            {"passenger_id": self.passenger_id_to_update,
                             "first_name": self.update_record_fn_entry.get(),
                             "last_name": self.update_record_ln_entry.get(),
                             "email": self.update_record_email_entry.get(),
                             "street_number": self.update_record_street_number_entry.get(),
                             "street_name": self.update_record_street_name_entry.get(),
                             "city": self.update_record_city_entry.get(),
                             "zip_code": self.update_record_zip_code_entry.get(),
                             "country": self.country_id
                             }
                            )

                self.conn.commit()

                return False  # No error, existing email not found.

            except sqlite3.IntegrityError:
                existing_email = self.update_record_email_entry.get()

                utils.popup_message_1(window=self.update_record_window,
                                message_title="Update Record Failed",
                                message_text=f"""Email address {existing_email}
        already exists.
        Please use a different email.""",
                                button_text="OK",
                                image_filename=const.ERROR_ICON)

                return True  # Error, existing email found.

            finally:
                self.conn.close()

        self.button_frame = tk.LabelFrame(self.update_record_window)
        self.button_frame.pack(fill=tk.X, expand=1, padx=20)

        def save_and_close():
            email_exists = save_updated_record()
            if email_exists == False:
                self.update_record_window.destroy()
                self.update_passengers_treeview(self.passengers_tree, self.tree_frame)

        self.save_button = tk.Button(self.button_frame, text="Save", padx=20, command=save_and_close)
        self.save_button.pack(pady=20)

    def delete_passenger(self):
        selected_items = self.passengers_tree.selection()

        if not selected_items:
            utils.popup_message_1(
                window=self.master,
                message_title="Cannot Perform Delete",
                message_text="No record selected!",
                button_text="OK",
                image_filename=const.ERROR_ICON
            )
            return

        ids_to_delete = [self.passengers_tree.item(record, "values")[0] for record in selected_items]

        self.conn = sqlite3.connect(const.DATABASE_PATH)
        self.cur = self.conn.cursor()

        # Construct the query to check if any of the selected passenger IDs have tickets
        query = f"SELECT passenger_id FROM tickets WHERE passenger_id IN ({','.join(['?'] * len(ids_to_delete))})"
        self.cur.execute(query, ids_to_delete)
        passengers_having_tickets = self.cur.fetchall()
        self.conn.close()

        if passengers_having_tickets:
            utils.popup_message_1(
                window=self.master,
                message_title="Records Cannot Be Deleted",
                message_text="""Selected passengers have purchase history 
and cannot be deleted.""",
                button_text="OK",
                image_filename=const.ERROR_ICON
            )
            return

        def delete_record():
            for record in selected_items:
                self.passengers_tree.delete(record)

            self.conn = sqlite3.connect(const.DATABASE_PATH)
            self.cur = self.conn.cursor()
            self.cur.executemany("DELETE FROM passengers WHERE passenger_id = ?", [(a,) for a in ids_to_delete])
            self.conn.commit()
            self.conn.close()
            utils.clear_entries(self.entry_frame)
            self.country_entry.config(state="normal")
            self.country_entry.delete(0, "end")
            utils.record_count(tree=self.passengers_tree, frame=self.tree_frame)
            utils.popup_message_1(
                window=self.master,
                message_title="Records Deleted",
                message_text="Selected record(s) deleted successfully.",
                button_text="OK",
                image_filename=const.INFORMATION_ICON
            )

        message = utils.popup_message_2(
            window=self.master,
            message_title="Delete Selected Records",
            message_text="""Are you sure you want to delete the selected record(s)?
            You cannot undo this action.""",
            button_1_text="Delete",
            button_2_text="Cancel",
            image_filename=const.QUESTIONMARK_ICON,
            command_1=lambda: (message.destroy(), delete_record())
        )

    def fetch_passengers_data(self):
        """
        Fetch passenger data from the database.

        Returns:
        List of tuples: Each tuple contains data for one passenger.
        """
        self.conn = sqlite3.connect(const.DATABASE_PATH)
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(f"""SELECT passenger_id, first_name, last_name, email, street_number, street, city, zip, country
                                FROM passengers
                                JOIN countries ON passengers.country_id = countries.country_id
                                ORDER BY passenger_id DESC
                                LIMIT {const.PASSENGERS_TAB_TREEVIEW_RECORD_LIMIT}""")
            return self.cur.fetchall()
        finally:
            self.conn.close()

    def update_passengers_treeview(self, tree, tree_frame):
        """
        Handle the process of fetching and displaying passenger data in the treeview.

        Parameters:
        passengers_tree (tkinter.ttk.Treeview): The Treeview widget instance to update.
        passengers_tree_frame (tkinter.Frame): The frame where the number of records is displayed.

        Returns:
        None
        """
        data = self.fetch_passengers_data()
        utils.update_treeview(self.passengers_tree, data)
        utils.record_count(self.passengers_tree, self.tree_frame)



