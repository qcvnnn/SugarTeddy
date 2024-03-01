import pygame
import random
from src.player import Player
from src.ground import Ground
from src.spike import Spike
from src.menu import MainMenu

class Game:
    def __init__(self):
        # Инициализация Pygame
        pygame.init()
        pygame.mixer.init()

        self.score = 0
        with open('./best.txt') as f:
            self.best_score = int(f.read())

        # Установка размеров экрана
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Sugar Teddy")
        pygame.display.set_icon(pygame.image.load('./visual/sprites/ui/logo.png'))

        self.font = pygame.font.Font('./fonts/Arcadepi.ttf', 24)

        # Загрузка изображений для фона и земли
        self.background = pygame.image.load('./visual/sprites/obj/bg.png').convert()
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Создание игрока
        self.player = Player()
        
        self.default_spike_spawn_interval = 500
        self.spike_spawn_timer = 0

        self.difficulty = 0

        # Создание земли
        self.spike_group = pygame.sprite.Group()
        self.collision = False  # Флаг для отслеживания столкновения с шипом
        self.death_timer = 0

        # Главный игровой цикл
        self.running = True
        self.clock = pygame.time.Clock()
        self.jumping = False
        self.jump_count = 13

        self.ground_1 = Ground(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.ground_2 = Ground(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.ground_2.rect.x = self.SCREEN_WIDTH

        self.main_menu = MainMenu(self.screen)

        self.curtain = pygame.image.load('./visual/sprites/ui/curtain.png').convert_alpha()
        self.curtain = pygame.transform.scale(self.curtain, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))  # Масштабирование занавески

        self.panel = pygame.image.load('./visual/sprites/ui/panel.png').convert_alpha()
        self.panel = pygame.transform.scale(self.panel, (self.screen.get_width(), self.screen.get_height()))  # Масштабируем занавеску до размеров экрана
        
        self.pause_button = pygame.image.load('./visual/sprites/ui/pause.png').convert_alpha()
        self.pause_button = pygame.transform.scale(self.pause_button, (self.pause_button.get_width() * 3, self.pause_button.get_height() * 3))  # Увеличиваем кнопку в 5 раз
        self.pause_button_rect = self.pause_button.get_rect(topleft=(42, 18))  # Устанавливаем левый верхний угол кнопки в позицию (10, 10)

        self.logo = pygame.image.load('./visual/sprites/ui/logo.png').convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (self.logo.get_width() * 3, self.logo.get_height() * 3))  # Увеличиваем кнопку в 5 раз
        self.logo_rect = self.logo.get_rect(topleft=(self.screen.get_width() - self.logo.get_width() - 42, 18))  # Устанавливаем левый верхний угол кнопки в позицию (10, 10)

        self.jump_sound = pygame.mixer.Sound('./sounds/jump.wav')
        self.death_sound = pygame.mixer.Sound('./sounds/death.wav')
        self.record_sound = pygame.mixer.Sound('./sounds/record.wav')

    def run(self):
        pygame.mixer.music.load('./sounds/bgmusic.wav')
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.3)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Передаем события в главное меню
                    action = self.main_menu.handle_event(event)
                    if action == "play":
                        self.running = False  # Запускаем игру
                        self.start_game()
                    elif action == "diffchange":
                        self.difficulty = (self.difficulty + 1) % 10
                        self.main_menu.update_difficulty(self.difficulty)
            self.main_menu.set_score(self.score, self.best_score)
            self.main_menu.draw()
            pygame.display.flip()
            self.clock.tick(60)

        # Запуск игры
                                
    def run_death_animation(self):
        pygame.mixer.music.stop()
        self.death_sound.play()
        pygame.time.set_timer(pygame.USEREVENT, 2200)
        
    def start_game(self):
        self.spike_spawn_interval = self.default_spike_spawn_interval // (self.difficulty+1)
       
        self.score = 0
        self.record = False

        self.ground_1.start()
        self.ground_2.start()
        self.collision = False

        self.player = Player()
        self.ground = Ground(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.spike_group = pygame.sprite.Group()
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.jumping and not self.collision:
                        self.jumping = True
                        self.jump_sound.play()
                elif event.type == pygame.USEREVENT:
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                    if self.record:
                        self.best_score = self.score
                        with open("./best.txt", "w") as f:
                            f.write(str(self.score))
                        self.record = False
                    self.run()

            if not self.collision:
                if self.player.check_collision(self.spike_group):
                    for spike in self.spike_group:
                        spike.kill()  # Убираем все шипы
                    self.ground_1.stop()
                    self.ground_2.stop()

                    self.main_menu.set_retry_mode(True)

                    self.player.change_animation("death")  # Запускаем анимацию смерти
                    self.collision = True
                    self.run_death_animation()
                else:
                    self.score += 1
                    if self.score > self.best_score and not self.record:
                        self.record = True
                        self.record_sound.play()

            if self.jumping:
                if self.jump_count >= -13:
                    neg = 1
                    if self.jump_count < 0:
                        neg = -1
                    self.player.rect.y -= (self.jump_count ** 2) * 0.2 * neg
                    self.player.collision_rect.y -= (self.jump_count ** 2) * 0.2 * neg
                    self.jump_count -= 1
                else:
                    self.jumping = False
                    self.jump_count = 13
                    if not self.collision:
                        self.player.change_animation("run")
            # Обновление земли
            self.ground_1.update()
            self.ground_2.update()

            # Отрисовка земли
            self.screen.blit(self.background, (0, 0))
            self.ground_1.draw(self.screen)
            self.ground_2.draw(self.screen)
            self.player.update()
            self.screen.blit(self.player.image, self.player.rect)

            if random.randint(1, 10) == 1:
                self.spike_spawn_timer += self.clock.get_time()  # Увеличиваем таймер спавна шипов
                if self.spike_spawn_timer >= self.spike_spawn_interval:
                    spike = Spike(self.SCREEN_WIDTH, 440)
                    self.spike_group.add(spike)
                    self.spike_spawn_timer = 0
            
            # Обновление и отрисовка шипов
            if not self.collision:
                self.spike_group.update()
                self.spike_group.draw(self.screen)

            self.screen.blit(self.curtain, (0,0))
            self.screen.blit(self.panel, (0,0))
            # self.screen.blit(self.pause_button, self.pause_button_rect)
            self.screen.blit(self.logo, self.logo_rect)

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

            difficulty_surface = self.font.render(str(self.difficulty), True, (255, 255, 255))
            self.difficulty_rect = difficulty_surface.get_rect(center=(67, 42))
            self.screen.blit(difficulty_surface, self.difficulty_rect)



            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
