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

        # Установка размеров экрана
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Infinity Runner")

        # Загрузка изображений для фона и земли
        self.background = pygame.image.load('./visual/sprites/obj/bg.png').convert()
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Создание игрока
        self.player = Player()
        
        self.spike_spawn_interval = 250  
        self.spike_spawn_timer = 0

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


    def run(self):
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

            self.main_menu.draw()
            pygame.display.flip()
            self.clock.tick(60)

        # Запуск игры
                                
    def run_death_animation(self):
        pygame.time.set_timer(pygame.USEREVENT, 1200)
        
    def start_game(self):
        
        self.ground_1.start()
        self.ground_2.start()
        self.collision = False

        pygame.display.set_caption("Infinity Runner")  # Установка заголовка окна
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
                elif event.type == pygame.USEREVENT:
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                    self.run()


            if self.player.check_collision(self.spike_group):
                for spike in self.spike_group:
                    spike.kill()  # Убираем все шипы
                self.ground_1.stop()
                self.ground_2.stop()

                self.player.change_animation("death")  # Запускаем анимацию смерти
                self.collision = True
                self.run_death_animation()

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

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
