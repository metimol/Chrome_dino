import pygame, sys, random
from pygame.color import THECOLORS

pygame.init()

#***SETTINGS***
FPS = 60
JUMP = 170
BACKGROUND = THECOLORS['white']
WIDTH = 1500
HEIGHT = 900
LENGTH_ANIMATION = 4
MIN_DISTANCE = 250
MAX_DISTANCE = 800
#***END_SETTINGS***

class Tree(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(f'images/cactus_images/{random.randint(0, 2)}.png')
		self.image = pygame.transform.scale(self.image, (60, 60))
		self.rect = self.image.get_rect()
		self.rect.center = (800, 400)
	def update(self):
		self.rect.x-=5
		if self.rect.x<-50:
			self.rect.x = 5000

class Dino(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('images/dino_images/1.png')
		self.image = pygame.transform.scale(self.image, (60, 60))
		self.rect = self.image.get_rect()
		self.rect.center = (150, 400)

class Floor(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((WIDTH, 2))
		self.image.fill(THECOLORS['black'])
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH/2, 430)

all_sprites = pygame.sprite.Group()
dino, floor = Dino(), Floor()
all_sprites.add(dino, floor)
trees = []
tree_x = 400
for i in range(8):
	tree = Tree()
	tree.rect.x = tree_x+random.randint(MIN_DISTANCE, MAX_DISTANCE)
	tree_x = tree.rect.x
	all_sprites.add(tree)
	trees.append(tree)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
timer_jump, dino_image, images_timer, sound_end_col = 0, 1, 0, 0
sound_jump = pygame.mixer.Sound('sounds/jump.wav')
sound_end = pygame.mixer.Sound('sounds/end.wav')
play = True

while True:
	touch = pygame.sprite.collide_rect(dino, floor)
	
	if play:
		if touch:
			if images_timer>LENGTH_ANIMATION:
				images_timer = 0
				if dino_image<4:
					dino_image += 1
				else:
					dino_image = 1
				image = pygame.image.load(f'images/dino_images/{dino_image}.png')
				dino.image = pygame.transform.scale(image, (60, 60))
			else:
				images_timer+=1
	
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				if play:
					if touch:
						sound_jump.play()
						timer_jump = 1
	
	if timer_jump>0:
		if timer_jump<JUMP:
			timer_jump+=7
			dino.rect.y-=7
		else:
			timer_jump = 0
	else:
		if dino.rect.y<369:
			dino.rect.y+=7
	
	hits = pygame.sprite.spritecollide(dino, trees, False)
	if hits:
		play = False
		if sound_end_col==0:
			sound_end.play()
		sound_end_col = 1
	
	clock.tick(FPS)
	if play:
		all_sprites.update()
	screen.fill(BACKGROUND)
	all_sprites.draw(screen)
	pygame.display.flip()