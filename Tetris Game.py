import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
hize = 30
hize_WIDTH = WIDTH // hize
hize_HEIGHT = HEIGHT // hize
FPS = 10
SCORE_FONT = pygame.font.Font(None, 30)
SPEED = 1

WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0 , 0, 255)

SHAPES = [
		[[1, 1, 1, 1]],
		[[1, 1, 1], [0, 1, 0]],
		[[1, 1, 1], [1, 1, 0]],
		[[1, 1, 1], [0, 1, 1]],
		[[1, 1], [1, 1]],
		[[1, 1, 0], [0, 1, 1]],
		[[0, 1, 1], [1, 1, 0]]
]

def draw_1(screen):
		for x in range(0, WIDTH, hize):
				pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
		for y in range(0, HEIGHT, hize):
				pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def create_shape():
		shape = random.choice(SHAPES)
		x = hize_WIDTH // 2 - len(shape[0]) // 2
		y = 0
		return shape, x, y

def draw(screen, shape, x, y):
		color = random.choice([BLACK, GREEN])
		for i in range(len(shape)):
				for j in range(len(shape[i])):
						if shape[i][j] == 1:
								pygame.draw.rect(screen, color, (x + j * hize, y + i * hize, hize, hize))

def check_collision(grid, shape, x, y):
		for i in range(len(shape)):
				for j in range(len(shape[i])):
						if shape[i][j] == 1:
								if x + j < 0 or x + j >= hize_WIDTH or y + i >= hize_HEIGHT or grid[y + i][x + j] != 0:
										return True
		return False

def clear_rows(grid):
		rows_cleared = 0
		for i in range(len(grid)):
				if all(grid[i]):
						grid.pop(i)
						grid.insert(0, [0] * hize_WIDTH)
						rows_cleared += 1
		return rows_cleared

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

grid = [[0] * hize_WIDTH for _ in range(hize_HEIGHT)]
shape, x, y = create_shape()
score = 0

running = True
while running:
		screen.fill(BLACK)

		for event in pygame.event.get():
				if event.type == pygame.QUIT:
						running = False

		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
				if not check_collision(grid, shape, x - 1, y):
						x -= 1
		if keys[pygame.K_RIGHT]:
				if not check_collision(grid, shape, x + 1, y):
						x += 1
		if keys[pygame.K_DOWN]:
				if not check_collision(grid, shape, x, y + 1):
						y += 1
		if keys[pygame.K_SPACE]:
				while not check_collision(grid, shape, x, y + 1):
						y += 1

		if not check_collision(grid, shape, x, y + 1):
				y += 1
		else:
				for i in range(len(shape)):
						for j in range(len(shape[i])):
								if shape[i][j] == 1:
										grid[y + i][x + j] = 1

				rows_cleared = clear_rows(grid)
				score += rows_cleared

				shape, x, y = create_shape()

				if check_collision(grid, shape, x, y):
						running = False

		for i in range(len(grid)):
				for j in range(len(grid[i])):
						if grid[i][j] == 1:
								pygame.draw.rect(screen, WHITE, (j * hize, i * hize, hize, hize))

		draw(screen, shape, x * hize, y * hize)
		draw_1(screen)




		pygame.display.flip()
		clock.tick(FPS)

pygame.quit()
