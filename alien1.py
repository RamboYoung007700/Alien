import sys
import pygame
import settings
from ship import Ship

def run_game():
    pygame.init()
    ai_settings=settings.Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("外星人入侵")

    ship=Ship(screen)
    
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
        screen.fill(ai_settings.bg_color)
        ship.blitme()
        pygame.display.flip()
        
run_game()

