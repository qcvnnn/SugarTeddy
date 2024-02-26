import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animations = {"run": [], "death": [], "jump": []}
        self.current_animation = "run"
        self.current_sprite = 0
        self.load_animations()
        self.image = self.animations[self.current_animation][self.current_sprite]
        self.rect = self.image.get_rect()

        # self.collision_rect.move_ip(-150, 0)  

        self.rect.center = (100, 400)  # Измененная начальная позиция игрока
        self.collision_rect = pygame.Rect(0, 0, 17*3, 27*3)  # Прямоугольник коллизии игрока
        self.collision_rect.center = (self.rect.center[0]-5, self.rect.center[1])

        self.animation_speed = 5
        self.animation_counter = 0

    def load_animations(self):
        animation_files = {
            "run": "./visual/anims/run.png",
            "death": "./visual/anims/death.png",
            "jump": "./visual/anims/jump.png"
        }
        for animation_name, file_path in animation_files.items():
            sprite_sheet = pygame.image.load(file_path).convert_alpha()
            width = sprite_sheet.get_width()
            height = sprite_sheet.get_height()
            sprites = []
            for i in range(0, width, 32):
                sprite = pygame.transform.scale(sprite_sheet.subsurface(pygame.Rect(i, 0, 32, 32)), (96, 96))
                sprites.append(sprite)
            self.animations[animation_name] = sprites
        

    def update(self):
        # self.collision_rect.center = self.rect.center
        
        self.animation_counter += 1
        if self.animation_counter % self.animation_speed == 0:
            self.current_sprite = (self.current_sprite + 1) % len(self.animations[self.current_animation])
            self.image = self.animations[self.current_animation][self.current_sprite]        

    def change_animation(self, animation_name):
        if animation_name in self.animations:
            self.current_animation = animation_name
            self.current_sprite = 0
            self.image = self.animations[self.current_animation][self.current_sprite]
            self.animation_counter = 0

    def check_collision(self, sprite_group):
        collided_sprites = []
        for sprite in sprite_group:
            if self.collision_rect.colliderect(sprite.rect):
                collided_sprites.append(sprite)
        return collided_sprites
