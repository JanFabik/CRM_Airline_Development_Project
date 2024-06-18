import tkinter as tk
from .default_seat_map_ui import SeatMap


class SeatMap733(SeatMap):
    """A class representing a customized seat map for a specific aircraft model layout (Boeing 737-300)."""

    def __init__(self, master, passenger_id, flight_id):
        """Initialize the SeatMap733 object.

        Args:
            master (tk.Tk or tk.Toplevel): The master window widget.
            passenger_id (int): The ID of the passenger from whom a seat will be booked.
            flight_id (int): The ID of the flight.
        """
        super().__init__(master, passenger_id, flight_id)
        self.setup_layout()

    def setup_layout(self):
        """Set up the layout of the customized seat map."""
        # Add labels for seat row numbers and business class seats
        for i in range(1, 4):
            seat_row_number_label1 = tk.Label(self.seats_frame, text=i)
            seat_row_number_label1.grid(row=0, column=i)

            self.business_seat(grid_row=1, grid_column=i, aisle="a", seat_number=i)
            self.business_seat(grid_row=3, grid_column=i, aisle="c", seat_number=i)
            self.business_seat(grid_row=5, grid_column=i, aisle="d", seat_number=i)
            self.business_seat(grid_row=7, grid_column=i, aisle="f", seat_number=i)

            seat_row_number_label2 = tk.Label(self.seats_frame, text=i)
            seat_row_number_label2.grid(row=8, column=i)

        # Add labels for middle aisle
        label_aisle = tk.Label(self.seats_frame, text="")
        label_aisle.grid(row=4, column=0, padx=4, pady=4)

        # Add labels for seat row numbers and economy class seats
        for i in range(4, 10):
            seat_row_number_label1 = tk.Label(self.seats_frame, text=i)
            seat_row_number_label1.grid(row=0, column=i)

            self.economy_seat(grid_row=1, grid_column=i, aisle="a", seat_number=i)
            self.economy_seat(grid_row=2, grid_column=i, aisle="b", seat_number=i)
            self.economy_seat(grid_row=3, grid_column=i, aisle="c", seat_number=i)
            self.economy_seat(grid_row=5, grid_column=i, aisle="d", seat_number=i)
            self.economy_seat(grid_row=6, grid_column=i, aisle="e", seat_number=i)
            self.economy_seat(grid_row=7, grid_column=i, aisle="f", seat_number=i)

            seat_row_number_label2 = tk.Label(self.seats_frame, text=i)
            seat_row_number_label2.grid(row=8, column=i)

        seat_row_number_label1 = tk.Label(self.seats_frame, text=10)
        seat_row_number_label1.grid(row=0, column=10)

        self.economy_seat(grid_row=2, grid_column=10, aisle="b", seat_number=10)
        self.economy_seat(grid_row=3, grid_column=10, aisle="c", seat_number=10)
        self.economy_seat(grid_row=5, grid_column=10, aisle="d", seat_number=10)
        self.economy_seat(grid_row=6, grid_column=10, aisle="e", seat_number=10)

        seat_row_number_label2 = tk.Label(self.seats_frame, text=10)
        seat_row_number_label2.grid(row=8, column=10)

        for i in range(11, 24):
            seat_row_number_label1 = tk.Label(self.seats_frame, text=i)
            seat_row_number_label1.grid(row=0, column=i)

            self.economy_seat(grid_row=1, grid_column=i, aisle="a", seat_number=i)
            self.economy_seat(grid_row=2, grid_column=i, aisle="b", seat_number=i)
            self.economy_seat(grid_row=3, grid_column=i, aisle="c", seat_number=i)
            self.economy_seat(grid_row=5, grid_column=i, aisle="d", seat_number=i)
            self.economy_seat(grid_row=6, grid_column=i, aisle="e", seat_number=i)
            self.economy_seat(grid_row=7, grid_column=i, aisle="f", seat_number=i)

            seat_row_number_label2 = tk.Label(self.seats_frame, text=i)
            seat_row_number_label2.grid(row=8, column=i)


        # Add canvas elements for aircraft wings, nose, and tail and draw the aircraft outline
        self.right_wing_canvas = tk.Canvas(self.right_wing_frame, width=400, height=50)
        self.right_wing_canvas.grid(row=0, column=0)
        self.right_wing_canvas.create_line(140, 0, 80, 50)
        self.right_wing_canvas.create_line(330, 0, 310, 50)

        self.left_wing_canvas = tk.Canvas(self.left_wing_frame, width=400, height=50)
        self.left_wing_canvas.grid(row=0, column=0)
        self.left_wing_canvas.create_line(80, 0, 140, 50)
        self.left_wing_canvas.create_line(310, 0, 330, 50)

        self.nose_canvas = tk.Canvas(self.nose_frame, width=200, height=300)
        self.nose_canvas.grid(row=0, column=0)
        self.nose_canvas.create_line(200, 0, 70, 50)
        self.nose_canvas.create_line(200, 300, 70, 250)
        self.nose_canvas.create_arc(20, 36, 220, 264, style=tk.ARC, start=241, extent=-121)

        self.nose_canvas.create_line(100, 140, 130, 140)
        self.nose_canvas.create_line(130, 140, 160, 80)
        self.nose_canvas.create_line(100, 140, 130, 80)
        self.nose_canvas.create_line(130, 80, 160, 80)

        self.nose_canvas.create_line(100, 160, 130, 160)
        self.nose_canvas.create_line(130, 160, 160, 220)
        self.nose_canvas.create_line(100, 160, 130, 220)
        self.nose_canvas.create_line(130, 220, 160, 220)

        self.tail_canvas = tk.Canvas(self.tail_frame, width=100, height=500)
        self.tail_canvas.pack()
        self.tail_canvas.create_line(0, 100, 50, 10)
        self.tail_canvas.create_line(50, 10, 100, 10)
        self.tail_canvas.create_line(100, 10, 50, 200)

        self.tail_canvas.create_line(0, 400, 50, 490)
        self.tail_canvas.create_line(50, 490, 100, 490)
        self.tail_canvas.create_line(100, 490, 50, 300)

        self.tail_canvas.create_arc(0, 200, 100, 300, style=tk.ARC, start=90, extent=-180)

        # Change the color of occupied seats on the selected flight
        self.change_occupied_seats_color()
