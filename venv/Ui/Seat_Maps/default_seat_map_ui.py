import tkinter as tk
import constants as const
from tkinter import ttk
import sqlite3
import random
import string
import datetime


class SeatMap:
    """A class representing a seat map for a flight."""

    def __init__(self, master, passenger_id, flight_id):
        """Initialize the SeatMap object.

        Args:
            master (tk.Tk or tk.Toplevel): The master widget.
            passenger_id (int): The ID of the passenger.
            flight_id (int): The ID of the flight.
        """
        self.master = master
        self.passenger_id = passenger_id
        self.flight_id = flight_id
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface for the seat map."""
        # Create a window for seat selection
        self.seats_picker_window = tk.Toplevel(self.master)
        self.seats_picker_window.title("Select Seats")
        self.seats_picker_window.iconbitmap(const.MAIN_ICON)

        # Maximize the window
        self.seats_picker_window.state('zoomed')
        # Set weight of the window's grid colum to 1 to expadn the content horizontally
        self.seats_picker_window.columnconfigure(0, weight=1)

        # Create a frame for passenger details
        self.passenger_information_tree_frame = tk.LabelFrame(self.seats_picker_window, text="Passenger Details")
        self.passenger_information_tree_frame.grid(row=0, column=0, padx=20, pady=10)
        self.passenger_information_tree_frame.columnconfigure(0, weight=1)

        # Create a treeview for displaying passenger information
        self.passenger_information_tree = ttk.Treeview(self.passenger_information_tree_frame, height=1)
        self.passenger_information_tree.grid(row=1, column=0, padx=35, pady=10, sticky=tk.EW)
        self.passenger_information_tree["columns"] = (
            "Passenger ID", "First Name", "Last Name", "Email", "Street Number", "Street Name", "City", "ZIP Code",
            "Country")
        self.passenger_information_tree.column("#0", width=0, stretch=tk.NO)
        for col in self.passenger_information_tree["columns"]:
            self.passenger_information_tree.column(col, anchor=tk.W, width=120)
            self.passenger_information_tree.heading(col, text=col, anchor=tk.W)

        # Load and display passenger information in the treeview widget
        self.load_passenger_info()

        # Create a frame for the seat map
        self.seat_map_frame = tk.LabelFrame(self.seats_picker_window, text="Seat Map")
        self.seat_map_frame.grid(row=2, column=0, padx=20)


        self.seats_frame = tk.Frame(self.seat_map_frame)
        self.seats_frame.grid(row=3, column=1)

        # Seat color legend frame and lables
        self.legend_frame = tk.Frame(self.seat_map_frame)
        self.legend_frame.grid(row=0, column=0, columnspan=2, sticky=tk.W)

        self.legend_business_seat = tk.Label(self.legend_frame, text="", width=1, height=1, highlightthickness=2,
                                             highlightbackground=const.BUSINESS_SEAT_COLOR, padx=1)
        self.legend_business_seat.grid(row=0, column=0, padx=2, pady=2)

        self.legend_business_seat_label = tk.Label(self.legend_frame, text="Business", anchor=tk.W)
        self.legend_business_seat_label.grid(row=0, column=1, padx=2, pady=2)

        self.legend_comfort_seat = tk.Label(self.legend_frame, text="", width=1, height=1, highlightthickness=2,
                                            highlightbackground=const.COMFORT_SEAT_COLOR, padx=1)
        self.legend_comfort_seat.grid(row=0, column=2, padx=2, pady=2)

        self.legend_comfort_seat_label = tk.Label(self.legend_frame, text="Comfort", anchor=tk.W)
        self.legend_comfort_seat_label.grid(row=0, column=3, padx=2, pady=2)

        self.legend_economy_seat = tk.Label(self.legend_frame, text="", width=1, height=1, highlightthickness=2,
                                            highlightbackground=const.ECONOMY_SEAT_COLOR, padx=1)
        self.legend_economy_seat.grid(row=0, column=4, padx=2, pady=2)

        self.legend_business_seat_label = tk.Label(self.legend_frame, text="Economy", anchor=tk.W)
        self.legend_business_seat_label.grid(row=0, column=5, padx=2, pady=2)

        self.legend_occupied_seat = tk.Label(self.legend_frame, text="", bg=const.OCCUPIED_SEAT_COLOR,
                                            width=1, height=1, highlightthickness=2, padx=1)
        self.legend_occupied_seat.grid(row=1, column=0, padx=2, pady=2)

        self.legend_occupied_seat_label = tk.Label(self.legend_frame, text="Occupied", anchor=tk.W)
        self.legend_occupied_seat_label.grid(row=1, column=1, padx=2, pady=2)

        self.legend_available_seat = tk.Label(self.legend_frame, text="", bg=const.VACANT_SEAT_COLOR,
                                             width=1, height=1, highlightthickness=2, padx=1)
        self.legend_available_seat.grid(row=1, column=2, padx=2)

        self.legend_available_seat_label = tk.Label(self.legend_frame, text="Available", anchor=tk.W)
        self.legend_available_seat_label.grid(row=1, column=3, padx=2)

        self.legend_selected_seat = tk.Label(self.legend_frame, text="", bg=const.SELECTED_SEAT_COLOR,
                                              width=1, height=1, highlightthickness=2, padx=1)
        self.legend_selected_seat.grid(row=1, column=4, padx=2)

        self.legend_selected_seat_label = tk.Label(self.legend_frame, text="Selected", anchor=tk.W)
        self.legend_selected_seat_label.grid(row=1, column=5, padx=2)

        # Additional frames for visual representation of the aircraft outline
        self.right_wing_frame = tk.Frame(self.seat_map_frame)
        self.right_wing_frame.grid(row=2, column=1, pady=10)
        self.left_wing_frame = tk.Frame(self.seat_map_frame)
        self.left_wing_frame.grid(row=4, column=1, pady=10)
        self.nose_frame = tk.Frame(self.seat_map_frame)
        self.nose_frame.grid(row=3, column=0)
        self.tail_frame = tk.Frame(self.seat_map_frame)
        self.tail_frame.grid(row=2, column=2, padx=(0, 10), rowspan=3)

        # Button for booking selected seat
        self.book_seat_button = tk.Button(self.seats_picker_window, text="Book Seat", padx=10,
                                          command=lambda: (self.book_seat(), self.seats_picker_window.destroy()))
        self.book_seat_button.grid(row=3, column=0, sticky=tk.E, padx=100, pady=20)

        # Dictionaries to store labels with their corresponding names and seat types
        self.labels = {}
        self.seat_types = {}


    def load_passenger_info(self):
        """Load and display passenger information in the treeview."""
        self.conn = sqlite3.connect(const.DATABASE_PATH)
        self.cur = self.conn.cursor()
        self.cur.execute(f"""SELECT passenger_id, first_name, last_name, email, street_number, street, city, zip, countries.country 
                        FROM passengers
                        JOIN countries ON countries.country_id = passengers.country_id
                        WHERE passenger_id = ?
                        """, (self.passenger_id,))
        record = self.cur.fetchone()
        self.conn.close()
        # Insert fetched data into the treeview
        self.passenger_information_tree.insert(parent="", index="end", iid=1, text="", values=(
            record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8]))

    def change_occupied_seats_color(self):
        """Change the color of occupied seats."""
        self.conn = sqlite3.connect(const.DATABASE_PATH)
        self.cur = self.conn.cursor()
        self.cur.execute(f"""SELECT boarding_passes.seat_no
                            FROM flights
                            JOIN ticket_flights ON ticket_flights.flight_id = flights.flight_id
                            JOIN boarding_passes ON boarding_passes.ticket_no = ticket_flights.ticket_no AND flights.flight_id = boarding_passes.flight_id
                            WHERE flights.flight_id = ?
                        """, (self.flight_id,))
        self.records = self.cur.fetchall()
        self.occupied_seats = len(self.records)
        self.conn.close()

        # Change the color of occupied seats in the seat map
        for record in self.records:
            seat_number = record[0].lower()
            if seat_number in self.labels:
                self.labels[seat_number].config(bg=const.OCCUPIED_SEAT_COLOR, fg="grey60", highlightbackground="grey60")

    def book_seat(self):
        """Book the selected seat."""
        # Retrieve the selected seat
        self.selected_seat = self.selected_seats[0]

        # Generate booking reference
        self.book_ref = self.generate_book_ref()

        # Generate timestamp
        self.dt = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))
        self.timestamp = self.dt.strftime('%Y-%m-%d %H:%M:%S+03')

        # Determine seat type and price
        self.seat_type = self.seat_types.get(self.selected_seat.lower())
        if self.seat_type == "Business":
            self.price = const.BUSINESS_SEAT_PRICE
        elif self.seat_type == "Economy":
            self.price = 1111  # Placeholder value, replace with actual economy seat price
        elif self.seat_type == "Comfort":
            self.price = 4444  # Placeholder value, replace with actual comfort seat price

        # Book the seat
        self.conn = sqlite3.connect(const.DATABASE_PATH)
        self.cur = self.conn.cursor()
        self.cur.execute(f"""INSERT INTO tickets (book_ref, passenger_id)
                        VALUES (?, ?)
                            """, (self.book_ref, self.passenger_id))

        self.cur.execute(f"""INSERT INTO bookings (book_ref, total_amount, book_date)
                            VALUES (?, ?, ?)
                                """, (self.book_ref, self.price, self.timestamp))

        self.cur.execute(f"""SELECT ticket_no FROM tickets WHERE passenger_id = ? AND book_ref = ?
                                        """, (self.passenger_id, self.book_ref))
        self.ticket_number = self.cur.fetchone()[0]

        self.cur.execute(f"""INSERT INTO boarding_passes (ticket_no, flight_id, boarding_no, seat_no)
                                    VALUES (?, ?, ?, ?)
                                        """, (self.ticket_number, self.flight_id, self.occupied_seats + 1, self.selected_seat))

        self.cur.execute(f"""INSERT INTO ticket_flights (ticket_no, flight_id, fare_conditions, amount)
                                            VALUES (?, ?, ?, ?)
                                                """,
                    (self.ticket_number, self.flight_id, self.seat_type, self.price))
        self.conn.commit()
        self.conn.close()


    def toggle_background_color(self, event):
        """Toggle the background color of the clicked label."""
        # Get the name of the clicked label
        self.label_name = event.widget.label_name
        self.selected_seats = [label_name for label_name in self.labels if self.labels[label_name]["bg"] == const.SELECTED_SEAT_COLOR]

        # Change the background color of the clicked label
        if self.labels[self.label_name]["bg"] == const.VACANT_SEAT_COLOR:
            if not self.selected_seats:
                self.labels[self.label_name].config(bg=const.SELECTED_SEAT_COLOR)
                self.selected_seats.append(self.label_name.upper())
            else:
                # If there is already a blue label, change it back to green
                # and add the new label in blue
                self.labels[self.selected_seats[0]].config(bg=const.VACANT_SEAT_COLOR)
                self.labels[self.label_name].config(bg=const.SELECTED_SEAT_COLOR)
                self.selected_seats[0] = self.label_name.upper()

    def on_label_click(self, event):
        """Handle label click event."""
        self.toggle_background_color(event)

    def business_seat(self, grid_row: int, grid_column: int, aisle: str, seat_number: int, frame=None) -> None:
        """Create a business class seat label."""
        # Create and configure seat label
        if frame is None:
            frame = self.seats_frame
        self.label_name = f"{seat_number}{aisle}"
        self.seat = tk.Label(frame, text=aisle.upper(), bg=const.VACANT_SEAT_COLOR,
                             width=3, height=2, highlightthickness=3, highlightbackground=const.BUSINESS_SEAT_COLOR, padx=1)
        self.seat.grid(row=grid_row, column=grid_column, padx=4)
        self.seat.bind("<Button-1>", self.on_label_click)
        self.seat.label_name = self.label_name
        # Add label to the dictionaries
        self.labels[self.label_name] = self.seat
        self.seat_types[self.label_name] = "Business"

    def comfort_seat(self, grid_row: int, grid_column: int, aisle: str, seat_number: int, frame=None) -> None:
        """Create a comfort class seat label."""
        # Create and configure seat label
        if frame is None:
            frame = self.seats_frame
        self.label_name = f"{seat_number}{aisle}"
        self.seat = tk.Label(frame, text=aisle.upper(), bg=const.VACANT_SEAT_COLOR,
                     width=2, height=1, highlightthickness=3, highlightbackground=const.COMFORT_SEAT_COLOR, padx=1)
        self.seat.grid(row=grid_row, column=grid_column, padx=2, pady=4)
        self.seat.bind("<Button-1>", self.on_label_click)
        self.seat.label_name = self.label_name
        # Add label to the dictionaries
        self.labels[self.label_name] = self.seat
        self.seat_types[self.label_name] = "Comfort"

    def economy_seat(self, grid_row: int, grid_column: int, aisle: str, seat_number: int, frame=None, padx=None) -> None:
        """Create a economy class seat label."""
        # Create and configure seat label
        if frame is None:
            frame = self.seats_frame
        if padx is None:
            padx = 2
        self.label_name = f"{seat_number}{aisle}"
        self.seat = tk.Label(frame, text=aisle.upper(), bg=const.VACANT_SEAT_COLOR,
                     width=2, height=1, highlightthickness=2, highlightbackground=const.ECONOMY_SEAT_COLOR, padx=1)
        self.seat.grid(row=grid_row, column=grid_column, padx=padx, pady=4)
        self.seat.bind("<Button-1>", self.on_label_click)
        self.seat.label_name = self.label_name
        # Add label to the dictionaries
        self.labels[self.label_name] = self.seat
        self.seat_types[self.label_name] = "Economy"


    def generate_book_ref(self):
        """Generate a unique booking reference."""
        conn = sqlite3.connect(const.DATABASE_PATH)
        cur = conn.cursor()
        cur.execute(f"""SELECT book_ref FROM bookings""")
        records = set(cur.fetchall())
        conn.close()

        book_ref = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

        # Check if the generated reference is unique
        if book_ref in records:
            return self.generate_book_ref()
        else:
            return book_ref
