import pygame
from configs import *
from random import randint

class Star(pygame.sprite.Sprite):
    def __init__(self, plane, level):
        super().__init__()
        pygame.init()
        self.images = Star.loadImages()
        self.image = self.images[randint(0,7)]
        self.plane = plane
        self.level = level
        heightFactor = -(self.level.verticalScroll // HEIGHT)
        self.collectFx = pygame.mixer.Sound(f"{CWD}/assets/soundEffects/collectfx.mp3")
        self.collectFx.set_volume(0.2)
        self.initX = WIDTH + WIDTH/2
        self.initY = randint(HEIGHT * (heightFactor - 1), HEIGHT * (heightFactor + 2))
        self.pos = pygame.Vector2(self.initX, self.initY)
        self.rect = self.image.get_rect(center = self.pos)

    def update(self):
        self.rect.center = (self.pos)
        self.pos[1] = self.initY + self.level.verticalScroll
        self.pos += pygame.Vector2(-self.plane.xSpeed, 0)
        self.onScreenCheck()
        self.collisionCheck()

    def collisionCheck(self):
        if pygame.sprite.collide_rect(self, self.plane):
            pygame.event.post(pygame.event.Event(STAR_COLLECTED))
            self.collectFx.play()
            self.kill()

    def onScreenCheck(self):
        if self.pos[0] < 0:
            self.kill()

    @staticmethod
    def loadImages():
        imgs = []
        for i in range(1, 9):
            image = pygame.transform.scale(
                pygame.image.load(f"{CWD}/assets/starFiles/star{i}.png").convert_alpha(), star_sizes[i - 1]
                )
            imgs.append(image)
        return imgs