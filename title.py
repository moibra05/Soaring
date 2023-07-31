import pygame
from configs import *

class Title:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.new_game_rect = default_font.render("New Game", True, "white").get_rect(topleft = (61,303))
        self.load_game_rect = default_font.render("Load Game", True, "white").get_rect(topleft = (61,356))

        self.newGame = default_font.render("New Game", True, "white")
        self.loadGame = default_font.render("Load Game", True, "white")

        self.titleScreen = pygame.image.load(f"{CWD}/assets/gameImages/game-title-without-load.png")
        self.bgMusic = pygame.mixer.music.load(f"{CWD}/assets/levelMusic/gameMusic.mp3")
        self.selectfx = pygame.mixer.Sound(f"{CWD}/assets/soundEffects/selectfx.mp3")
        self.new_game_request = False
        pygame.mixer.music.play(-1)


    def new_game_confirm(self):
        mouse = pygame.mouse.get_pos()
        leftClick = pygame.mouse.get_pressed()[0]
        
        if 640 <= mouse[0] <= 708 and 430 <= mouse[1] <= 465:
            self.yes = in_game_font.render("Yes", True, (50,50,50))
            self.no = in_game_font.render("No", True, "white")
    
            if leftClick:
                self.selectfx.play()
                pygame.event.post(pygame.event.Event(NEW_GAME))

        elif 275 <= mouse[0] <= 325 and 430 <= mouse[1] <= 465:
            self.yes = in_game_font.render("Yes", True, "white")
            self.no = in_game_font.render("No", True, (50, 50, 50))
            if pygame.mouse.get_pressed()[0]:
                self.selectfx.play()
                self.new_game_request = False

        else:
            self.yes = in_game_font.render("Yes", True, "white")
            self.no = in_game_font.render("No", True, "white")

        self.screen.blit(self.yes, (640, 430))
        self.screen.blit(self.no, (275, 430))

    def update(self):
        mouse = pygame.mouse.get_pos()

        if 60 <= mouse[0] <= 308 and 323 <= mouse[1] <= 349:
            self.newGame = default_font.render("New Game", True, (50,50,50))
            self.loadGame = default_font.render("Load Game", True, "white")

        elif 60 <= mouse[0] <= 375 and 376 <= mouse[1] <= 402:
            self.newGame = default_font.render("New Game", True, "white")
            self.loadGame = default_font.render("Load Game", True, (50, 50, 50))

        else:
            self.newGame = default_font.render("New Game", True, "white")
            self.loadGame = default_font.render("Load Game", True, "white")

    def draw(self):
        self.screen.blit(self.titleScreen, (0,0))

        if self.new_game_request:
            confirm1 = in_game_font.render("Are you sure?", True, "white")
            confirm2 = in_game_font.render("All previous data will be overwritten.", True, "white")
            self.screen.blit(confirm1, (340,300))
            self.screen.blit(confirm2, (80,350))
            self.new_game_confirm()
        else:
            self.screen.blit(self.newGame, self.new_game_rect)
            self.screen.blit(self.loadGame, self.load_game_rect)


