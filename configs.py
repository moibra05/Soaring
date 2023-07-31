import pygame
import os.path

WIDTH, HEIGHT = (960, 720)
FPS = 60
CWD = os.path.dirname(__file__)
pygame.init()

default_font = pygame.font.Font(f"{CWD}/assets/Silkscreen-Regular.ttf", 42)
in_game_font = pygame.font.Font(f"{CWD}/assets/Silkscreen-Regular.ttf", 32)
summary_font = pygame.font.Font(f"{CWD}/assets/Silkscreen-Regular.ttf", 25)
upgrade_font = pygame.font.Font(f"{CWD}/assets/Silkscreen-Regular.ttf", 17)
description_font = pygame.font.Font(f"{CWD}/assets/Silkscreen-Regular.ttf", 15)

city = [
    "citybg.png",
    "far-buildings.png",
    "back-buildings.png",
    "foreground.png"
]

factory = [
    "factorybg.png",
    "factory3.png",
    "factory2.png",
    "factory1.png"
]

underwater = [
    "underwaterbg.png",
    "far.png",
    "sand.png",
    "foreground-merged.png"
]

redMountains = [
    "sky.png", 
    "far-clouds.png", 
    "near-clouds.png", 
    "far-mountains.png", 
    "mountains.png", 
    "trees.png"
]

glacialMountains = [
    "sky.png",
    "clouds_bg.png",
    "glacial_mountains.png",
    "clouds_mg_3.png",
    "clouds_mg_2.png",
    "clouds_mg_1.png"
]

space = [
    "background_1.png",
    "background_2.png",
    "background_3.png",
    "background_4.png"
]

levels = [city, factory, underwater, redMountains, glacialMountains, space]
level_names = ["city", "factory", "underwater", "redMountains", "glacialMountains", "space"]

true_level_names = [
    "The City",
    "Factory Infinite",
    "Atlantis",
    "Mountain Dusk",
    "Himalayas",
    "Space?"
]

full_level_images = ["city.png", 
    "factory.png", 
    "underwater.png", 
    "redMountains.png",
    "glacialMountains.png", 
    "space.png"
]


level_distances = {"city": 300, 
    "factory": 400, 
    "underwater": 550, 
    "redMountains": 700, 
    "glacialMountains": 800, 
    "space": 1100
}

game_states = {"TITLE": 0, "PLAY": 1, "SUMMARY": 2, "PROGRESS": 3, "SHOP": 4, "END": 5}
airplane_states = {"STILL": 0, "FLYING": 1}

STAR_COLLECTED = pygame.USEREVENT + 0
FLIGHT_END = pygame.USEREVENT + 1
LOAD_GAME = pygame.USEREVENT + 2
NEW_GAME = pygame.USEREVENT + 3
SAVE_GAME = pygame.USEREVENT + 4
SUMMARY_CONTINUE = pygame.USEREVENT + 5
PROGRESS_CONTINUE = pygame.USEREVENT + 6
SHOP_CONTINUE = pygame.USEREVENT + 7
BEAT_LEVEL = pygame.USEREVENT + 8
GAME_END = pygame.USEREVENT + 9

star_sizes = [
    (31, 31), 
    (29.8, 26.6), 
    (40, 40), 
    (26.4, 26.4), 
    (48, 45.6), 
    (29, 26.4), 
    (31, 31), 
    (45.8, 43.4)
]