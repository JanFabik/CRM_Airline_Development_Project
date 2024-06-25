import sqlite3

MAIN_ICON = "Icons/airplane.ico"
ERROR_ICON = "Icons/error_icon_48px.png"
INFORMATION_ICON = "Icons/information_icon_48px.png"
QUESTIONMARK_ICON = "Icons/questionmark_icon_48px.png"
DROP_DOWN_ICON = "Icons/dropdown_menu_arrow.png"

DATABASE_PATH = "Databases/travel_test.sqlite"
PASSENGERS_TAB_TREEVIEW_RECORD_LIMIT = 20

BUSINESS_SEAT_PRICE = 9999
COMFORT_SEAT_PRICE = 4444
ECONOMY_SEAT_PRICE = 1111

BUSINESS_SEAT_COLOR = "gold2"
COMFORT_SEAT_COLOR = "DeepPink2"
ECONOMY_SEAT_COLOR = "blue2"

OCCUPIED_SEAT_COLOR = "lightgray"
VACANT_SEAT_COLOR = "Spring Green3"
SELECTED_SEAT_COLOR = "cyan"

def countries_list():
    """Fetch a list of countries from the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()
    cur.execute("""SELECT country FROM countries""")
    countries = [row[0] for row in cur.fetchall()]
    conn.close()

    return countries


def airports_list():
    """Fetch s list of airports from the database. Each value consists of airport name and airport code."""
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()
    cur.execute("""SELECT airport_name || ' (' || airport_code || ')' as airport FROM airports_data ORDER BY airport_name""")
    airports = [row[0] for row in cur.fetchall()]
    conn.close()

    return airports


def aircrafts_list():
    """Fetch s list of aircraft models from the database. Each value consists of aircraft name and aircraft code."""
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()
    cur.execute("""SELECT model || ' (' || aircraft_code || ')' as aircraft FROM aircrafts_data ORDER BY model""")
    aircrafts = [row[0] for row in cur.fetchall()]
    conn.close()

    return aircrafts
