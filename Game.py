import pygame
import sys 
import math 
from configs import *
from airplane import Airplane
from levels import Levels
from arrow import Arrow
from powerbarArrow import PowerBarArrow
from stars import Star
from wind import Wind
from title import Title
from shop import Shop
from progress_screen import Progress
from summary import Summary

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_data = [1, 0, 0, 0, 0, 0, 0, 0]
        self.game_init()
        self.init_game_assets() 
        pygame.display.set_caption("Soaring")

    def game_init(self):
        self.height_text = summary_font.render("0.0m", True, "white")
        self.velocity_text = summary_font.render("0.0m/s", True, "white")
        self.distance_text = summary_font.render("0.0m", True, "white")
        self.level_number = 0
        self.total_distance = 0
        self.total_cash = 0
        self.star_spawn_time = 0
        self.star_spawn_rate = 0.3
        self.wind_spawn_time = 0
        self.star_total = 0

    def init_game_assets(self):
        self.game_state = game_states["TITLE"]
        self.plane = Airplane()
        self.title = Title()
        self.summary = Summary(self.plane, self.star_total)
        self.shop = Shop(0, self.plane, [0,0,0,0])
        self.end_screen = pygame.image.load(f"{CWD}/assets/gameImages/end_screen.png")
        self.arrow = pygame.sprite.GroupSingle(Arrow())
        self.header = pygame.transform.scale(
            pygame.image.load(f"{CWD}/assets/gameImages/banner.png").convert_alpha(), (400, 50)
            )
        self.power_bar = pygame.image.load(f"{CWD}/assets/gameImages/powerbar.png").convert_alpha()
        self.power_rect = self.power_bar.get_rect(center = (WIDTH/2, 670))
        self.power_bar_arrow = pygame.sprite.GroupSingle(PowerBarArrow())
        self.stars = pygame.sprite.Group()
        self.wind = pygame.sprite.Group()

    def update(self):
        if self.game_state == game_states["PLAY"]: 
            self.star_spawn_time += self.clock.get_time()
            self.wind_spawn_time += self.clock.get_time()
            self.arrow.update()
            self.power_bar_arrow.update()
            self.stars.update()
            self.wind.update()
            self.plane.update(self.power_bar_arrow.sprite.powerDivide)
            self.item_spawn()

            self.height_text = summary_font.render(f"{self.plane.height/10:.1f}m", True, "white")
            self.distance_text = summary_font.render(f"{self.plane.distance:.1f}m", True, "white")
            self.velocity_text = summary_font.render(
                f"{math.sqrt(self.plane.xSpeed ** 2 + self.plane.ySpeed ** 2)/2:.1f}m/s", True, "white"
                )

            if self.plane.xSpeed > self.plane.initXSpeed and self.plane.rect.center[1] < 600:
                self.plane.xSpeed = self.plane.xSpeed - 0.005 * (self.plane.flightTime / 1000)

            if self.plane.airplane_state == airplane_states["STILL"]:
                self.total_distance += round(self.plane.distance, 1)
                self.total_cash += round((self.plane.distance) * 0.5 + self.star_total * 5, 2)
                self.stars.empty()
                self.wind.empty()

        elif self.game_state == game_states["TITLE"]:
            self.title.update()

        elif self.game_state == game_states["SHOP"]:
            self.shop.update(self.total_cash)

    def item_spawn(self):
        if self.plane.posTrack[1] <= 0:
            if (self.star_spawn_time / 1000) >= (self.star_spawn_rate - 0.02 * self.game_data[4]):
                self.stars.add(Star(self.plane, self.level))
                self.star_spawn_time = 0
            if (self.wind_spawn_time / 1000) >= 1:
                if len(self.wind) < 5:
                    self.wind.add(Wind(self.plane, self.level, self.game_data[6]))
                    self.wind_spawn_time = 0

    def screen_fade_out(self):
        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.fill((0,0,0))
        for alpha in range(0, 255):
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.delay(5)

    def screen_fade_in(self):
        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.fill((0,0,0))
        for alpha in range(0, 255, 2):
            fade.set_alpha(255 - alpha)
            self.draw()
            self.screen.blit(fade, (0,0))
            pygame.display.update()

    def game_draw(self):
        self.level.draw()
        self.plane.draw()
        self.stars.draw(self.screen)
        self.wind.draw(self.screen)
        self.screen.blit(self.header, (10,10))
        self.screen.blit(pygame.transform.flip(self.header, True, False), (550,10))
        self.screen.blit(in_game_font.render("Altitude", True, "red"), (90, 12))
        self.screen.blit(in_game_font.render("Velocity", True, "red"), (710, 12))
        self.screen.blit(summary_font.render("Distance", True, "white"), (410, 40))

        self.screen.blit(self.height_text, (285, 8))
        rect = self.distance_text.get_rect(center = (WIDTH/2, 25))
        self.screen.blit(self.distance_text, rect)
        self.screen.blit(self.velocity_text, (575, 8))

        if self.plane.airplane_state == airplane_states["STILL"] and self.game_state == game_states["PLAY"]:
            self.arrow.draw(self.screen)
            self.screen.blit(self.power_bar, self.power_rect.topleft)
            self.power_bar_arrow.draw(self.screen)
            if self.game_data[0] == 1:
                instructions1 = summary_font.render(
                    " 1. Aim arrow with mouse ", True, "white", "red"
                    )
                instructions2 = summary_font.render(
                    " 2. Time the power arrow in the center ", True, "white", "red"
                    )
                instructions3 = summary_font.render(
                    " 3. Press Space to fire plane ", True, "white", "red"
                    )
                self.screen.blit(instructions1, (240, 400))
                self.screen.blit(instructions2, (240, 450))
                self.screen.blit(instructions3, (240, 500))

    def draw(self):    
        if self.game_state == game_states["TITLE"]:
            self.title.draw()

        elif self.game_state == game_states["PLAY"]:
            self.game_draw()

        elif self.game_state == game_states["SUMMARY"]:
            self.game_draw()
            self.summary.draw()

        elif self.game_state == game_states["PROGRESS"]:
            self.progress_screen.draw()

        elif self.game_state == game_states["SHOP"]:
            self.shop.draw()

        elif self.game_state == game_states["END"]:
            end = default_font.render("The End", True, "white", "black")
            self.screen.blit(self.end_screen, (0, 0))
            self.screen.blit(end, (385, 600))

    def load_level(self):
        self.load_stats()
        self.level = Levels(self.plane, self.level_number)

    def load_stats(self):
        self.game_data = self.load_data()
        self.level_number = int(self.game_data[1])
        self.total_distance = round(float(self.game_data[2]), 1)
        self.progress_pos = 100 + (
            (self.total_distance/level_distances[level_names[self.level_number]]) * 705
            )
        self.init_progress_pos = self.progress_pos
        self.shop.upgrades = self.game_data[4:]
        self.total_cash = round(float(self.game_data[3]), 2)
        self.plane.max_speed = 15 + 2.5 * self.game_data[5] 
        self.plane.deceleration_rate = 0.01 - 0.0005 * self.game_data[7]

    def apply_upgrades(self):
        self.plane.max_speed = 15 + 2.5 * self.game_data[5] 
        self.plane.deceleration_rate = 0.01 - 0.0005 * self.game_data[7]

    def save_data(self):
        with open("save_file", "w") as file:
            file.write(f"{self.game_data[0]}\n")
            file.write(f"{self.level_number}\n")
            file.write(f"{self.total_distance}\n")
            file.write(f"{self.total_cash}\n")
            for i in range(4):
                file.write(f"{self.shop.upgrades[i]}\n")

            file.write("""
                    --------------------------------
                    CHANGE CERTAIN NUMBERS TO ALTER IN-GAME STATS AND EXPERIENCE
                    DIFFERENT PARTS OF THE GAME WITHOUT PLAYING THROUGH ITS ENTIRETY

                    NUMBERS REPRESENT THESE VALUES IN THIS ORDER:
                    ~ TUTORIAL? 0 = False, 1 = True
                    ~ LEVEL
                    ~ DISTANCE TRAVELLED - REFER TO CONFIG FILE AS TO NOT EXCEED LEVEL DISTANCE
                    ~ MONEY
                    ~ UPGRADES (MAX)
                        - Star Spawn (12)
                        - Max Speed (12)
                        - Wind Power (8)
                        - Aerodynamics (6)
                    """
                    )

    @staticmethod
    def load_data():
        data = []
        with open("save_file", "r") as file:
            for index, value in enumerate(file):
                value = value.rstrip("\n")
                if index < 4:
                    data.append(float(value))
                elif 3 < index < 8:
                    data.append(int(value))
        return data

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.game_state == game_states["TITLE"]:
                        if self.title.new_game_rect.collidepoint(event.pos):
                            self.title.selectfx.play()
                            self.title.new_game_request = True
                        if self.title.load_game_rect.collidepoint(event.pos):
                            self.title.selectfx.play()
                            pygame.event.post(pygame.event.Event(LOAD_GAME))
                    elif self.game_state == game_states["SUMMARY"]:
                        if self.summary.cont_arrow_rect.collidepoint(event.pos):
                            self.title.selectfx.play()
                            self.summary.summary_pos = pygame.Vector2(WIDTH, 60)
                            self.summary.cont_arrow_pos = pygame.Vector2(WIDTH + 360, 570)
                            pygame.event.post(pygame.event.Event(SUMMARY_CONTINUE))

                    elif self.game_state == game_states["SHOP"]:
                        if self.shop.cont_arrow_rect.collidepoint(event.pos):
                            self.shop.cont_arrow_pos = pygame.Vector2(WIDTH + 360, 570)
                            pygame.event.post(pygame.event.Event(SHOP_CONTINUE))

                        elif 139 < event.pos[0] < 298 and 238 < event.pos[1] < 397:
                            if self.total_cash >= self.shop.upgrade_costs[0] and self.shop.upgrades[0] < self.shop.max_upgrades[0]:
                                self.total_cash -= self.shop.upgrade_costs[0]
                                self.shop.upgrade(0)
                            else:
                                self.shop.errorfx.play()

                        elif 401 < event.pos[0] < 560 and 179 < event.pos[1] < 337:
                            if self.total_cash >= self.shop.upgrade_costs[1] and self.shop.upgrades[1] < self.shop.max_upgrades[1]:
                                self.total_cash -= self.shop.upgrade_costs[1]
                                self.shop.upgrade(1)
                            else:
                                self.shop.errorfx.play()

                        elif 401 < event.pos[0] < 560 and 378 < event.pos[1] < 537:
                            if self.total_cash >= self.shop.upgrade_costs[2] and self.shop.upgrades[2] < self.shop.max_upgrades[2]:
                                self.total_cash -= self.shop.upgrade_costs[2]
                                self.shop.upgrade(2)
                            else:
                                self.shop.errorfx.play()

                        elif 667 < event.pos[0] < 826 and 238 < event.pos[1] < 397:
                            if self.total_cash >= self.shop.upgrade_costs[3] and self.shop.upgrades[3] < self.shop.max_upgrades[3]:
                                self.total_cash -= self.shop.upgrade_costs[3]
                                self.shop.upgrade(3)
                            else:
                                self.shop.errorfx.play()

                elif event.type == STAR_COLLECTED:
                    self.star_total += 1
                
                elif event.type == NEW_GAME:
                    self.screen_fade_out()
                    self.game_data = [1, 0, 0, 0, 0, 0, 0, 0]
                    self.save_data()
                    pygame.mixer.music.fadeout(1500)
                    self.load_level()
                    self.game_state = game_states["PLAY"]
                    self.screen_fade_in()

                elif event.type == LOAD_GAME:
                    self.screen_fade_out()
                    pygame.mixer.music.fadeout(1500)
                    self.load_level()
                    self.game_state = game_states["PLAY"]
                    self.screen_fade_in()

                elif event.type == FLIGHT_END:
                    self.summary = Summary(self.plane, self.star_total)
                    self.game_state = game_states["SUMMARY"]

                elif event.type == SUMMARY_CONTINUE:
                    self.screen_fade_out()
                    self.star_total = 0
                    self.game_data[0] = 0
                    self.progress_screen = Progress(
                        self.plane, self.total_distance, self.level_number
                        )
                    self.game_state = game_states["PROGRESS"]
                    pygame.mixer.music.fadeout(500)
                    pygame.mixer.music.load(f"{CWD}/assets/levelMusic/gameMusic.mp3")
                    pygame.mixer.music.play(-1)

                elif event.type == PROGRESS_CONTINUE:
                    self.screen_fade_out()
                    self.plane.distance = 0
                    self.save_data()
                    self.shop = Shop(self.total_cash, self.plane, self.game_data[4:])
                    self.game_state = game_states["SHOP"]
                    self.screen_fade_in()

                elif event.type == BEAT_LEVEL:
                    self.level_number += 1
                    self.total_cash += 40 * self.level_number
                    self.total_distance = self.progress_screen.total_distance
                    self.save_data()
                    self.load_level()

                elif event.type == SHOP_CONTINUE:
                    self.screen_fade_out()
                    pygame.mixer.music.fadeout(500)
                    self.save_data()
                    self.apply_upgrades()
                    self.load_level()
                    self.game_state = game_states["PLAY"]
                    self.screen_fade_in()

                elif event.type == GAME_END:
                    self.screen_fade_out()
                    self.game_state = game_states["END"]
                    self.screen_fade_in()

            self.screen.fill("black")
            self.draw()
            self.update()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
