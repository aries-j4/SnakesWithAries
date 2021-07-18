import random
import os
import pygame
pygame.init()

pygame.mixer.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))


menuimg = pygame.image.load(r"BackImg\snakemenu.jpg")
menuimg = pygame.transform.scale(menuimg, (screen_width, screen_height)).convert_alpha()

bgimg = pygame.image.load(r"BackImg\greenbg.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

pygame.display.set_caption("SnakesWithAries")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont('Courier New', 42)

def text_screen(text, color, x, y):
	screen_text = font.render(text, True, color)
	gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow, color, snk_list, snake_size):
	for x, y in snk_list:
		pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
	exit_game = False
	pygame.mixer.music.load(r'Audio\BellaBellaBeat.mp3')
	pygame.mixer.music.play()
	while not exit_game:
		gameWindow.fill((233, 220, 229))
		gameWindow.blit(menuimg, (0, 0))
		text_screen("Welcome to Snakes", black, screen_width/4.5, screen_height/4)
		text_screen("Press Spacebar to Play!", black, screen_width/7, screen_height/3)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit_game = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					pygame.mixer.music.stop()
					gameloop()

		pygame.display.update()
		clock.tick(60)

def gameloop():

	exit_game = False
	game_over = False
	snake_x = 45
	snake_y = 55
	velocity_x = 0
	velocity_y = 0
	food_x = random.randint(20, screen_width/1.5)
	food_y = random.randint(70, screen_height/1.5)
	score = 0
	if (not os.path.exists("hiscore.txt")):
		with open("hiscore.txt", "w") as f:
				f.write("0")
	with open("hiscore.txt", "r") as f:
		hiscore = f.read()
	init_velocity = 5
	snake_size = 10
	fps = 30
	snk_list = []
	snk_length = 1

	while not exit_game:

		if game_over:

			with open("hiscore.txt", "w") as f:
				f.write(str(hiscore))
	
			gameWindow.fill((233, 220, 229))
			gameWindow.blit(menuimg, (0, 0))
			text_screen("Game Over! Press Enter to Continue", black, screen_width/30, screen_height/2.9)
			text_screen("Score: " + str(score), black, screen_width/2.9, screen_height/2)
			text_screen("Hiscore: " + str(hiscore), black, screen_width/3.5, screen_height/1.7)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit_game = True

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						gameloop()

		else:	
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit_game = True
		
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RIGHT:
						velocity_x = init_velocity
						velocity_y = 0
		
					if event.key == pygame.K_LEFT:
						velocity_x = - init_velocity
						velocity_y = 0
		
					if event.key == pygame.K_UP:
						velocity_y = - init_velocity
						velocity_x = 0
		
					if event.key == pygame.K_DOWN:
						velocity_y = init_velocity
						velocity_x = 0
		
			snake_x = snake_x + velocity_x
			snake_y = snake_y + velocity_y
		
			if abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6:
				pygame.mixer.music.load(r'Audio\scoreup.mp3')
				pygame.mixer.music.play()
				score = score + 10
				food_x = random.randint(70, screen_width/1.5)
				food_y = random.randint(70, screen_height/1.5)
				snk_length = snk_length + 5
				if score > int(hiscore):
					hiscore = score
		
			gameWindow.fill(white)
			gameWindow.blit(bgimg, (0, 0))
			text_screen("Score: " + str(score) + "        Hiscore: " + str(hiscore), red, 5, 5)
			pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
		
			head = []
			head.append(snake_x)
			head.append(snake_y)
			snk_list.append(head)
		
			if len(snk_list) > snk_length:
				del snk_list[0]
		
			if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
				pygame.mixer.music.load(r'Audio\lose.mp3')
				pygame.mixer.music.play()
				game_over = True

			if head in snk_list[:-1]:
				pygame.mixer.music.load(r'Audio\lose.mp3')
				pygame.mixer.music.play()
				game_over = True

			plot_snake(gameWindow, black, snk_list, snake_size)
		
		pygame.display.update()
		clock.tick(fps)

	pygame.quit()
	quit()
	
def main():
	welcome()

if __name__ == '__main__':
    main()