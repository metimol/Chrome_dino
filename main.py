import pygame
import sys
import random
import time
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
GROUND_HEIGHT = 40
INITIAL_SPEED = 5
SPEED_INCREASE_RATE = 0.01  # pixels per frame

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
            pygame.mixer.Sound('sounds/jump.wav').play()
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

    def update(self, speed):
        self.rect.x -= speed
        if self.rect.right <= 0:
            self.rect.left = WIDTH

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x_pos):
        super().__init__()
        self.image = load_image(f'images/cactus_images/{random.randint(0, 2)}.png', (60, 60))
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT - GROUND_HEIGHT
        self.rect.left = x_pos

    def update(self, speed):
        self.rect.x -= speed
        if self.rect.right <= 0:
            self.kill()

class ObstacleManager:
    def __init__(self):
        self.obstacles = pygame.sprite.Group()
        self.last_obstacle_time = time.time()

    def update(self, speed):
        current_time = time.time()
        if current_time - self.last_obstacle_time > random.uniform(1, 2):
            self.spawn_obstacle()
            self.last_obstacle_time = current_time

        for obstacle in self.obstacles:
            obstacle.update(speed)

    def spawn_obstacle(self):
        x_pos = WIDTH + random.randint(OBSTACLE_MIN_DISTANCE, OBSTACLE_MAX_DISTANCE)
        obstacle = Obstacle(x_pos)
        self.obstacles.add(obstacle)

def main():
    # Initialize screen and clock
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chrome Dino Game')
    clock = pygame.time.Clock()

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    ground_sprites = pygame.sprite.Group()

    # Create sprite instances
    dino = Dino()
    ground1 = Ground(0)
    ground2 = Ground(WIDTH)
    all_sprites.add(dino)
    ground_sprites.add(ground1, ground2)

    # Create obstacle manager
    obstacle_manager = ObstacleManager()

    # Game loop variables
    score = 0
    game_speed = INITIAL_SPEED
    running = True
    start_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    dino.jump()

        # Update game speed
        elapsed_time = time.time() - start_time
        game_speed = INITIAL_SPEED + elapsed_time * SPEED_INCREASE_RATE

        # Update sprites
        all_sprites.update()
        ground_sprites.update(game_speed)
        obstacle_manager.update(game_speed)

        # Check for collisions
        if pygame.sprite.spritecollideany(dino, obstacle_manager.obstacles):
            running = False
            pygame.mixer.Sound('sounds/end.wav').play()

        # Draw everything
        screen.fill(BACKGROUND)
        ground_sprites.draw(screen)
        all_sprites.draw(screen)
        obstacle_manager.obstacles.draw(screen)

        # Display the score
        score = int(elapsed_time * 10)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()