import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load('./visual/sprites/ui/bg.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))  # Растягиваем фон на весь экран
        
        self.curtain = pygame.image.load('./visual/sprites/ui/curtain.png').convert_alpha()
        self.curtain = pygame.transform.scale(self.curtain, (self.screen.get_width(), self.screen.get_height()))  # Масштабируем занавеску до размеров экрана
        
        self.sign = pygame.image.load('./visual/sprites/ui/sign.png').convert_alpha()
        sign_width = self.screen.get_width()
        sign_height = int(self.sign.get_height() * (sign_width / self.sign.get_width()))
        self.sign = pygame.transform.scale(self.sign, (sign_width, sign_height))

        self.panel = pygame.image.load('./visual/sprites/ui/panel.png').convert_alpha()
        self.panel = pygame.transform.scale(self.panel, (self.screen.get_width(), self.screen.get_height()))  # Масштабируем занавеску до размеров экрана
        
        self.pause_button = pygame.image.load('./visual/sprites/ui/pause.png').convert_alpha()
        self.pause_button = pygame.transform.scale(self.pause_button, (self.pause_button.get_width() * 3, self.pause_button.get_height() * 3))  # Увеличиваем кнопку в 5 раз
        self.pause_button_rect = self.pause_button.get_rect(topleft=(42, 18))  # Устанавливаем левый верхний угол кнопки в позицию (10, 10)

        self.play_button = pygame.image.load('./visual/sprites/ui/play.png').convert_alpha()
        self.play_button = pygame.transform.scale(self.play_button, (self.play_button.get_width() * 5, self.play_button.get_height() * 5))  # Увеличиваем кнопку в 5 раз
        self.play_button_rect = self.play_button.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
    
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.curtain, (0, 0))
        self.screen.blit(self.sign, (0, 0))
        self.screen.blit(self.panel, (0, 0))
        self.screen.blit(self.play_button, self.play_button_rect)
        self.screen.blit(self.pause_button, self.pause_button_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button_rect.collidepoint(event.pos):
                return "play"
        return None
