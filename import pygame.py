import pygame
import sys
import random
import math

def authenticate():
    while True:
        password = input("Authentication Required. Please enter the password: ")

        if password == "10110":
            break
        else:
            print("Incorrect password. Please try again.")

authenticate()

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Missile Game")

background_color = (0, 0, 0)

white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

cell_size = 20

def draw_matrix_background():
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, white, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, white, (0, y), (width, y))

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

class Missile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        super().__init__()
        self.image = pygame.Surface((30, 10), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, red, [(0, 0), (30, 5), (0, 10)])
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.speed = 5 
        self.angle = math.atan2(target_pos[1] - start_pos[1], target_pos[0] - start_pos[0])
        self.displacement_factor = 20
        self.tail_length = 5
        self.tail = [(self.rect.centerx, self.rect.centery) for _ in range(self.tail_length)]

    def update(self):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)
        self.rect.x += random.randint(-self.displacement_factor, self.displacement_factor)
        self.rect.y += random.randint(-self.displacement_factor, self.displacement_factor)
        self.tail.append((self.rect.centerx, self.rect.centery))
        self.tail = self.tail[-self.tail_length:]

        distance_to_target = distance(self.rect.center, target_pos)
        min_distance = 50 
        if distance_to_target < min_distance:
            self.rect.x -= (min_distance - distance_to_target) * math.cos(self.angle)
            self.rect.y -= (min_distance - distance_to_target) * math.sin(self.angle)

        if self.rect.x < 0 or self.rect.x > width or self.rect.y < 0 or self.rect.y > height:
            self.rect.center = self.start_pos

class Radar(pygame.sprite.Sprite):
    def __init__(self, center, max_radius, speed):
        super().__init__()
        self.image = pygame.Surface((2 * max_radius, 2 * max_radius), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=center)
        self.center = center
        self.max_radius = max_radius
        self.speed = speed
        self.radius = 0
        self.blink_count = 0
        self.show_dot = False
        self.dot_pos = (0, 0)

    def update(self):
        self.radius += self.speed
        if self.radius > self.max_radius:
            self.radius = 0
            self.blink_count += 1
            if self.blink_count >= 10:
                self.blink_count = 0
                self.show_dot = not self.show_dot 

        self.image.fill((0, 255, 0, 0))
        pygame.draw.circle(self.image, green, (self.max_radius, self.max_radius), int(self.radius), 2)

        if self.show_dot:
            angle = math.atan2(source_pos[1] - self.center[1], source_pos[0] - self.center[0])
            self.dot_pos = (
                int(self.center[0] + (self.max_radius - 5) * math.cos(angle)),
                int(self.center[1] + (self.max_radius - 5) * math.sin(angle))
            )
            pygame.draw.circle(self.image, white, self.dot_pos, 3)

source_pos = (100, height // 2)
target_pos = (width - 100, height // 2)
missile = Missile(source_pos, target_pos)

all_sprites = pygame.sprite.Group()
all_sprites.add(missile)

green_point = (width - 150, height // 2)

radar = Radar(green_point, 100, 3)
all_sprites.add(radar)

running = True
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
heading_font = pygame.font.Font(None, 48)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)
    draw_matrix_background()

    heading_text = heading_font.render("Trishul - Advanced Missile Defense System", True, white)
    screen.blit(heading_text, (width // 2 - heading_text.get_width() // 2, 10))

    all_sprites.update()

    if distance(missile.rect.center, (width - 50, height // 2)) < 20:
        missile.rect.center = source_pos

    pygame.draw.lines(screen, red, False, missile.tail, 2)

    pygame.draw.circle(screen, blue, (50, height // 2), 5)
    pygame.draw.circle(screen, red, (width - 50, height // 2), 5)
    pygame.draw.circle(screen, green, green_point, 5)

    source_label = font.render("Source", True, white)
    target_label = font.render("Target", True, white)
    screen.blit(source_label, (10, height // 2 - 50))
    screen.blit(target_label, (width - 110, height // 2 - 50))

    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
