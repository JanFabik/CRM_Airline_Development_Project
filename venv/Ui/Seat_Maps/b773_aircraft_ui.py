import tkinter as tk
from .default_seat_map_ui import SeatMap


class SeatMap773(SeatMap):
    """A class representing a customized seat map for a specific aircraft model layout (Boeing 777-300)."""

    def __init__(self, master, passenger_id, flight_id):
        """Initialize the SeatMap773 object.

        Args:
            master (tk.Tk or tk.Toplevel): The master window widget.
            passenger_id (int): The ID of the passenger from whom a seat will be booked.
            flight_id (int): The ID of the flight.
        """
        super().__init__(master, passenger_id, flight_id)
        self.setup_layout()

    def setup_layout(self):
        """Set up the layout of the customized seat map."""
        # Create frame for business seats
        self.business_seats_frame = tk.Frame(self.seats_frame)
        self.business_seats_frame.grid(row=0, column=0)
        # Add labels for seat row numbers and business class seats
        for i in range(1, 6):
            seat_row_number_label1 = tk.Label(self.business_seats_frame, text=i)
            seat_row_number_label1.grid(row=0, column=i)

            self.business_seat(frame=self.business_seats_frame, grid_row=1, grid_column=i, aisle="a", seat_number=i)
            self.business_seat(frame=self.business_seats_frame, grid_row=2, grid_column=i, aisle="c", seat_number=i)
            self.business_seat(frame=self.business_seats_frame, grid_row=3, grid_column=i, aisle="d", seat_number=i)
            self.business_seat(frame=self.business_seats_frame, grid_row=5, grid_column=i, aisle="g", seat_number=i)
            self.business_seat(frame=self.business_seats_frame, grid_row=6, grid_column=i, aisle="h", seat_number=i)
            self.business_seat(frame=self.business_seats_frame, grid_row=7, grid_column=i, aisle="k", seat_number=i)

            seat_row_number_label2 = tk.Label(self.business_seats_frame, text=i)
            seat_row_number_label2.grid(row=8, column=i)

        # Add labels for middle aisle in business class
        label_aisle_business = tk.Label(self.business_seats_frame, text="")
        label_aisle_business.grid(row=4, column=0, padx=4, pady=4)

        # Create frame for comfort seats
        self.comfort_seats_frame = tk.Frame(self.seats_frame)
        self.comfort_seats_frame.grid(row=0, column=1)

        # Add labels for seat row numbers and comfort class seats
        for i in range(11, 17):
            seat_row_number_label1 = tk.Label(self.comfort_seats_frame, text=i)
            seat_row_number_label1.grid(row=0, column=i)

            self.comfort_seat(frame=self.comfort_seats_frame, grid_row=1, grid_column=i, aisle="a", seat_number=i)
            self.comfort_seat(frame=self.comfort_seats_frame, grid_row=2, grid_column=i, aisle="c", seat_number=i)

            self.comfort_seat(frame=self.comfort_seats_frame, grid_row=5, grid_column=i, aisle="d", seat_number=i)
            self.comfort_seat(frame=self.comfort_seats_frame, grid_row=6, grid_column=i, aisle="e", seat_number=i)
            self.comfort_seat(frame=self.comfort_seats_frame, grid_row=7, grid_column=i, aisle="f", seat_number=i)
            self.comfort_seat(frame=self.comfort_seats_frame, grid_row=8, grid_column=i, aisle="g", seat_number=i)

            self.comfort_seat(frame=self.comfort_seats_frame, grid_row=11, grid_column=i, aisle="h", seat_number=i)
            self.comfort_seat(frame=self.comfort_seats_frame, grid_row=12, grid_column=i, aisle="k", seat_number=i)

            seat_row_number_label2 = tk.Label(self.comfort_seats_frame, text=i)
            seat_row_number_label2.grid(row=13, column=i)

        # Add labels for aisles in comfort class
        label_comfort_aisle1 = tk.Label(self.comfort_seats_frame, text="")
        label_comfort_aisle1.grid(row=4, column=0, padx=4, pady=4)

        label_comfort_aisle2 = tk.Label(self.comfort_seats_frame, text="")
        label_comfort_aisle2.grid(row=9, column=0, padx=4, pady=4)

        # Create frame for first section of economy seats
        self.economy_seats_frame1 = tk.Frame(self.seats_frame)
        self.economy_seats_frame1.grid(row=0, column=2)

        # Add labels for seat row numbers and economy class seats
        seat_row_number_label1 = tk.Label(self.economy_seats_frame1, text=17)
        seat_row_number_label1.grid(row=0, column=17)

        self.economy_seat(frame=self.economy_seats_frame1, grid_row=1, grid_column=17, aisle="a", seat_number=17, padx=1)
        self.economy_seat(frame=self.economy_seats_frame1, grid_row=2, grid_column=17, aisle="c", seat_number=17, padx=1)

        self.economy_seat(frame=self.economy_seats_frame1, grid_row=5, grid_column=17, aisle="d", seat_number=17, padx=1)
        self.economy_seat(frame=self.economy_seats_frame1, grid_row=6, grid_column=17, aisle="e", seat_number=17, padx=1)
        self.economy_seat(frame=self.economy_seats_frame1, grid_row=7, grid_column=17, aisle="f", seat_number=17, padx=1)
        self.economy_seat(frame=self.economy_seats_frame1, grid_row=8, grid_column=17, aisle="g", seat_number=17, padx=1)

        self.economy_seat(frame=self.economy_seats_frame1, grid_row=11, grid_column=17, aisle="h", seat_number=17, padx=1)
        self.economy_seat(frame=self.economy_seats_frame1, grid_row=12, grid_column=17, aisle="k", seat_number=17, padx=1)

        seat_row_number_label2 = tk.Label(self.economy_seats_frame1, text=17)
        seat_row_number_label2.grid(row=13, column=17)

        # Add labels for aisles in economy class
        label_economy_aisle1 = tk.Label(self.economy_seats_frame1, text="")
        label_economy_aisle1.grid(row=4, column=0, padx=4, pady=4)

        label_economy_aisle2 = tk.Label(self.economy_seats_frame1, text="")
        label_economy_aisle2.grid(row=9, column=0, padx=4, pady=4)

        for i in range (18, 24):
            seat_row_number_label1 = tk.Label(self.economy_seats_frame1, text=i)
            seat_row_number_label1.grid(row=0, column=i)

            self.economy_seat(frame=self.economy_seats_frame1, grid_row=1, grid_column=i, aisle="a", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=2, grid_column=i, aisle="b", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=3, grid_column=i, aisle="c", seat_number=i, padx=1)

            self.economy_seat(frame=self.economy_seats_frame1, grid_row=5, grid_column=i, aisle="d", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=6, grid_column=i, aisle="e", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=7, grid_column=i, aisle="f", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=8, grid_column=i, aisle="g", seat_number=i, padx=1)

            self.economy_seat(frame=self.economy_seats_frame1, grid_row=10, grid_column=i, aisle="h", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=11, grid_column=i, aisle="j", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=12, grid_column=i, aisle="k", seat_number=i, padx=1)

            seat_row_number_label2 = tk.Label(self.economy_seats_frame1, text=i)
            seat_row_number_label2.grid(row=13, column=i)

        seat_row_number_label1 = tk.Label(self.economy_seats_frame1, text=24)
        seat_row_number_label1.grid(row=0, column=24)

        self.economy_seat(frame=self.economy_seats_frame1, grid_row=5, grid_column=24, aisle="d", seat_number=24, padx=1)
        self.economy_seat(frame=self.economy_seats_frame1, grid_row=6, grid_column=24, aisle="e", seat_number=24, padx=1)
        self.economy_seat(frame=self.economy_seats_frame1, grid_row=7, grid_column=24, aisle="f", seat_number=24, padx=1)
        self.economy_seat(frame=self.economy_seats_frame1, grid_row=8, grid_column=24, aisle="g", seat_number=24, padx=1)

        seat_row_number_label2 = tk.Label(self.economy_seats_frame1, text=24)
        seat_row_number_label2.grid(row=13, column=24)

        for i in range (25, 38):
            seat_row_number_label1 = tk.Label(self.economy_seats_frame1, text=i)
            seat_row_number_label1.grid(row=0, column=i)

            self.economy_seat(frame=self.economy_seats_frame1, grid_row=1, grid_column=i, aisle="a", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=2, grid_column=i, aisle="b", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=3, grid_column=i, aisle="c", seat_number=i, padx=1)

            self.economy_seat(frame=self.economy_seats_frame1, grid_row=5, grid_column=i, aisle="d", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=6, grid_column=i, aisle="e", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=7, grid_column=i, aisle="f", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=8, grid_column=i, aisle="g", seat_number=i, padx=1)

            self.economy_seat(frame=self.economy_seats_frame1, grid_row=10, grid_column=i, aisle="h", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=11, grid_column=i, aisle="j", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=12, grid_column=i, aisle="k", seat_number=i, padx=1)

            seat_row_number_label2 = tk.Label(self.economy_seats_frame1, text=i)
            seat_row_number_label2.grid(row=13, column=i)

        seat_row_number_label1 = tk.Label(self.economy_seats_frame1, text=38)
        seat_row_number_label1.grid(row=0, column=38)

        self.economy_seat(frame=self.economy_seats_frame1, grid_row=1, grid_column=38, aisle="a", seat_number=38, padx=1)
        self.economy_seat(frame=self.economy_seats_frame1, grid_row=2, grid_column=38, aisle="b", seat_number=38, padx=1)
        self.economy_seat(frame=self.economy_seats_frame1, grid_row=3, grid_column=38, aisle="c", seat_number=38, padx=1)
        self.economy_seat(frame=self.economy_seats_frame1, grid_row=10, grid_column=38, aisle="h", seat_number=38, padx=1)
        self.economy_seat(frame=self.economy_seats_frame1, grid_row=11, grid_column=38, aisle="j", seat_number=38, padx=1)
        self.economy_seat(frame=self.economy_seats_frame1, grid_row=12, grid_column=38, aisle="k", seat_number=38, padx=1)

        seat_row_number_label2 = tk.Label(self.economy_seats_frame1, text=38)
        seat_row_number_label2.grid(row=13, column=38)

        for i in range (39, 47):
            seat_row_number_label1 = tk.Label(self.economy_seats_frame1, text=i)
            seat_row_number_label1.grid(row=0, column=i)

            self.economy_seat(frame=self.economy_seats_frame1, grid_row=1, grid_column=i, aisle="a", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=2, grid_column=i, aisle="b", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=3, grid_column=i, aisle="c", seat_number=i, padx=1)

            self.economy_seat(frame=self.economy_seats_frame1, grid_row=5, grid_column=i, aisle="d", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=6, grid_column=i, aisle="e", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=7, grid_column=i, aisle="f", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=8, grid_column=i, aisle="g", seat_number=i, padx=1)

            self.economy_seat(frame=self.economy_seats_frame1, grid_row=10, grid_column=i, aisle="h", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=11, grid_column=i, aisle="j", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=12, grid_column=i, aisle="k", seat_number=i, padx=1)

            seat_row_number_label2 = tk.Label(self.economy_seats_frame1, text=i)
            seat_row_number_label2.grid(row=13, column=i)

        for i in range(47, 51):
            seat_row_number_label1 = tk.Label(self.economy_seats_frame1, text=i)
            seat_row_number_label1.grid(row=1, column=i)

            self.economy_seat(frame=self.economy_seats_frame1, grid_row=2, grid_column=i, aisle="a", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=3, grid_column=i, aisle="c", seat_number=i, padx=1)

            self.economy_seat(frame=self.economy_seats_frame1, grid_row=5, grid_column=i, aisle="d", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=6, grid_column=i, aisle="e", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=7, grid_column=i, aisle="f", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=8, grid_column=i, aisle="g", seat_number=i, padx=1)

            self.economy_seat(frame=self.economy_seats_frame1, grid_row=10, grid_column=i, aisle="h", seat_number=i, padx=1)
            self.economy_seat(frame=self.economy_seats_frame1, grid_row=11, grid_column=i, aisle="k", seat_number=i, padx=1)

            seat_row_number_label2 = tk.Label(self.economy_seats_frame1, text=i)
            seat_row_number_label2.grid(row=12, column=i)

        seat_row_number_label1 = tk.Label(self.economy_seats_frame1, text=51)
        seat_row_number_label1.grid(row=1, column=51)

        self.economy_seat(frame=self.economy_seats_frame1, grid_row=5, grid_column=51, aisle="d", seat_number=51, padx=1)
        self.economy_seat(frame=self.economy_seats_frame1, grid_row=6, grid_column=51, aisle="e", seat_number=51, padx=1)
        self.economy_seat(frame=self.economy_seats_frame1, grid_row=7, grid_column=51, aisle="f", seat_number=51, padx=1)
        self.economy_seat(frame=self.economy_seats_frame1, grid_row=8, grid_column=51, aisle="g", seat_number=51, padx=1)

        seat_row_number_label2 = tk.Label(self.economy_seats_frame1, text=51)
        seat_row_number_label2.grid(row=12, column=51)


        # Change the color of occupied seats on the selected flight
        self.change_occupied_seats_color()
