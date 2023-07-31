import pygame, math
from configs import *

class PowerBarArrow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.image = pygame.image.load(f"{CWD}/assets/gameImages/powerbarArrow.png")
        self.rect = self.image.get_rect(center = (WIDTH/2, 680))
        self.direction = "right"
        self.powerDivide = 0

    def update(self):
        self.arrowMove()
        self.keyPress()

    def keyPress(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.powerDivide = 2.5*(math.log(((abs((WIDTH/2) - self.rect.center[0]))/55) + 1, 3)) + 1

    def arrowMove(self):
        if self.direction == "right":
            if self.rect.right < (WIDTH/2) + 150:
                self.rect.right += 5
            else:
                self.direction = "left"
        if self.direction == "left":
            if self.rect.left > (WIDTH/2) - 150:
                self.rect.left -= 5
            else:
                self.direction = "right"
    
