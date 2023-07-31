import pygame
from configs import *

class Progress:
    def __init__(self, plane, total_distance, level):
        pygame.init()
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.progress_time = 0
        self.end_time = 0
        self.level_number = level
        self.plane = plane
        self.total_distance = total_distance
        self.progress_pos = (((self.total_distance - self.plane.distance) / 
        level_distances[level_names[self.level_number]]) * 705) + 100
        self.init_progress_pos = self.progress_pos
        self.progress_screen = pygame.image.load(f"{CWD}/assets/gameImages/progress_screen.png")
        self.progress_plane = pygame.transform.scale(
            pygame.image.load(f"{CWD}/assets/gameImages/progress_plane.png").convert_alpha(), (50,50)
            )
        self.pixel_distance = (
            (self.plane.distance / level_distances[level_names[self.level_number]]) * 705
            )

    def draw(self):
        level_image = pygame.image.load(f"{CWD}/assets/levelBGs/{full_level_images[self.level_number]}")
        level_title = default_font.render(f"{true_level_names[self.level_number]}", True, "white")
        distance_fraction = summary_font.render(
            f"{self.total_distance:.1f}m/{level_distances[level_names[self.level_number]]}m", 
            True, "black"
            )
        level_title_rect = level_title.get_rect(center = (WIDTH/2, 55))
        fraction_rect = distance_fraction.get_rect(center = (WIDTH/2, 690))

        self.screen.blit(self.progress_screen, (0,0))
        self.screen.blit(pygame.transform.scale(level_image, (565, 381)), (197, 154))
        self.screen.blit(self.progress_plane, (self.progress_pos, 633))
        self.screen.blit(distance_fraction, fraction_rect)
        self.screen.blit(level_title, level_title_rect)

        if self.progress_pos <= self.init_progress_pos + self.pixel_distance:
            self.progress_pos += 2
            if self.progress_pos >= 805:
                if self.level_number != 5:
                    self.plane.distance = self.total_distance - level_distances[level_names
                    [self.level_number]]
                    self.pixel_distance = (
                        (self.plane.distance / level_distances[level_names[self.level_number + 1]]) 
                        * 705
                        )
                    self.progress_pos = 100
                    self.init_progress_pos = self.progress_pos
                    self.level_number += 1
                    self.total_distance = round(self.plane.distance, 1)
                    pygame.event.post(pygame.event.Event(BEAT_LEVEL))
                else:
                    self.total_distance = 600
                    self.progress_pos = 805
                    self.end_time += 0.017
                    if self.end_time >= 2:
                        pygame.event.post(pygame.event.Event(GAME_END))
                                
        self.progress_continue()

    def progress_continue(self):
        if self.progress_pos >= self.init_progress_pos + self.pixel_distance:
            self.progress_time += 0.017

        if self.progress_time >= 2:
            self.progress_time = 0
            self.init_progress_pos = self.progress_pos
            pygame.event.post(pygame.event.Event(PROGRESS_CONTINUE))
