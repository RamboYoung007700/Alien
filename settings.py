class Settings():
    def __init__(self):
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(0,155,255)
        
        #ship
        self.ship_limit=3

        #bullet
        self.bullets_allowed=3

        #alien        
        self.fleet_drop_speed=20
        
        #bullet       
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=(250,0,0)

        #加快游戏节奏系数
        self.speedup_scale=1.1
        #外星人分数提高
        self.score_scale=1.5

        #动态属性初始化
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor=1.5
        self.bullet_speed_factor=3
        self.alien_speed_factor=1
        self.alien_points=50
        self.fleet_direction=1

    def increase_speed(self):
        self.ship_speed_factor*=self.speedup_scale
        self.bullet_speed_factor*=self.speedup_scale
        self.alien_speed_factor*=self.speedup_scale
        self.alien_points=int(self.alien_points*self.score_scale)

       




























        

        
