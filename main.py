import pygame
import sys
import random
from pygame.color import THECOLORS

# Initialize pygame
pygame.init()

# Settings
FPS = 60
GRAVITY = 1
JUMP_STRENGTH = -20
BACKGROUND = THECOLORS['white']
WIDTH = 800
HEIGHT = 600
DINO_RUN_ANIM_SPEED = 5
OBSTACLE_MIN_DISTANCE = 500
OBSTACLE_MAX_DISTANCE = 1200
GROUND_HEIGHT = 40

# Colors
BLACK = (0, 0, 0)

# Load assets
def load_image(path, scale=None):
    image = pygame.image.load(path)
    if scale:
        return pygame.transform.scale(image, scale)
    return image

# Classes
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [load_image(f'images/dino_images/{i}.png', (60, 60)) for i in range(1, 5)]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT - GROUND_HEIGHT
        self.rect.left = 100
        self.running_idx = 0
        self.is_jumping = False
        self.jump_speed = 0
        self.anim_timer = 0

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_speed = JUMP_STRENGTH

    def update(self):
        if self.is_jumping:
            self.rect.y += self.jump_speed
            self.jump_speed += GRAVITY
            if self.rect.bottom >= HEIGHT - GROUND_HEIGHT:
                self.rect.bottom = HEIGHT - GROUND_HEIGHT
                self.is_jumping = False
        else:
            if self.anim_timer > DINO_RUN_ANIM_SPEED:
                self.anim_timer = 0
                self.running_idx = (self.running_idx + 1) % len(self.images)
                self.image = self.images[self.running_idx]
            else:
                self.anim_timer += 1

class Ground(pygame.sprite.Sprite):
    def __init__(self, x_pos):
        super().__init__()
        self.image = load_image('images/ground.png', (WIDTH, GROUND_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect.x -= 5
        if self.rect.right <= 0:
            self.rect.left = WIDTH

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x_pos):
        super().__init__()
        self.image = load_image(f'images/cactus_images/{random.randint(0, 2)}.png', (60, 60))
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT - GROUND_HEIGHT
        self.rect.left = x_pos

    def update(self):
        self.rect.x -= 5
        if self.rect.right <= 0:
            self.rect.left = WIDTH + random.randint(OBSTACLE_MIN_DISTANCE, OBSTACLE_MAX_DISTANCE)

def main():
    # Initialize screen and clock
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chrome Dino Game')
    clock = pygame.time.Clock()

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    # Create sprite instances
    dino = Dino()
    ground1 = Ground(0)
    ground2 = Ground(WIDTH)
    all_sprites.add(dino, ground1, ground2)

    # Create initial obstacles
    for i in range(4):
        obstacle = Obstacle(WIDTH + i * 300 + random.randint(OBSTACLE_MIN_DISTANCE, OBSTACLE_MAX_DISTANCE))
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

    # Game loop
    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    dino.jump()

        # Update sprites
        all_sprites.update()

        # Check for collisions
        if pygame.sprite.spritecollideany(dino, obstacles):
            running = False
            pygame.mixer.Sound('sounds/end.wav').play()
        
        # Draw everything
        screen.fill(BACKGROUND)
        all_sprites.draw(screen)

        # Display the score
        score += 1
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()