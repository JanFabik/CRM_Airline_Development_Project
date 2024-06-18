import tkinter as tk
from .default_seat_map_ui import SeatMap


class SeatMapCN1(SeatMap):
    """A class representing a customized seat map for a specific aircraft model layout (Cessna 208 Caravan)."""

    def __init__(self, master, passenger_id, flight_id):
        """Initialize the SeatMapCN1 object.

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
        label_aisle.grid(row=5, column=0, padx=4, pady=4)

        # Add labels for first section of seat row numbers and economy class seats
        for i in range(1, 7):
            seat_row_number_label1 = tk.Label(self.seats_frame, text=i)
            seat_row_number_label1.grid(row=3, column=i)

            self.economy_seat(grid_row=4, grid_column=i, aisle="a", seat_number=i)
            self.economy_seat(grid_row=6, grid_column=i, aisle="b", seat_number=i)

            seat_row_number_label2 = tk.Label(self.seats_frame, text=i)
            seat_row_number_label2.grid(row=7, column=i)


        # Add canvas elements for aircraft wings, nose, and tail and draw the aircraft outline
        self.right_wing_canvas = tk.Canvas(self.right_wing_frame, width=100, height=50)
        self.right_wing_canvas.grid(row=0, column=0)
        self.right_wing_canvas.create_line(40, 0, 10, 50)
        self.right_wing_canvas.create_line(90, 0, 75, 50)

        self.left_wing_canvas = tk.Canvas(self.left_wing_frame, width=100, height=50)
        self.left_wing_canvas.grid(row=0, column=0)
        self.left_wing_canvas.create_line(10, 0, 40, 50)
        self.left_wing_canvas.create_line(90, 50, 75, 0)

        self.nose_canvas = tk.Canvas(self.nose_frame, width=140, height=100)
        self.nose_canvas.grid(row=0, column=0)
        self.nose_canvas.create_line(140, 0, 40, 20)
        self.nose_canvas.create_line(140, 100, 40, 80)
        self.nose_canvas.create_arc(15, 17, 115, 83, style=tk.ARC, start=241, extent=-121)

        self.nose_canvas.create_line(40, 45, 70, 45)
        self.nose_canvas.create_line(70, 45, 100, 20)
        self.nose_canvas.create_line(40, 45, 70, 20)
        self.nose_canvas.create_line(70, 20, 100, 20)

        self.nose_canvas.create_line(40, 55, 70, 55)
        self.nose_canvas.create_line(70, 55, 100, 80)
        self.nose_canvas.create_line(40, 55, 70, 80)
        self.nose_canvas.create_line(70, 80, 100, 80)

        self.tail_canvas = tk.Canvas(self.tail_frame, width=80, height=200)
        self.tail_canvas.pack()
        self.tail_canvas.create_line(0, 50, 50, 10)
        self.tail_canvas.create_line(50, 10, 70, 10)
        self.tail_canvas.create_line(70, 10, 50, 80)

        self.tail_canvas.create_line(0, 150, 50, 190)
        self.tail_canvas.create_line(50, 190, 70, 190)
        self.tail_canvas.create_line(70, 190, 50, 120)

        self.tail_canvas.create_arc(40, 80, 70, 120, style=tk.ARC, start=90, extent=-180)

        # Change the color of occupied seats on the selected flight
        self.change_occupied_seats_color()
