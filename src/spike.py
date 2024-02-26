import pygame
import random

class Spike(pygame.sprite.Sprite):
    def __init__(self, screen_width, height):
        super().__init__()
        self.images = [
            pygame.image.load('./visual/sprites/obj/obs1.png').convert_alpha(),
            pygame.image.load('./visual/sprites/obj/obs2.png').convert_alpha(),
            pygame.image.load('./visual/sprites/obj/obs3.png').convert_alpha()
        ]
        self.image = random.choice(self.images)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 3, self.image.get_height() * 3))  # Увеличиваем размеры в 4 раза
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = height - self.rect.height


    def update(self):
        self.rect.x -= 5
