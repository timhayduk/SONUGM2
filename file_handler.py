import csv
import os


# Maps text characters in the game map to the image ID for the level editor
TEXT_CHAR_MAPPING = {
    "#": 0,
    "i": 10,
    " ": -1,
}
# Fallback ID used in development for unrecognized characters in the game map
FALLBACK_ID = 19


def initialize_world_data(ROWS: int = 64, COLS: int = 64):
    world_data = []
    for row in range(ROWS):
        r = [-1] * COLS
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
