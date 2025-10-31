import csv
import os


# Maps text characters in the game map to the image ID for the level editor
TEXT_CHAR_MAPPING = {
    "P": -1,
    "#": 0,
    "/": 1,
    "\\": 2,
    " ": 5,
    "i": 6,
    "R": 7,
    "r": 8,
    "%": 9,
    "@": 10,
    "&": 11,
    "=": 12,
}
CHAR_TEXT_MAPPING = {
    -1: "P",    # Pit
    0: "#",     # Wall
    1: "/",     # Angled Wall
    2: "\\",    # Angled Wall
    3: "/",     # Angled Wall
    4: "\\",    # Angled Wall
    5: " ",     # Floor
    6: "i",     # Ice
    7: "R",     # Stairs (Upper)
    8: "r",     # Stairs (Lower)
    9: "%",     # Flag
    10: "@",    # Start space
    11: "&",    # Statue of Liberty
    12: "=",    # Door
}
# Fallback ID used in development for unrecognized characters in the game map.
# Fallback to wall tiles, since that seems to be the default in the standard game.
FALLBACK_ID = 0


def initialize_world_data(ROWS: int = 64, COLS: int = 64):
    world_data = []
    for row in range(ROWS):
        r = [0] * COLS
        world_data.append(r)
    
    return world_data

def load_file(file_name: str):
    world_data = initialize_world_data()

    file_path = os.path.join("Maps", file_name)
    if not os.path.exists(file_path):
        return world_data

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)

    return world_data

def save_file(world_data: list[list[str]], file_name: str):
    with open(os.path.join("Maps", file_name), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        for row in world_data:
            writer.writerow(row)
