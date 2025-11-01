import pygame
import button
import csv

from file_handler import initialize_world_data, load_file, save_file, save_text_file
from tile_data import TILE_DATA

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#game window
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024
LOWER_MARGIN = 100
SIDE_MARGIN = 600

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Super One Nation Under God Maker 2')


#define game variables
ROWS = 64
MAX_COLS = 64
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
level = "Ice is Fun!"
floor = 1
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1


#load images
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()
#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'img/tile/{x}.png').convert_alpha()
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)

save_img = pygame.image.load('img/save_btn.png').convert_alpha()
load_img = pygame.image.load('img/load_btn.png').convert_alpha()


#define colours
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

#define font
font = pygame.font.SysFont('Futura', 30)

#create empty tile list
world_data = initialize_world_data(ROWS, MAX_COLS)

#create ground
for tile in range(0, MAX_COLS):
	world_data[ROWS - 1][tile] = 0


#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


#create function for drawing background
def draw_bg():
	screen.fill((0, 0, 0))
	# width = sky_img.get_width()
	# for x in range(4):
	# 	screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
	# 	screen.blit(mountain_img, ((x * width) - scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
	# 	screen.blit(pine1_img, ((x * width) - scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
	# 	screen.blit(pine2_img, ((x * width) - scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

#draw grid
def draw_grid():
	#vertical lines
	for c in range(MAX_COLS + 1):
		pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
	#horizontal lines
	for c in range(ROWS + 1):
		pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


#function for drawing the world tiles
def draw_world():
	for y, row in enumerate(world_data):
		for x, tile in enumerate(row):
			if tile >= 0:
				screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))



#create buttons
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
#make a button list
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
	tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 2)
	button_list.append(tile_button)
	button_col += 1
	if button_col == 6:
		button_row += 1
		button_col = 0

world_data = load_file("level", floor)

run = True
while run:

	clock.tick(FPS)

	draw_bg()
	draw_grid()
	draw_world()

	draw_text(f'Floor: {floor}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
	draw_text('Press UP or DOWN to change floor', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

	#save and load data
	if save_button.draw(screen):
		#save level data
		save_file(world_data, "level", floor)
		save_text_file("level")
	if load_button.draw(screen):
		#load in level data
		#reset scroll back to the start of the level
		scroll = 0
		world_data = load_file("level", floor)
				

	#draw tile panel and tiles
	pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

	#choose a tile
	button_count = 0
	for button_count, i in enumerate(button_list):
		if i.draw(screen):
			current_tile = button_count

	#highlight the selected tile
	pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

	# Show the current tile's name
	draw_text(f'Current Tile: {TILE_DATA[current_tile]["name"]}', font, WHITE, SCREEN_WIDTH + 10, 10)

	#scroll the map
	if scroll_left == True and scroll > 0:
		scroll -= 5 * scroll_speed
	if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
		scroll += 5 * scroll_speed

	#add new tiles to the screen
	#get mouse position
	pos = pygame.mouse.get_pos()
	x = (pos[0] + scroll) // TILE_SIZE
	y = pos[1] // TILE_SIZE

	#check that the coordinates are within the tile area
	if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
		#update tile value
		if pygame.mouse.get_pressed()[0] == 1:
			if world_data[y][x] != current_tile:
				world_data[y][x] = current_tile
		if pygame.mouse.get_pressed()[2] == 1:
			world_data[y][x] = -1

	events = pygame.event.get()

	for event in events:
		if event.type == pygame.QUIT:
			run = False
		#keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP and floor < 4:
				floor += 1
				world_data = load_file(f'level{floor}_data.csv')
			if event.key == pygame.K_DOWN and floor > 1:
				floor -= 1
				world_data = load_file(f'level{floor}_data.csv')
			if event.key == pygame.K_LEFT:
				scroll_left = True
			if event.key == pygame.K_RIGHT:
				scroll_right = True
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 5


		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				scroll_left = False
			if event.key == pygame.K_RIGHT:
				scroll_right = False
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 1


	pygame.display.update()

pygame.quit()

