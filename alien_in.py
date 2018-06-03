import pygame
import settings
from ship import Ship
import gamefunctions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from instruction import Instruction
from scoreboard import Scoreboard

def run_game():
    pygame.init()
    ai_settings=settings.Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("外星人入侵")

    play_button=Button(ai_settings,screen,'Play')
    instruction='INSTRUCTION  [left: left moving] [right: right moving] [up: up moving] [down: down moving] [space: fire]'
    ins=Instruction(ai_settings,screen,instruction)

    ship=Ship(screen,ai_settings)
    bullets=Group()
    aliens=Group()
    gf.create_fleet(ai_settings,screen,ship,aliens)

    stats=GameStats(ai_settings)

    sb=Scoreboard(ai_settings,screen,stats)
    
    while True:
        gf.check_events(ai_settings,screen,stats,play_button,ship,sb,aliens,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,stats,screen,ship,sb,aliens,bullets)
        gf.update_screen(ai_settings,screen,sb,
                         ship,bullets,aliens,stats,play_button,ins)
        
run_game()

