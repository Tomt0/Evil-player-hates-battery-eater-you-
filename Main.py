import sys
import pygame
import random


def main() -> None:
	pygame.init()
	WIDTH, HEIGHT = 1000, 800
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Simple Pygame App")
	clock = pygame.time.Clock()

	# batteries
	batteries_size = 30
	batteries_rect_color = (251, 239, 43)
	batteries_rect = pygame.Rect((WIDTH - batteries_size) // 2, (HEIGHT - batteries_size) // 2, batteries_size, batteries_size)
	batteries_start = (random.randint(0, WIDTH - batteries_size), random.randint(0, HEIGHT - batteries_size))
	batteries_rect = pygame.Rect(batteries_start[0], batteries_start[1], batteries_size, batteries_size)

	# Evil Player
	Evil_player_size = 45
	Evil_player_color = (0, 0, 0)
	# starting position for the evil player
	Evil_start = (0, 220)
	Evil_player_rect = pygame.Rect(Evil_start[0], Evil_start[1], Evil_player_size, Evil_player_size)
	Evil_speed = 1200  # pixels per second

	# Player
	player_size = 40
	player_color = (200, 30, 30)
	player_start = (700, 220)
	player_rect = pygame.Rect(player_start[0], player_start[1], player_size, player_size)
	speed = 900  # pixels per second
	score = 0

	running = True
	while running:
		dt = clock.tick(60) / 1000.0  # delta time in seconds

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				running = False

		keys = pygame.key.get_pressed()
		dx = dy = 0
		if keys[pygame.K_a]:
			dx -= 1
		if keys[pygame.K_d]:
			dx += 1
		if keys[pygame.K_w]:
			dy -= 1
		if keys[pygame.K_s]:       
			dy += 1
		edx = edy = 0
		if keys[pygame.K_LEFT]:
			edx -= 1
		if keys[pygame.K_RIGHT]:
			edx += 1
		if keys[pygame.K_UP]:
			edy -= 1
		if keys[pygame.K_DOWN]:
			edy += 1

		# normalize evil diagonal movement
		if edx != 0 and edy != 0:
			from math import sqrt

			inv = 1 / sqrt(2)
			edx *= inv
			edy *= inv

		# normalize diagonal movement
		if dx != 0 and dy != 0:
			from math import sqrt

			inv = 1 / sqrt(2)
			dx *= inv
			dy *= inv

		player_rect.x += int(dx * speed * dt)
		player_rect.y += int(dy * speed * dt)
		Evil_player_rect.x += int(edx * Evil_speed * dt)
		Evil_player_rect.y += int(edy * Evil_speed * dt)



		# clamp to screen
		player_rect.left = max(0, player_rect.left)
		player_rect.top = max(0, player_rect.top)
		player_rect.right = min(WIDTH, player_rect.right)
		player_rect.bottom = min(HEIGHT, player_rect.bottom)

		# EVIL clamp to screen
		Evil_player_rect.left = max(0, Evil_player_rect.left)
		Evil_player_rect.top = max(0, Evil_player_rect.top)
		Evil_player_rect.right = min(WIDTH, Evil_player_rect.right)
		Evil_player_rect.bottom = min(HEIGHT, Evil_player_rect.bottom)

		# batteries clamp to screen
		batteries_rect.left = max(0, batteries_rect.left)
		batteries_rect.top = max(0, batteries_rect.top)
		batteries_rect.right = min(WIDTH, batteries_rect.right)
		batteries_rect.bottom = min(HEIGHT, batteries_rect.bottom)

		# draw
		screen.fill((30, 30, 40))
		pygame.draw.rect(screen, player_color, player_rect)
		pygame.draw.rect(screen, Evil_player_color, Evil_player_rect)
		pygame.draw.rect(screen, batteries_rect_color, batteries_rect)

		# FPS display in caption
		fps = int(clock.get_fps()) if clock.get_fps() > 0 else 60
		pygame.display.set_caption(f"Simple Pygame App — FPS: {fps} | Score: {score}")

		pygame.display.flip()

		#NOT CLANKER STUFF

		if Evil_player_rect.colliderect(player_rect):
			score -= 1
			print("oooo evil player got you. you lost a battery. you have", score, "batteries left.")
			Evil_player_respawn = (random.randint(0, WIDTH - Evil_player_size), random.randint(0, HEIGHT - Evil_player_size))
			Evil_player_rect = pygame.Rect(Evil_player_respawn[0], Evil_player_respawn[1], Evil_player_size, Evil_player_size)
			if score < 0:
				print("you didnt eat enough batteries. :(")
				running = False
				pygame.quit()

		if player_rect.colliderect(batteries_rect):
			batteries_respawn = (random.randint(0, WIDTH - batteries_size), random.randint(0, HEIGHT - batteries_size))
			batteries_rect = pygame.Rect(batteries_respawn[0], batteries_respawn[1], batteries_size, batteries_size)
			score += 1
			print("yummy. you eaten", score, "batteries.")
		




if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print("Error running the game:", e, file=sys.stderr)
		pygame.quit()
		raise
