import pygame

class MainMenu:
    def __init__(self, screen):
        self.font = pygame.font.Font('./fonts/Arcadepi.ttf', 24)
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

        self.logo = pygame.image.load('./visual/sprites/ui/logo.png').convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (self.logo.get_width() * 3, self.logo.get_height() * 3))  # Увеличиваем кнопку в 5 раз
        self.logo_rect = self.logo.get_rect(topleft=(self.screen.get_width() - self.logo.get_width() - 42, 18))  # Устанавливаем левый верхний угол кнопки в позицию (10, 10)

        self.play_button = pygame.image.load('./visual/sprites/ui/play.png').convert_alpha()
        self.play_button = pygame.transform.scale(self.play_button, (self.play_button.get_width() * 5, self.play_button.get_height() * 5))  # Увеличиваем кнопку в 5 раз
        self.play_button_rect = self.play_button.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
    
        self.retry_button = pygame.image.load('./visual/sprites/ui/retry.png').convert_alpha()
        self.retry_button = pygame.transform.scale(self.retry_button, (self.retry_button.get_width() * 5, self.retry_button.get_height() * 5))  # Увеличиваем кнопку в 5 раз
        self.retry_button_rect = self.retry_button.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))


        self.score = 0
        self.best_score = 0
        
        self.retry_mode = False
    def set_score(self, score, best_score):
        self.score = score
        self.best_score = best_score

    def set_retry_mode(self, mode):
        self.retry_mode = mode

    def draw(self):    
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.curtain, (0, 0))
        self.screen.blit(self.sign, (0, 0))
        self.screen.blit(self.panel, (0, 0))
        if not self.retry_mode:
            self.screen.blit(self.play_button, self.play_button_rect)
        else:
            self.screen.blit(self.retry_button, self.retry_button_rect)

        self.screen.blit(self.logo, self.logo_rect)
        # self.screen.blit(self.pause_button, self.pause_button_rect)

        score_surface = self.font.render(str(self.score), True, (255, 255, 255))
        score_rect = score_surface.get_rect()
        score_rect.centerx = 238
        score_rect.centery = 42
        self.screen.blit(score_surface, score_rect)

        best_surface = self.font.render(str(self.best_score), True, (255, 255, 255))
        best_rect = best_surface.get_rect()
        best_rect.centerx = 565
        best_rect.centery = 42
        self.screen.blit(best_surface, best_rect)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button_rect.collidepoint(event.pos):
                return "play"
        return None
