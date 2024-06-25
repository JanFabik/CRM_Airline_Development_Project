import tkinter as tk
from tkinter import ttk
import tkcalendar as tkcal
import sqlite3
import constants as const
import utils
import settings
import sys
from Ui import Seat_Maps

class BookFlightsUI:
    def __init__(self, master):
        self.master = master
        self.setup_ui()

    def setup_ui(self):
        self.scheduled_flights_frame = tk.LabelFrame(self.master, text="Scheduled Flights")
        self.scheduled_flights_frame.grid(row=0, column=0, padx=20, pady=10, columnspan=2)

        self.tree_scroll = tk.Scrollbar(self.scheduled_flights_frame, width=25)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.scheduled_flights_tree = ttk.Treeview(self.scheduled_flights_frame, yscrollcommand=self.tree_scroll.set,
                                              selectmode="extended",
                                              height=5)
        self.scheduled_flights_tree.pack(padx=20, pady=10)

        self.tree_scroll.config(command=self.scheduled_flights_tree.yview)

        self.scheduled_flights_tree["columns"] = (
            "Flight ID", "Flight No", "Origin", "Destination", "Departure", "Arrival", "Aircraft", "Occupancy")

        self.scheduled_flights_tree.column("#0", width=0, stretch=tk.NO)
        self.scheduled_flights_tree.column("Flight ID", anchor=tk.W, width=80)
        self.scheduled_flights_tree.column("Flight No", anchor=tk.W, width=80)
        self.scheduled_flights_tree.column("Origin", anchor=tk.W, width=280)
        self.scheduled_flights_tree.column("Destination", anchor=tk.W, width=280)
        self.scheduled_flights_tree.column("Departure", anchor=tk.W, width=180)
        self.scheduled_flights_tree.column("Arrival", anchor=tk.W, width=180)
        self.scheduled_flights_tree.column("Aircraft", anchor=tk.W, width=160)
        self.scheduled_flights_tree.column("Occupancy", anchor=tk.W, width=140)

        self.scheduled_flights_tree.heading("#0", text="", anchor=tk.W)
        self.scheduled_flights_tree.heading("Flight ID", text="Flight ID", anchor=tk.W)
        self.scheduled_flights_tree.heading("Flight No", text="Flight No", anchor=tk.W)
        self.scheduled_flights_tree.heading("Origin", text="Origin", anchor=tk.W)
        self.scheduled_flights_tree.heading("Destination", text="Destination", anchor=tk.W)
        self.scheduled_flights_tree.heading("Departure", text="Departure", anchor=tk.W)
        self.scheduled_flights_tree.heading("Arrival", text="Arrival", anchor=tk.W)
        self.scheduled_flights_tree.heading("Aircraft", text="Aircraft", anchor=tk.W)
        self.scheduled_flights_tree.heading("Occupancy", text="Occupancy", anchor=tk.W)

        self.scheduled_flights_tree.tag_configure("oddrow", background=settings.saved_secondary_color)
        self.scheduled_flights_tree.tag_configure("evenrow", background=settings.saved_primary_color)

        self.scheduled_flights_tree.bind("<ButtonRelease-1>", self.select_flight)
        self.search_flights_frame = tk.LabelFrame(self.master, text="Search Flights")
        self.search_flights_frame.grid(row=1, column=0, sticky=tk.W, padx=20)

        self.search_flights_frame_commands_frame = tk.Frame(self.search_flights_frame)
        self.search_flights_frame_commands_frame.grid(row=0, column=1)

        self.airports = const.airports_list()

        self.origin_label = tk.Label(self.search_flights_frame_commands_frame, text="Origin")
        self.origin_label.grid(row=0, column=0, padx=10, pady=10)

        self.origin_entry = utils.AutofillDropdown(self.search_flights_frame_commands_frame, self.master, row=0, column=1, width=30, options=self.airports)

        self.destination_label = tk.Label(self.search_flights_frame_commands_frame, text="Destination")
        self.destination_label.grid(row=1, column=0, padx=10, pady=10)

        self.destination_entry = utils.AutofillDropdown(self.search_flights_frame_commands_frame, self.master, row=1, column=1, width=30, options=self.airports)

        self.search_flights_calendar = tkcal.Calendar(self.search_flights_frame, selectmode="day", date_pattern="y-mm-dd", year=2023,
                                           month=8,
                                           day=1)
        self.search_flights_calendar.grid(row=0, column=0, pady=10, padx=20)

        self.search_flights_button = tk.Button(self.search_flights_frame_commands_frame, text="Search Flights",
                                       command=self.search_flights)
        self.search_flights_button.grid(row=3, column=3, padx=10, pady=10)

        self.select_seats_button_frame = tk.LabelFrame(self.master, text="Select Seats")
        self.select_seats_button_frame.grid(row=1, column=1)
        self.flight_id_label = tk.Label(self.select_seats_button_frame, text="Flight ID")
        self.flight_id_label.grid(row=0, column=1, padx=10, pady=10)
        self.flight_id_entry = tk.Entry(self.select_seats_button_frame)
        self.flight_id_entry.grid(row=1, column=1, padx=10, pady=10)
        self.select_seats_button = tk.Button(self.select_seats_button_frame, text="Select Seats >>", padx=10,
                                     command=self.select_seat_map)
        self.select_seats_button.grid(row=2, column=1, padx=10, pady=10)

        self.passenger_id_to_select_seat_label = tk.Label(self.select_seats_button_frame, text="Passenger ID")
        self.passenger_id_to_select_seat_label.grid(row=0, column=0, padx=20)
        self.passenger_id_to_select_seat_entry = tk.Entry(self.select_seats_button_frame)
        self.passenger_id_to_select_seat_entry.grid(row=1, column=0, padx=20)

        def find_passenger_for_seat():
            conn = sqlite3.connect(const.DATABASE_PATH)
            cur = conn.cursor()
            cur.execute(f"""SELECT first_name, last_name, email
                                        FROM passengers
                                        WHERE passenger_id = ?                            
                                    """, (self.passenger_id_to_select_seat_entry.get(),))
            passenger_information = cur.fetchone()
            conn.close()

            if passenger_information:
                self.passenger_information_label.config(
                    text=f"{passenger_information[0]} {passenger_information[1]} <{passenger_information[2]}>")
                self.passenger_id_to_select_seat_entry.config(state="readonly")
            else:
                self.passenger_information_label.config(text=f"⚠ Passenger ID not found.")

        self.find_passenger_button = tk.Button(self.select_seats_button_frame, text="Find", padx=10, command=find_passenger_for_seat)
        self.find_passenger_button.grid(row=2, column=0)

        self.passenger_information_label = tk.Label(self.select_seats_button_frame, text="")
        self.passenger_information_label.grid(row=3, column=0, pady=20, columnspan=2)

        def reset_flights_view():
            self.update_scheduled_flights_treeview(self.scheduled_flights_tree, self.scheduled_flights_frame)
            self.passenger_id_to_select_seat_entry.config(state="normal")
            self.passenger_information_label.config(state="normal")
            self.passenger_id_to_select_seat_entry.delete(0, tk.END)
            self.passenger_information_label.config(text="")
            self.origin_entry.delete(0, tk.END)
            self.destination_entry.delete(0, tk.END)

            for record in self.passengers_on_flight_tree.get_children():
                self.passengers_on_flight_tree.delete(record)

        self.reset_flights_view_button = tk.Button(self.search_flights_frame_commands_frame, text="Reset View", padx=10,
                                           command=reset_flights_view)
        self.reset_flights_view_button.grid(row=3, column=0, padx=10, pady=10, sticky=tk.S)

        self.update_scheduled_flights_treeview(self.scheduled_flights_tree, self.scheduled_flights_frame)

        self.passengers_on_flight_frame = tk.LabelFrame(self.master, text="Passengers on Flight")
        self.passengers_on_flight_frame.grid(row=2, column=0, padx=20, pady=10, columnspan=2, sticky=tk.EW)

        self.passengers_on_flight_tree_scroll = tk.Scrollbar(self.passengers_on_flight_frame, width=25)
        self.passengers_on_flight_tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.passengers_on_flight_tree = ttk.Treeview(self.passengers_on_flight_frame,
                                                 yscrollcommand=self.passengers_on_flight_tree_scroll.set,
                                                 selectmode="extended",
                                                 height=7)
        self.passengers_on_flight_tree.pack(padx=20, pady=10)

        self.passengers_on_flight_tree_scroll.config(command=self.passengers_on_flight_tree.yview)

        self.passengers_on_flight_tree["columns"] = (
            "Seat Number", "Passenger ID", "First Name", "Last Name", "Email", "Street Number", "Street Name", "City",
            "ZIP Code",
            "Country")

        self.passengers_on_flight_tree.column("#0", width=0, stretch=tk.NO)
        self.passengers_on_flight_tree.column("Seat Number", anchor=tk.W, width=80)
        self.passengers_on_flight_tree.column("Passenger ID", anchor=tk.W, width=120)
        self.passengers_on_flight_tree.column("First Name", anchor=tk.W, width=120)
        self.passengers_on_flight_tree.column("Last Name", anchor=tk.W, width=140)
        self.passengers_on_flight_tree.column("Email", anchor=tk.W, width=240)
        self.passengers_on_flight_tree.column("Street Number", anchor=tk.W, width=80)
        self.passengers_on_flight_tree.column("Street Name", anchor=tk.W, width=140)
        self.passengers_on_flight_tree.column("City", anchor=tk.W, width=140)
        self.passengers_on_flight_tree.column("ZIP Code", anchor=tk.W, width=80)
        self.passengers_on_flight_tree.column("Country", anchor=tk.W, width=240)

        self.passengers_on_flight_tree.heading("#0", text="", anchor=tk.W)
        self.passengers_on_flight_tree.heading("Seat Number", text="Seat Number", anchor=tk.W)
        self.passengers_on_flight_tree.heading("Passenger ID", text="Passenger ID", anchor=tk.W)
        self.passengers_on_flight_tree.heading("First Name", text="First Name", anchor=tk.W)
        self.passengers_on_flight_tree.heading("Last Name", text="Last Name", anchor=tk.W)
        self.passengers_on_flight_tree.heading("Email", text="Email", anchor=tk.W)
        self.passengers_on_flight_tree.heading("Street Number", text="Street Number", anchor=tk.W)
        self.passengers_on_flight_tree.heading("Street Name", text="Street Name", anchor=tk.W)
        self.passengers_on_flight_tree.heading("City", text="City", anchor=tk.W)
        self.passengers_on_flight_tree.heading("ZIP Code", text="ZIP Code", anchor=tk.W)
        self.passengers_on_flight_tree.heading("Country", text="Country", anchor=tk.W)

        self.passengers_on_flight_tree.tag_configure("oddrow", background=settings.saved_secondary_color)
        self.passengers_on_flight_tree.tag_configure("evenrow", background=settings.saved_primary_color)

    def fetch_scheduled_flights_data(self):
        """
        Fetch scheduled flights data from the database.

        Returns:
        List of tuples: Each tuple contains data for one flight.
        """
        self.conn = sqlite3.connect(const.DATABASE_PATH)
        try:
            self.cur = self.conn.cursor()
            self.cur.execute("""SELECT 
                            flights.flight_id,
                            flight_no, 
                            dep_airport.airport_name || ' ('|| flights.departure_airport|| ')' AS origin, 
                            arr_airport.airport_name || ' ('|| flights.arrival_airport|| ')' AS destination, 
                            scheduled_departure, 
                            scheduled_arrival, 
                            aircrafts_data.model, 
                            COUNT(boarding_passes.seat_no) || ' / ' || (
                                SELECT COUNT(*) 
                                FROM seats 
                                WHERE seats.aircraft_code = flights.aircraft_code
                            ) as occupancy
                        FROM flights
                        JOIN aircrafts_data ON aircrafts_data.aircraft_code = flights.aircraft_code
                        JOIN airports_data AS dep_airport ON dep_airport.airport_code = flights.departure_airport
                        JOIN airports_data AS arr_airport ON arr_airport.airport_code = flights.arrival_airport
                        JOIN ticket_flights ON ticket_flights.flight_id = flights.flight_id
                        LEFT JOIN boarding_passes ON boarding_passes.ticket_no = ticket_flights.ticket_no AND flights.flight_id = boarding_passes.flight_id
                        WHERE flights.status = "Scheduled" OR flights.status = "Delayed"
                        GROUP BY flights.flight_id
                        ORDER BY scheduled_departure
                        """)
            return self.cur.fetchall()
        finally:
            self.conn.close()

    def update_scheduled_flights_treeview(self, scheduled_flights_tree, scheduled_flights_frame):
        """
        Handle the entire process of fetching and displaying scheduled flights data in the treeview.

        Parameters:
        scheduled_flights_tree (tkinter.ttk.Treeview): The Treeview widget instance to update.
        scheduled_flights_frame (tkinter.Frame): The frame where the number of records is displayed.

        Returns:
        None
        """
        self.data = self.fetch_scheduled_flights_data()
        utils.update_treeview(self.scheduled_flights_tree, self.data)
        utils.record_count(tree=self.scheduled_flights_tree, frame=self.scheduled_flights_frame)

    def fetch_passengers_on_flight_data(self, scheduled_flights_tree):
        """
        Fetch data about passengers on a specfic flight from the database.

        Parameters:
        scheduled_flights_tree (tkinter.ttk.Treeview): The treeview with flights to select from.

        Returns:
        List of tuples: Each tuple contains data for one passenger.
        """
        self.conn = sqlite3.connect(const.DATABASE_PATH)
        try:
            self.cur = self.conn.cursor()
            self.cur.execute("""SELECT seat_no, passengers.passenger_id, first_name, last_name, email, street_number, street, city, zip, country
                    FROM passengers
                    JOIN countries ON passengers.country_id = countries.country_id
                    JOIN tickets ON tickets.passenger_id = passengers.passenger_id
                    JOIN boarding_passes ON boarding_passes.ticket_no = tickets.ticket_no
                    WHERE boarding_passes.flight_id = ?
                    ORDER BY last_name
                     """, ((self.scheduled_flights_tree.item(self.scheduled_flights_tree.focus())['values'][0],)))
            return self.cur.fetchall()
        finally:
            self.conn.close()


    def update_passengers_on_flight_treeview(self, scheduled_flights_tree, passengers_on_flight_tree, passengers_on_flight_frame):
        """
        Handle the entire process of fetching and displaying data about passengers on a specific flight in the treeview.

        Parameters:
        scheduled_flights_tree (tkinter.ttk.Treeview): The treeview with flights to select from.
        passengers_on_flight_tree (tkinter.ttk.Treeview): The Treeview widget instance to update.
        passengers_on_flight_frame (tkinter.Frame): The frame where the number of records is displayed.

        Returns:
        None
        """
        self.data = self.fetch_passengers_on_flight_data(self.scheduled_flights_tree)
        utils.update_treeview(self.passengers_on_flight_tree, self.data)
        utils.record_count(tree=self.passengers_on_flight_tree, frame=self.passengers_on_flight_frame)

    def search_flights(self):
        for record in self.scheduled_flights_tree.get_children():
            self.scheduled_flights_tree.delete(record)

        conn = sqlite3.connect(const.DATABASE_PATH)
        cur = conn.cursor()

        cur.execute(f"""SELECT 
                                flights.flight_id,
                                flight_no, 
                                dep_airport.airport_name || ' ('|| flights.departure_airport|| ')' AS origin, 
                                arr_airport.airport_name || ' ('|| flights.arrival_airport|| ')' AS destination, 
                                scheduled_departure, 
                                scheduled_arrival, 
                                aircrafts_data.model, 
                                COUNT(boarding_passes.seat_no) || ' / ' || 
                                (SELECT COUNT(*) FROM seats WHERE seats.aircraft_code = aircrafts_data.aircraft_code) as occupancy
                            FROM 
                                flights
                            JOIN 
                                ticket_flights ON ticket_flights.flight_id = flights.flight_id
                            LEFT JOIN 
                                boarding_passes ON boarding_passes.ticket_no = ticket_flights.ticket_no AND flights.flight_id = boarding_passes.flight_id
                            JOIN 
                                aircrafts_data ON aircrafts_data.aircraft_code = flights.aircraft_code
                            JOIN 
                                airports_data AS dep_airport ON dep_airport.airport_code = flights.departure_airport
                            JOIN 
                                airports_data AS arr_airport ON arr_airport.airport_code = flights.arrival_airport
                            WHERE 
                                (flights.status = "Scheduled" OR flights.status = "Delayed")
                                AND
                                scheduled_departure LIKE ? 
                                AND 
                                flights.departure_airport = ?
                                AND 
                                flights.arrival_airport = ?
                            GROUP BY 
                                flights.flight_id, 
                                flight_no, 
                                dep_airport.airport_name, 
                                flights.departure_airport, 
                                arr_airport.airport_name, 
                                flights.arrival_airport, 
                                scheduled_departure, 
                                scheduled_arrival, 
                                aircrafts_data.model
                            ORDER BY 
                                scheduled_departure
                    """,
                    (str(self.search_flights_calendar.get_date()) + '%',
                     self.origin_entry.get()[len(self.origin_entry.get()) - 4: len(self.origin_entry.get()) - 1],
                     self.destination_entry.get()[len(self.destination_entry.get()) - 4: len(self.destination_entry.get()) - 1]
                     ))
        records = cur.fetchall()
        conn.close()

        count = 0

        for record in records:
            if count % 2 == 0:
                self.scheduled_flights_tree.insert(parent="", index="end", iid=count, text="", values=(
                    record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7]),
                                              tags=("evenrow",))
            else:
                self.scheduled_flights_tree.insert(parent="", index="end", iid=count, text="", values=(
                    record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7]),
                                              tags=("oddrow",))

            count += 1

        utils.record_count(tree=self.scheduled_flights_tree, frame=self.scheduled_flights_frame)

        self.flight_id_entry.config(state="normal")
        self.flight_id_entry.delete(0, tk.END)

    def select_flight(self, e):
        self.flight_id_entry.config(state="normal")
        self.flight_id_entry.delete(0, tk.END)

        selected = self.scheduled_flights_tree.focus()
        values = self.scheduled_flights_tree.item(selected, "values")

        self.flight_id_entry.insert(0, values[0])
        self.flight_id_entry.config(state="readonly")

        self.update_passengers_on_flight_treeview(self.scheduled_flights_tree, self.passengers_on_flight_tree, self.passengers_on_flight_frame)

    def select_seat_map(self):
        selected = self.scheduled_flights_tree.focus()
        values = self.scheduled_flights_tree.item(selected, "values")
        self.aircraft_model = values[6]

        self.conn = sqlite3.connect(const.DATABASE_PATH)
        self.cur = self.conn.cursor()

        self.cur.execute(f"""SELECT aircraft_code FROM aircrafts_data WHERE model = ?""", (self.aircraft_model,))
        aircraft_code = self.cur.fetchone()[0]
        self.conn.close()

        class_name = f"SeatMap{aircraft_code}"

        # Access the class directly from Seat_Maps module
        seat_map_class = getattr(Seat_Maps, class_name)
        return seat_map_class(self.master, self.get_passenger_id(), self.get_flight_id())



    def get_passenger_id(self):
        return self.passenger_id_to_select_seat_entry.get()

    def get_flight_id(self):
        return self.flight_id_entry.get()