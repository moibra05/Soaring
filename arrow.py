import pygame, math
from configs import *
 
class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.image = pygame.transform.scale(
            pygame.image.load(f"{CWD}/assets/gameImages/arrow.png").convert_alpha(), (130, 36)
            )
        self.origin = (150, 625)
        self.pivot = (0, self.image.get_height() / 2)
        self.rect = self.image.get_rect(
            topleft = (self.origin[0] - self.pivot[0], self.origin[1] - self.pivot[1])
            )
        self.orig_arrow = self.image
        self.arrow_pos = pygame.Vector2(
            self.rect.right, self.rect.topright[1] - self.image.get_height() / 2
            )

    def update(self):
        image_rect = self.orig_arrow.get_rect(
            topleft = (self.origin[0] - self.pivot[0], self.origin[1]-self.pivot[1])
            )
        offset_center_to_pivot = pygame.math.Vector2(self.origin) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-self.angle_calculation_start())
        rotated_image_center = (self.origin[0]-rotated_offset.x, self.origin[1]-rotated_offset.y)
        self.image = pygame.transform.rotate(self.orig_arrow, self.angle_calculation_start())
        self.rect = self.image.get_rect(center = rotated_image_center)

    def angle_calculation_start(self):
        x, y = pygame.mouse.get_pos()
        xCal, yCal = abs(x - self.origin[0]), abs(y - self.origin[1])

        if x > self.origin[0] and y <= self.origin[1]:
            angle = math.atan(yCal/xCal)
        elif x < self.origin[0] and y < self.origin[1]:
            angle = math.pi / 2
        elif x >= self.origin[0] and y > self.origin[1]:
            angle = 0
        else:
            angle = 0

        return ((angle * 180) / math.pi)