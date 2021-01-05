# import allthe necessary functions
import random
import sys
import pygame
from pygame.locals import *

# initialize all the functions of pygame
pygame.mixer.pre_init(frequency = 44100 , size = 16 , channels =1 , buffer = 512)
pygame.init()

# function to draw floor
def draw_floor():
	gameWindow.blit(floor_surface,(floor_x_pos,450))
	gameWindow.blit(floor_surface,(floor_x_pos+336,450))

# function to creat new pipes
def create_pipe():
	temp = random.randint(150,400)
	bottomPipe = pipe_surface.get_rect(midtop=(300,temp))
	temp -= 85
	topPipe = pipe_surface.get_rect(midbottom=(300, temp))
	return bottomPipe,topPipe

# function to moves pipes
def move_pipe(pipes):
	for pipe in pipes:
		pipe.centerx -= 3
	return pipes

# function to draw pipes
def draw_pipe(pipes):
	for pipe in pipes:
		if pipe.bottom >= 512:
			gameWindow.blit(pipe_surface,pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface,False,True)
			gameWindow.blit(flip_pipe,pipe)

# in this function we check collision with pipe and surfaces
def check_collision(pipes):
	if bird_rect.centery > 1000:
		return False
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			hit_sound.play()
			return False
	if bird_rect.centery >= 438 or bird_rect.centery <= 12 :
		hit_sound.play()
		return False
	return True

# here we use rotozoom function to rotate our bird 
def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird,-bird_movement*3,1)
	return new_bird

# function to change the bird image so that we can have animation
def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (60,bird_rect.centery))
	return new_bird,new_bird_rect

def score_display(game_state):
	if game_state == "maingame":
		score_surface = game_font.render(str(int(score)),True,(255,255,255))
		score_rect = score_surface.get_rect(center = (144,50))
		gameWindow.blit(score_surface,score_rect)
	else:
		score_surface = game_font.render(f'Score : {int(score)}',True,(255,255,255))
		score_rect = score_surface.get_rect(center = (144,90))
		gameWindow.blit(score_surface,score_rect)

		high_score_surface = game_font.render(f'High Score : {int(high_score)}',True,(255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (144,50))
		gameWindow.blit(high_score_surface,high_score_rect)

		restart = game_font.render(f'Press "Space" to',True,(255,255,255))
		restart_rect = restart.get_rect(center = (144,400))
		gameWindow.blit(restart,restart_rect)
		restart = game_font.render(f'start',True,(255,255,255))
		restart_rect = restart.get_rect(center = (144,430))
		gameWindow.blit(restart,restart_rect)

		with open("high_score.txt", "w") as hs:
			hs.write(str(int(high_score)))

# declareing some basic variables for our game
score = 0
with open("high_score.txt","r") as hs:
	for i in hs:
		high_score = int(i)
gravity = 0.2
bird_movement = 1000
FPS = 100
S_WIDTH = 288
S_HEIGHT = 512
game_active = True # we created this variable to store is our game over or not if over then to restart it
gameWindow = pygame.display.set_mode((S_WIDTH,S_HEIGHT))
clock = pygame.time.Clock() # it is used to countrol fps
game_font = pygame.font.Font('/home/jayesh/Documents/Programming/Python/CompletedProject/FlappyBird/04B_19.TTF',25)
pygame.display.set_caption("Flappy Bird")

# loading images
background = ["images/background-day.png","images/background-night.png"]
bg_surface = pygame.image.load(background[0]).convert()
floor_surface = pygame.image.load("images/base.png").convert()
floor_x_pos = 0 # here we creat this so that we can move floor in left direction

bird_downflag = pygame.image.load("images/bluebird-downflap.png").convert_alpha()
bird_midflag = pygame.image.load("images/bluebird-midflap.png").convert_alpha()
bird_upflag = pygame.image.load("images/bluebird-upflap.png").convert_alpha()
bird_frames = [bird_downflag,bird_midflag,bird_upflag]
bird_index = 0
bird = bird_frames[bird_index]
bird_rect = bird.get_rect(center = (60,280)) # this command creates a rectangle around the given surface
BIRD_FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRD_FLAP,200)

pipe_color = ["images/pipe-green.png","images/pipe-red.png"]
pipe_surface = pygame.image.load(pipe_color[0]).convert()
# pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT # this event occurs automatically and events in game loop occurs on users input
pygame.time.set_timer(SPAWNPIPE,850) # set the timer to spawn the pipes

game_over_surface = pygame.image.load("images/gameover.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(144,250))
welcome_surface = pygame.image.load("images/message.png")
welcome_surface_rect = welcome_surface.get_rect(center=(144,250))

# importing sounds
flap_sound = pygame.mixer.Sound("sounds/wing.wav")
point_sound = pygame.mixer.Sound("sounds/point.wav")
score_sound = 100
die_sound = pygame.mixer.Sound("sounds/die.wav")
hit_sound = pygame.mixer.Sound("sounds/hit.wav")
swooshing = pygame.mixer.Sound("sounds/swooshing.wav")

# Game loop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == K_SPACE and game_active:
				bird_movement = 0   # here we are making it zero so that we don't have to cancle gravity 
				bird_movement -= 4
				flap_sound.play()
			# below if is for restatring the game from start
			if event.key == K_SPACE and game_active == False:
				game_active = True
				pipe_list.clear()
				bg_surface = pygame.image.load(background[random.randint(0,1)]).convert()
				pipe_surface = pygame.image.load(pipe_color[random.randint(0,1)]).convert()
				bird_movement = 0
				score = 0
				bird_rect.center = (60,280)

		if event.type == SPAWNPIPE:
			pipe_list.extend(create_pipe())

		if event.type == BIRD_FLAP:
			if bird_index < 2:
				bird_index += 1
			else:
				bird_index = 0

			bird,bird_rect = bird_animation()

	# below command will put one surface onto the other surface first argument is which image second is where to put
	gameWindow.blit(bg_surface,(0,0))
	# below if is todo some work untill we collide
	if game_active:
		bird_movement += gravity
		rotated_bird = rotate_bird(bird)
		bird_rect.centery += bird_movement
		gameWindow.blit(rotated_bird,bird_rect)

		pipe_list = move_pipe(pipe_list)
		draw_pipe(pipe_list)
		score += 0.01
		if high_score < score:
			high_score = score
		score_display("maingame")
		score_sound -= 1
		if score_sound == 0:
			point_sound.play()
			score_sound = 100
		game_active = check_collision(pipe_list)
	else:
		if bird_movement > 1000:
			gameWindow.blit(welcome_surface,welcome_surface_rect)
		else:
			gameWindow.blit(game_over_surface,game_over_rect)
		score_display("gameover")

	floor_x_pos -= 1
	draw_floor()
	if floor_x_pos <= -336: # This is to reset the floor postion so that we see continues floor
		floor_x_pos = 0

	clock.tick(FPS) # now our fps will be less than FPS
	pygame.display.update()