from tkinter import colorchooser
from tkinter import ttk
from configparser import ConfigParser


parser = ConfigParser()
parser.read("main.ini")
saved_primary_color = parser.get("colors", "primary_color")
saved_secondary_color = parser.get("colors", "secondary_color")
saved_highlight_color = parser.get("colors", "highlight_color")




def primary_color(passengers_tree, scheduled_flights_tree, passengers_on_flight_tree):
    primary_color = colorchooser.askcolor()[1]
    if primary_color:
        passengers_tree.tag_configure("evenrow", background=primary_color)
        scheduled_flights_tree.tag_configure("evenrow", background=primary_color)
        passengers_on_flight_tree.tag_configure("evenrow", background=primary_color)

        parser.read("main.ini")

        parser.set("colors", "primary_color", primary_color)

        with open("main.ini", "w") as configfile:
            parser.write(configfile)


def secondary_color(passengers_tree, scheduled_flights_tree, passengers_on_flight_tree):
    secondary_color = colorchooser.askcolor()[1]
    if secondary_color:
        passengers_tree.tag_configure("oddrow", background=secondary_color)
        scheduled_flights_tree.tag_configure("oddrow", background=secondary_color)
        passengers_on_flight_tree.tag_configure("oddrow", background=secondary_color)

        parser.read("main.ini")

        parser.set("colors", "secondary_color", secondary_color)

        with open("main.ini", "w") as configfile:
            parser.write(configfile)


def treeview_highlight_color(style):
    highlight_color = colorchooser.askcolor()[1]
    if highlight_color:
        style.map("Treeview", background=[("selected", highlight_color)])

        parser.read("main.ini")

        parser.set("colors", "highlight_color", highlight_color)

        with open("main.ini", "w") as configfile:
            parser.write(configfile)


def reset_colors(style, passengers_tree, scheduled_flights_tree, passengers_on_flight_tree):
    parser.read("main.ini")

    parser.set("colors", "primary_color", "white")
    parser.set("colors", "secondary_color", "#EEF2FF")
    parser.set("colors", "highlight_color", "#222277")

    with open("main.ini", "w") as configfile:
        parser.write(configfile)

    passengers_tree.tag_configure("evenrow", background="white")
    passengers_tree.tag_configure("oddrow", background="#EEF2FF")
    scheduled_flights_tree.tag_configure("evenrow", background="white")
    scheduled_flights_tree.tag_configure("oddrow", background="#EEF2FF")
    passengers_on_flight_tree.tag_configure("evenrow", background="white")
    passengers_on_flight_tree.tag_configure("oddrow", background="#EEF2FF")
    style.map("Treeview", background=[("selected", "#222277")])