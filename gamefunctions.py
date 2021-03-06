import sys
import pygame
from alien import Alien
from bullet import Bullet
from time import sleep

def read_high_score():
    filename='highscore.txt'
    try:
        with open(filename) as file:
            highscore=file.read()
    except FileNotFoundError:
        highscore=0
    highscore=int(highscore)
    return highscore

def save_high_score(high_score):
    filename='highscore.txt'
    try:
        with open(filename) as file:
            filehighscore=file.read()
    except FileNotFoundError:
        with open(filename,'w') as file:
            file.write(str(high_score))
    else:
        with open(filename,'w') as file:
            file.write(str(high_score))

def ship_hit(settings,stats,screen,ship,sb,aliens,bullets):
    if stats.ships_left>0:
        stats.ships_left-=1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(settings,screen,ship,aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)
        save_high_score(stats.high_score)

def check_aliens_bottom(settings,stats,screen,ship,sb,aliens,bullets):
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            ship_hit(settings,stats,screen,ship,sb,aliens,bullets)
            break

def check_keydown_events(event,settings,screen,ship,sb,bullets,stats,aliens):
    if event.key==pygame.K_RIGHT:
        ship.moving_right=True
    if event.key==pygame.K_LEFT:
        ship.moving_left=True
    if event.key==pygame.K_SPACE:
        fire_bullet(settings,screen,ship,bullets)
    if event.key==pygame.K_q:
        save_high_score(stats.high_score)
        sys.exit()
    if event.key==pygame.K_p:
        start_game(stats,aliens,bullets,settings,screen,ship,sb)
    if event.key==pygame.K_c:
        settings.bullet_width=settings.screen_width
    if event.key==pygame.K_u:
        settings.bullet_width=3

def check_keyup_events(event,ship):
    if event.key==pygame.K_RIGHT:
        ship.moving_right=False
    if event.key==pygame.K_LEFT:
        ship.moving_left=False
    
    
def check_events(settings,screen,stats,play_button,ship,sb,aliens,bullets):
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            save_high_score(stats.high_score)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,settings,screen,ship,sb,bullets,
                                 stats,aliens)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(settings,screen,stats,play_button,
                              ship,sb,aliens,bullets,mouse_x,mouse_y)

def check_play_button(settings,screen,stats,play_button,
                      ship,sb,aliens,bullets,mouse_x,mouse_y):
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        start_game(stats,aliens,bullets,settings,screen,ship,sb)

def start_game(stats,aliens,bullets,settings,screen,ship,sb):
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    settings.initialize_dynamic_settings()
    stats.game_active=True
   
    sb.prep_images()
    
    aliens.empty()
    bullets.empty()
    create_fleet(settings,screen,ship,aliens)
    ship.center_ship()
           
def update_screen(ai_settings,screen,sb,ship,bullets,aliens,stats,play_button):
        screen.fill(ai_settings.bg_color)
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        ship.blitme()
        aliens.draw(screen)
        sb.show_score()
        if not stats.game_active:
            play_button.draw_button()
        pygame.display.flip()

def update_bullets(settings,screen,stats,sb,ship,aliens,bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(settings,screen,stats,sb,ship,aliens,bullets)

def check_bullet_alien_collisions(settings,screen,stats,sb,ship,aliens,bullets):
    collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for aliens in collisions.values():
            stats.score+=settings.alien_points*len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
    if len(aliens)==0:
        start_new_level(bullets,settings,stats,sb,screen,ship,aliens)

def start_new_level(bullets,settings,stats,sb,screen,ship,aliens):
    bullets.empty()
    settings.increase_speed()
    stats.level+=1
    sb.prep_level()
    create_fleet(settings,screen,ship,aliens)

def update_aliens(settings,stats,screen,ship,sb,aliens,bullets):
    check_fleet_edges(settings,aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(settings,stats,screen,ship,sb,aliens,bullets)
    check_aliens_bottom(settings,stats,screen,ship,sb,aliens,bullets)

def get_number_aliens_x(settings,alien_width):
    available_sapce_x=settings.screen_width-2*alien_width
    number_aliens_x=int(available_sapce_x/(2*alien_width))
    return number_aliens_x

def create_alien(settings,screen,aliens,alien_number,row_number):
    alien=Alien(settings,screen)
    alien_width=alien.rect.width
    alien.x=alien_width+2*alien_width*alien_number
    alien.rect.x=alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)

def get_number_rows(settings,ship_height,alien_height):
    available_space_y=(settings.screen_height-
                       (3*alien_height)-ship_height)
    number_rows=int(available_space_y/(2*alien_height))
    return number_rows

def create_fleet(settings,screen,ship,aliens):
    alien =Alien(settings,screen)
    alien_width=alien.rect.width
    number_aliens_x=get_number_aliens_x(settings,alien_width)
    number_rows=get_number_rows(settings,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(settings,screen,aliens,alien_number,row_number)
        
def check_fleet_edges(settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings,aliens)
            break

def change_fleet_direction(settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y+=settings.fleet_drop_speed
    settings.fleet_direction*=-1

def check_high_score(stats,sb):
    if stats.score>stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()



    

def fire_bullet(settings,screen,ship,bullets):
    if len(bullets)<settings.bullets_allowed:
        new_bullet=Bullet(settings,screen,ship)
        bullets.add(new_bullet)

    
    
