import tkinter as tk
from .default_seat_map_ui import SeatMap


class SeatMapCR2(SeatMap):
    """A class representing a customized seat map for a specific aircraft model layout (Bombardier CRJ-200)."""

    def __init__(self, master, passenger_id, flight_id):
        """Initialize the SeatMapCR2 object.

        Args:
            master (tk.Tk or tk.Toplevel): The master window widget.
            passenger_id (int): The ID of the passenger from whom a seat will be booked.
            flight_id (int): The ID of the flight.
        """
        super().__init__(master, passenger_id, flight_id)
        self.setup_layout()

    def setup_layout(self):
        """Set up the layout of the customized seat map."""

        # Add labels for middle aisle
        label_aisle = tk.Label(self.seats_frame, text="")
        label_aisle.grid(row=3, column=0, padx=4, pady=4)

        # Add labels for seat row numbers and economy class seats
        for i in range(1, 8):
            seat_row_number_label1 = tk.Label(self.seats_frame, text=i)
            seat_row_number_label1.grid(row=0, column=i)

            self.economy_seat(grid_row=1, grid_column=i, aisle="a", seat_number=i)
            self.economy_seat(grid_row=2, grid_column=i, aisle="b", seat_number=i)
            self.economy_seat(grid_row=4, grid_column=i, aisle="c", seat_number=i)
            self.economy_seat(grid_row=5, grid_column=i, aisle="d", seat_number=i)

            seat_row_number_label2 = tk.Label(self.seats_frame, text=i)
            seat_row_number_label2.grid(row=6, column=i)

        for i in range(18, 23):
            seat_row_number_label1 = tk.Label(self.seats_frame, text=i)
            seat_row_number_label1.grid(row=0, column=i)

            self.economy_seat(grid_row=1, grid_column=i, aisle="a", seat_number=i)
            self.economy_seat(grid_row=2, grid_column=i, aisle="b", seat_number=i)
            self.economy_seat(grid_row=4, grid_column=i, aisle="c", seat_number=i)
            self.economy_seat(grid_row=5, grid_column=i, aisle="d", seat_number=i)

            seat_row_number_label2 = tk.Label(self.seats_frame, text=i)
            seat_row_number_label2.grid(row=6, column=i)

        seat_row_number_label1 = tk.Label(self.seats_frame, text=23)
        seat_row_number_label1.grid(row=0, column=23)

        self.economy_seat(grid_row=1, grid_column=23, aisle="a", seat_number=23)
        self.economy_seat(grid_row=2, grid_column=23, aisle="b", seat_number=23)

        seat_row_number_label2 = tk.Label(self.seats_frame, text=23)
        seat_row_number_label2.grid(row=6, column=23)


        # Add canvas elements for aircraft wings, nose, and tail and draw the aircraft outline
        self.right_wing_canvas = tk.Canvas(self.right_wing_frame, width=400, height=50)
        self.right_wing_canvas.grid(row=0, column=0)
        self.right_wing_canvas.create_line(170, 0, 140, 50)
        self.right_wing_canvas.create_line(330, 0, 310, 50)

        self.left_wing_canvas = tk.Canvas(self.left_wing_frame, width=400, height=50)
        self.left_wing_canvas.grid(row=0, column=0)
        self.left_wing_canvas.create_line(140, 0, 170, 50)
        self.left_wing_canvas.create_line(310, 0, 330, 50)

        self.nose_canvas = tk.Canvas(self.nose_frame, width=200, height=200)
        self.nose_canvas.grid(row=0, column=0)
        self.nose_canvas.create_line(200, 0, 60, 47)
        self.nose_canvas.create_line(200, 200, 60, 153)
        self.nose_canvas.create_arc(20, 36, 200, 164, style=tk.ARC, start=241, extent=-121)

        self.nose_canvas.create_line(100, 90, 130, 90)
        self.nose_canvas.create_line(130, 90, 160, 40)
        self.nose_canvas.create_line(160, 40, 130, 40)
        self.nose_canvas.create_line(130, 40, 100, 90)

        self.nose_canvas.create_line(100, 110, 130, 110)
        self.nose_canvas.create_line(130, 110, 160, 160)
        self.nose_canvas.create_line(160, 160, 130, 160)
        self.nose_canvas.create_line(130, 160, 100, 110)

        self.tail_canvas = tk.Canvas(self.tail_frame, width=100, height=300)
        self.tail_canvas.pack()
        self.tail_canvas.create_line(0, 50, 50, 10)
        self.tail_canvas.create_line(50, 10, 100, 10)
        self.tail_canvas.create_line(100, 10, 50, 110)

        self.tail_canvas.create_line(0, 250, 50, 290)
        self.tail_canvas.create_line(50, 290, 100, 290)
        self.tail_canvas.create_line(100, 290, 50, 190)

        self.tail_canvas.create_arc(0, 110, 100, 190, style=tk.ARC, start=90, extent=-180)

        # Change the color of occupied seats on the selected flight
        self.change_occupied_seats_color()
