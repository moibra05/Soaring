import pygame, math
from configs import *

class Levels:
    def __init__(self, airplane, level):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.plane = airplane
        self.verticalScroll = 0
        self.level = level
        self.pics_needed = {}
        self.image_names = []
        self.images = []

        for index, image in enumerate(levels[self.level]):
            img = pygame.image.load(f"{CWD}/assets/levelBGs/{level_names[self.level]}/{image}")
            img = pygame.transform.scale(
                img, (img.get_width() * (HEIGHT / img.get_height()), HEIGHT)
                ).convert_alpha()
            self.images.append(img)
            self.pics_needed.update(
                {f"layer{index + 1}Needed": math.ceil(WIDTH / self.images[index].get_width())}
                )
            self.image_names.append(f"layer{index + 1}")
            setattr(self, f"layer{index + 1}Scroll", 0)

        pygame.mixer.music.unload()
        pygame.mixer.music.load(f"{CWD}/assets/levelMusic/{level_names[self.level]}Music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0, 1000)

    def draw(self):
        self.plane_pos_check()
        for imageIndex, image in enumerate(self.images):
            scroll = getattr(self, f"layer{imageIndex + 1}Scroll")
            for i in range(self.pics_needed[f"{self.image_names[imageIndex]}Needed"] + 1):
                if self.level == 5:
                    self.screen.blit(image, (image.get_width() * i - (scroll), 0))
                else:
                    if imageIndex == 0:
                        self.screen.blit(image, (image.get_width() * i, 0))
                    else:
                        self.screen.blit(
                            image, (image.get_width() * i - (scroll), self.verticalScroll)
                            )
            if abs(scroll) >= image.get_width():
                setattr(self, f"{self.image_names[imageIndex]}Scroll", 0)

    def plane_pos_check(self):
        if self.plane.rect.center[0] >= WIDTH/2:
            for index in range(len(levels[self.level])):
                scroll = getattr(self, f"layer{index + 1}Scroll")
                setattr(
                    self, f"layer{index + 1}Scroll", scroll + (2 * index * (self.plane.xSpeed * 0.1))
                    )

        if self.plane.posTrack[1] < HEIGHT/2:
            self.verticalScroll = abs(self.plane.posTrack[1] - HEIGHT/2)
        else:
            self.verticalScroll = 0
