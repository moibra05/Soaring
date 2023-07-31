import pygame

pygame.init()
debug_font = pygame.default_font.Font(None, 30)

def debug(info, y = 10, x = 10):
    displaySurf = pygame.display.get_surface()
    debugSurf = debug_font.render(str(info), True, 'white')
    debugRect = debugSurf.get_rect(topleft = (x, y))
    pygame.draw.rect(displaySurf, 'black', debugRect)
    displaySurf.blit(debugSurf, debugRect)