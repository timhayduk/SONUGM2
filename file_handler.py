import csv
import os

from tile_data import TILE_DATA


def initialize_world_data(ROWS: int = 64, COLS: int = 64):
    world_data = []
    for row in range(ROWS):
        r = [0] * COLS
        world_data.append(r)
    
    return world_data

def load_file(
        file_name: str,
        floor: int
    ):
    world_data = initialize_world_data()

    file_path = os.path.join("Maps", f"{file_name}_{floor}.csv")
    if not os.path.exists(file_path):
        return world_data

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)

    return world_data

def save_file(
        world_data: list[list[str]],
        file_name: str, floor: int
    ):
    with open(os.path.join("Maps", f"{file_name}_{floor}.csv"), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        for row in world_data:
            writer.writerow(row)

def convert_world_data(
        world_data: list[list[str]],
    ):
    lines = []
    for row in world_data:
        line = ""
        row_index = 64
        for col in row:
            line += TILE_DATA[col]['char']
        line += f"{row_index}\n"
        lines.append(line)

    return lines

def save_text_file(
        file_name: str
    ):
    # Load and export the first floor
    world_data = load_file(file_name, floor=1)
    lines = []
    lines.append(f"; {file_name}\n")
    lines.append(f"0\n")
    lines.append(f"; 1st Floor\n")
    lines.extend(convert_world_data(world_data))

    # Load and export the second floor
    world_data = load_file(file_name, floor=2)
    lines.append("; Second Floor\n")
    lines.extend(convert_world_data(world_data))

    # Load and export the third floor
    world_data = load_file(file_name, floor=3)
    lines.append("; Third Floor\n")
    lines.extend(convert_world_data(world_data))

    # Load and export the fourth floor
    world_data = load_file(file_name, floor=4)
    lines.append("; Fourth Floor\n")
    lines.extend(convert_world_data(world_data))

    with open(os.path.join("Maps", f"{file_name}.txt"), 'w', newline='') as textfile:
        textfile.writelines(lines)
