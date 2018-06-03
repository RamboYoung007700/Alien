import pygame.font

class Instruction():
    def __init__(self,settings,screen,msg):
        self.screen=screen
        self.screen_rect=screen.get_rect()

        self.width, self.height=1100,30
        self.button_color=(100,100,100)
        self.text_color=(0,0,0)
        self.font=pygame.font.SysFont(None,30)

        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.centerx=self.screen_rect.centerx
        self.rect.centery=self.screen_rect.bottom-200
        self.prep_msg(msg)
    def prep_msg(self,msg):
        self.msg_image=self.font.render(
            msg,True,self.text_color,self.button_color)
        self.msg_image_rect=self.msg_image.get_rect()
        self.msg_image_rect.center=self.rect.center
    def draw_button(self):
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)
