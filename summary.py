import pygame
from configs import *

class Summary:
    def __init__(self, plane, star_total):
        self.screen = pygame.display.get_surface()
        self.summary_pos = pygame.Vector2(WIDTH, 60)
        self.summary = pygame.image.load(f"{CWD}/assets/gameImages/gameSummary.png").convert_alpha()
        self.cont_arrow = pygame.transform.scale(
            pygame.image.load(f"{CWD}/assets/gameImages/continueArrow.png"), (162, 123)
            ).convert_alpha()
        self.cont_arrow_rect = self.cont_arrow.get_rect(topleft = (WIDTH + 360, 570))
        self.cont_arrow_pos = self.cont_arrow_rect
        self.plane = plane
        self.star_total = star_total

    def draw(self):  
        stars_collected = summary_font.render(str(self.star_total), True, "orange3")
        distance_travelled = summary_font.render(f"{self.plane.distance:.1f}m", True, "orange3")
        star_cash = summary_font.render(f"${self.star_total * 5}", True, "darkgreen")
        distance_cash = summary_font.render(f"${(self.plane.distance) * 0.5:.2f}", True, "darkgreen")
        total_cash = default_font.render(
            f"${self.plane.distance * 0.5 + self.star_total * 5:.2f}", True, "darkgreen"
            )

        if self.summary_pos[0] > 240:
            self.screen.blit(self.summary, self.summary_pos)
            self.screen.blit(self.cont_arrow, self.cont_arrow_pos)
            self.summary_pos[0] -= 20
            self.cont_arrow_pos[0] -= 20
        else:
            self.screen.blit(self.summary, self.summary_pos)
            self.screen.blit(self.cont_arrow, self.cont_arrow_pos)
            self.screen.blit(stars_collected, (380, 300))
            self.screen.blit(distance_travelled, (380, 430))

            self.screen.blit(star_cash, (570, 300))
            self.screen.blit(distance_cash, (535, 430))
            self.screen.blit(total_cash, (450, 510))
            self.summary_update()

    def summary_update(self):
        mouse_pos = pygame.mouse.get_pos()
        if 600 < mouse_pos[0] < 762 and 570 < mouse_pos[1] < 693:
            self.cont_arrow = pygame.transform.scale(self.cont_arrow, (178, 135))
            self.cont_arrow_rect = self.cont_arrow.get_rect(topleft = pygame.Vector2(590, 560))
            self.cont_arrow_pos = self.cont_arrow_rect
        else:
            self.cont_arrow = pygame.transform.scale(
                pygame.image.load(f"{CWD}/assets/gameImages/continueArrow.png"), (162, 123)
                )
            self.cont_arrow_rect = self.cont_arrow.get_rect(topleft = pygame.Vector2(600, 570))
            self.cont_arrow_pos = self.cont_arrow_rect
         
