import pygame
from configs import *
from random import randint

class Wind(pygame.sprite.Sprite):
    def __init__(self, plane, level, upgrade):
        super().__init__()
        pygame.init()
        self.images = Wind.loadImages()
        self.image = self.images[0]
        self.plane = plane
        self.level = level
        self.upgrade = upgrade
        self.animVal = 0
        self.animDelay = 3
        self.index = 0
        heightFactor = -(self.level.verticalScroll // HEIGHT)
        self.windfx = pygame.mixer.Sound(f"{CWD}/assets/soundEffects/windfx.mp3")
        self.initX = WIDTH + WIDTH/2
        self.initY = randint(HEIGHT * (heightFactor - 1), HEIGHT * (heightFactor + 2))
        self.pos = pygame.Vector2(self.initX, self.initY)
        self.rect = self.image.get_rect(center = self.pos)

    def update(self):
        self.rect.center = (self.pos)
        self.pos[1] = self.initY + self.level.verticalScroll
        self.pos += pygame.Vector2(-self.plane.xSpeed, 0)
        self.imageAnimate()
        self.onScreenCheck()
        self.collisionCheck()

    def collisionCheck(self):
        if pygame.sprite.collide_rect(self, self.plane):
            self.kill()
            self.windfx.play()
            if self.plane.angle > 0:
                self.plane.initXSpeed *= (1.4 + 0.04 * self.upgrade)
                self.plane.ySpeed *= (1.3 + 0.03 * self.upgrade)

            elif self.plane.angle < 0:
                self.plane.initXSpeed *= (1.4 + 0.04 * self.upgrade)
                self.plane.ySpeed *= (-0.6 - 0.03 * self.upgrade)

    def onScreenCheck(self):
        if self.pos[0] < 0:
            self.kill()

    def imageAnimate(self):
        self.animVal += 1
        self.image = self.images[self.index]
        self.index = (self.animVal // self.animDelay) % len(self.images)

    @staticmethod
    def loadImages():
        imgs = []
        for i in range(1, 11):
            image = pygame.image.load(f"{CWD}/assets/windImages/windGust{i}.png").convert_alpha()
            image = pygame.transform.scale(image, (100,100))
            imgs.append(image)
        return imgs