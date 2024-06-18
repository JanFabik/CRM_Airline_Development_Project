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

        # self.scheduled_flights_tree.bind("<ButtonRelease-1>", self.select_flight)
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

        self.search_flights_button = tk.Button(self.search_flights_frame_commands_frame, text="Search Flights")
        self.search_flights_button.grid(row=3, column=3, padx=10, pady=10)

        self.select_seats_button_frame = tk.LabelFrame(self.master, text="Select Seats")
        self.select_seats_button_frame.grid(row=1, column=1)
        self.flight_id_label = tk.Label(self.select_seats_button_frame, text="Flight ID")
        self.flight_id_label.grid(row=0, column=1, padx=10, pady=10)
        self.flight_id_entry = tk.Entry(self.select_seats_button_frame)
        self.flight_id_entry.grid(row=1, column=1, padx=10, pady=10)
        self.select_seats_button = tk.Button(self.select_seats_button_frame, text="Select Seats >>", padx=10)
        self.select_seats_button.grid(row=2, column=1, padx=10, pady=10)

        self.passenger_id_to_select_seat_label = tk.Label(self.select_seats_button_frame, text="Passenger ID")
        self.passenger_id_to_select_seat_label.grid(row=0, column=0, padx=20)
        self.passenger_id_to_select_seat_entry = tk.Entry(self.select_seats_button_frame)
        self.passenger_id_to_select_seat_entry.grid(row=1, column=0, padx=20)