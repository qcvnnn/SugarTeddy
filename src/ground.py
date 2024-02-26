import pygame

class Ground(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load('./visual/sprites/obj/fg.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (screen_width, screen_width))
        self.rect = self.image.get_rect()
        self.rect.y = screen_height - self.rect.height
        self.rect.x = 0
        self.move = True

    def update(self):
        if self.move:
            self.rect.x -= 5
            if self.rect.right <= 0:
                self.rect.x = self.rect.width

    def stop(self):
        self.move = False  

    def start(self):
        self.move = True  

    def draw(self, screen):
        screen.blit(self.image, self.rect)
