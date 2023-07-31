import pygame
import math
from configs import *

class Airplane(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imgs = []
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.startPos = (140, 620)
        self.downwards = False
        for i in range(1, 5):
            img = pygame.image.load(
                f"{CWD}/assets/paper-airplane-flap-images/paperairplaneflap{i}.png"
                ).convert_alpha()
            img = pygame.transform.scale(img, (93, 36))
            self.imgs.append(img)

        self.airplane_state = airplane_states["STILL"]

        self.angle = 0
        self.xSpeed = 0
        self.initXSpeed = 0
        self.ySpeed = 0
        self.max_speed = 15
        self.deceleration_rate = 0.01
        self.flightTime = 0
        self.distance = 0
        self.height = 0
        self.animVal = 0
        self.animDelay = 7
        self.index = 0
        self.image = self.imgs[0]
        self.rect = self.image.get_rect(topright = self.startPos)
        self.posTrack = self.rect.center

    def update(self, power_divide):
        if self.airplane_state == airplane_states["STILL"]:
            self.default()
            self.angle_retrieve(power_divide)

        elif self.airplane_state == airplane_states["FLYING"]:
            self.speedCalculation()
            self.imageAnimate()

    def plane_pos_update(self, xSpeed, ySpeed):
        if self.ySpeed > 0:
            self.rect.center += pygame.Vector2(xSpeed, ySpeed)
        elif self.ySpeed < 0 and self.posTrack[1] > HEIGHT/2:
            self.rect.center += pygame.Vector2(xSpeed, abs(self.ySpeed))

    def flight_time_update(self):
        if self.flightTime / 1000 < 10:
            self.flightTime += self.clock.tick()
        else:
            self.flightTime = 10000

    def sliding_plane_update(self):
        self.posTrack += pygame.Vector2(self.xSpeed, 0)
        self.angle = 0
        self.ySpeed = 0
        self.height = 0
        self.xSpeed = self.xSpeed - 0.02 * (self.flightTime / 1000)

        if self.xSpeed <= 0:
            self.xSpeed = 0
            self.posTrack = (93, 638)
            self.airplane_state = airplane_states["STILL"]
            pygame.event.post(pygame.event.Event(FLIGHT_END))

    def speedCalculation(self):
        self.distance = (self.posTrack[0] - 93) * 0.004
        if self.posTrack[1] > 638:
            self.posTrack[1] = 638

        if self.rect.bottomright[1] < 657:
            self.flight_time_update()
            self.posTrack += pygame.Vector2(self.xSpeed, -self.ySpeed)

            self.height = abs(self.posTrack[1] - 638) / 20

            if self.rect.center[0] <= WIDTH/2 and self.rect.center[1] >= HEIGHT/2:
                self.plane_pos_update(self.xSpeed, -self.ySpeed)
            
            elif self.rect.center[0] >= WIDTH/2 and self.rect.center[1] >= HEIGHT/2:
                self.plane_pos_update(0, -self.ySpeed)

            elif self.rect.center[0] <= WIDTH/2 and self.rect.center[1] <= HEIGHT/2:
                self.plane_pos_update(self.xSpeed, 0)

            elif self.rect.center[0] >= WIDTH/2 and self.rect.center[1] <= HEIGHT/2:
                self.plane_pos_update(0, 0)

            self.ySpeed = self.ySpeed - self.deceleration_rate * (self.flightTime / 1000)
            self.angleCalculationFlight()

        else:
            self.sliding_plane_update()

    def angle_retrieve(self, powerDivide):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.clock.tick()
            self.angle = self.angleCalculationStart()
            self.xSpeed = (self.max_speed / powerDivide) * math.cos((self.angle * math.pi) / 180)
            self.ySpeed = (self.max_speed / powerDivide) * math.sin((self.angle * math.pi) / 180)
            self.initXSpeed = self.xSpeed
            self.airplane_state = airplane_states["FLYING"]

    def angleCalculationStart(self):
        x, y = pygame.mouse.get_pos()
        xCal, yCal = abs(x - self.startPos[0]), abs(y - self.startPos[1])

        if x > self.startPos[0] and y <= self.startPos[1]:
            angle = math.atan(yCal/xCal)
        elif x < self.startPos[0] and y < self.startPos[1]:
            angle = math.pi / 2
        elif x >= self.startPos[0] and y > self.startPos[1]:
            angle = 0
        else:
            angle = 0

        return ((angle * 180) / math.pi)

    def angleCalculationFlight(self):
        if self.ySpeed > 0:
            self.angle = (math.atan(abs(self.ySpeed)/self.xSpeed) * 180) / math.pi
            self.downwards = False
        else:
            self.downwards = True
        
        if self.downwards:
            self.angle = -(math.atan(abs(self.ySpeed)/self.xSpeed) * 180) / math.pi

    def default(self):
        self.rect.topright = self.startPos
        self.image = self.imgs[0]
        self.downwards = False
        self.angle = 0
        self.flightTime = 0
        self.xSpeed = 0
        self.ySpeed = 0

    def imageAnimate(self):
        self.animVal += 1
        self.image = self.imgs[self.index]
        self.index = (self.animVal // self.animDelay) % len(self.imgs)
        self.image = pygame.transform.rotate(self.image, self.angle)

    def draw(self):
        self.screen.blit(self.image, self.rect.topleft)
