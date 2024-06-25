import tkinter as tk
from tkinter import ttk
import tkcalendar as tkcal
import sqlite3
import constants as const
import utils
import settings
import sys


class ScheduleFlightsUI:
    def __init__(self, master):
        self.master = master
        self.setup_ui()

    def setup_ui(self):
        # Create frame for flight details
        self.flight_details_frame = tk.LabelFrame(self.master, text="Flight Details")
        self.flight_details_frame.grid(row=0, column=0, sticky=tk.NW, padx=20, pady=10)

        # Get list of airport names with airport codes
        self.airports = const.airports_list()

        # Get list of aircraft names with aircraft codes
        self.aircrafts = const.aircrafts_list()

        # Create widgets for departure details
        self.departure_date_label = tk.Label(self.flight_details_frame, text="Departure Date")
        self.departure_date_label.grid(row=0, column=0, sticky=tk.W, padx=20)

        self.departure_calendar = tkcal.Calendar(self.flight_details_frame, selectmode="day", date_pattern="y-mm-dd", year=2023, month=8, day=1)
        self.departure_calendar.grid(row=1, column=0, pady=10, padx=40)
        # Bind the <<CalendarSelected>> event to the on_date_selected function
        self.departure_calendar.bind("<<CalendarSelected>>", self.on_departure_date_selected)

        self.departure_details_frame = tk.Frame(self.flight_details_frame)
        self.departure_details_frame.grid(row=0, column=1, rowspan=2)

        self.origin_label = tk.Label(self.departure_details_frame, text="Origin")
        self.origin_label.grid(row=0, column=0, padx=(0,10), pady=10)

        self.origin_entry = utils.AutofillDropdown(self.departure_details_frame, self.master, row=0, column=1, width=30, options=self.airports, padx=20)

        self.departure_time_label = tk.Label(self.departure_details_frame, text="Departure Time")
        self.departure_time_label.grid(row=2, column=0, padx=(0,10))

        self.departure_time_picker = utils.TimePicker(self.departure_details_frame)
        self.departure_time_picker.grid(row=2, column=1, pady=20, sticky=tk.W)

        # Create widgets for arrival details
        self.arrival_date_label = tk.Label(self.flight_details_frame, text="Arrival Date")
        self.arrival_date_label.grid(row=0, column=2, sticky=tk.W, padx=20)

        self.arrival_calendar = tkcal.Calendar(self.flight_details_frame, selectmode="day", date_pattern="y-mm-dd", year=2023, month=8, day=1)
        self.arrival_calendar.grid(row=1, column=2, pady=10, padx=40)

        self.arrival_details_frame = tk.Frame(self.flight_details_frame)
        self.arrival_details_frame.grid(row=0, column=3, rowspan=2)

        self.origin_label = tk.Label(self.arrival_details_frame, text="Destination")
        self.origin_label.grid(row=0, column=0, padx=(0,10), pady=10)

        self.destination_entry = utils.AutofillDropdown(self.arrival_details_frame, self.master, row=0, column=1, width=30, options=self.airports, padx=20)

        self.departure_time_label = tk.Label(self.arrival_details_frame, text="Arrival Time")
        self.departure_time_label.grid(row=2, column=0, padx=(0,10))

        self.departure_time_picker = utils.TimePicker(self.arrival_details_frame)
        self.departure_time_picker.grid(row=2, column=1, pady=20, sticky=tk.W)


        self.recurrence_pattern_frame = tk.LabelFrame(self.flight_details_frame, text="Recurrence Pattern")
        self.recurrence_pattern_frame.grid(row=3, column=0, pady=10, columnspan=2)

        self.daily_radiobutton = tk.Radiobutton(self.recurrence_pattern_frame, text="Daily")
        self.daily_radiobutton.grid(row=0,column=0, sticky=tk.W, pady=(10,0))

        self.weekly_radiobutton = tk.Radiobutton(self.recurrence_pattern_frame, text="Weekly")
        self.weekly_radiobutton.grid(row=1, column=0, sticky=tk.W, pady=(0,10))

        self.separator = ttk.Separator(self.recurrence_pattern_frame, orient='vertical')
        self.separator.grid(row=0, column=1, sticky=(tk.N, tk.S), padx=(20, 20), pady=10, rowspan=4)

        self.recur_label_1st_part = tk.Label(self.recurrence_pattern_frame, text="Recur every")
        self.recur_label_1st_part.grid(row=0, column=2, pady=(10, 0), sticky=tk.W)

        self.spinbox_value = tk.StringVar(value='1')
        self.recur_weeks_entry = ttk.Spinbox(self.recurrence_pattern_frame, from_=1, to=8, wrap=True, width=2,font=("Calibri", 12), textvariable=self.spinbox_value)
        self.recur_weeks_entry.grid(row=0, column=2, pady=(10, 0), sticky=tk.E)

        self.recur_label_2nd_part = tk.Label(self.recurrence_pattern_frame, text="week(s) on:")
        self.recur_label_2nd_part.grid(row=0, column=3, pady=(10, 0), sticky=tk.W)

        self.sunday_check = tk.Checkbutton(self.recurrence_pattern_frame, text="Sunday")
        self.sunday_check.grid(row=1, column=2, padx=20, pady=(10,0), sticky=tk.W)

        self.monday_check = tk.Checkbutton(self.recurrence_pattern_frame, text="Monday")
        self.monday_check.grid(row=1, column=3, padx=20, pady=(10,0), sticky=tk.W)

        self.tuesday_check = tk.Checkbutton(self.recurrence_pattern_frame, text="Tuesday")
        self.tuesday_check.grid(row=1, column=4, padx=20, pady=(10,0), sticky=tk.W)

        self.wednesday_check = tk.Checkbutton(self.recurrence_pattern_frame, text="Wednesday")
        self.wednesday_check.grid(row=1, column=5, padx=20, pady=(10,0), sticky=tk.W)

        self.thursday_check = tk.Checkbutton(self.recurrence_pattern_frame, text="Thursday")
        self.thursday_check.grid(row=2, column=2, padx=20, pady=(0,10), sticky=tk.W)

        self.friday_check = tk.Checkbutton(self.recurrence_pattern_frame, text="Friday")
        self.friday_check.grid(row=2, column=3, padx=20, pady=(0,10), sticky=tk.W)

        self.saturday_check = tk.Checkbutton(self.recurrence_pattern_frame, text="Saturday")
        self.saturday_check.grid(row=2, column=4, padx=20, pady=(0,10), sticky=tk.W)

        self.end_by_label = tk.Label(self.recurrence_pattern_frame, text="End by:")
        self.end_by_label.grid(row=3, column=2, pady=(0, 10), sticky=tk.W)

        self.end_by_entry = utils.DatePickerEntry(self.recurrence_pattern_frame, width=15)
        self.end_by_entry.grid(row=3, column=3, pady=(0, 10), sticky=tk.W)

        self.aircraft_model_label = tk.Label(self.flight_details_frame, text="Aircraft Model")
        self.aircraft_model_label.grid(row=3, column=3, padx=20, pady=40, sticky=tk.E)

        self.aircraft_model_entry = utils.AutofillDropdown(self.flight_details_frame, self.master, row=3, column=3, width=30, options=self.aircrafts, sticky=tk.W)

        self.schedule_flight_button = tk.Button(self.flight_details_frame, text="Schedule Flight >")
        self.schedule_flight_button.grid(row=3, column=3, sticky=tk.S, pady=10)

        self.scheduled_flights_frame = tk.LabelFrame(self.master, text="Scheduled Flights")
        self.scheduled_flights_frame.grid(row=1, column=0, padx=20, columnspan=2)

        self.tree_scroll = tk.Scrollbar(self.scheduled_flights_frame, width=25)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.scheduled_flights_tree = ttk.Treeview(self.scheduled_flights_frame, yscrollcommand=self.tree_scroll.set, selectmode="extended", height=5)
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
        # self.scheduled_flights_tree.bind("<ButtonRelease-1>", self.select_flight)


    def on_departure_date_selected(self, event):
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
                                AND scheduled_departure LIKE ? 
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
                                origin,
                                destination""",
                    (str(self.departure_calendar.get_date()) + '%',
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

