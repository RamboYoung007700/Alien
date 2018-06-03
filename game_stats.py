import gamefunctions as gf

class GameStats():
    def __init__(self,settings):
        self.settings=settings
        self.game_active=False
        self.reset_stats()
        
    def reset_stats(self):
        self.ships_left=self.settings.ship_limit
        self.score=0
        self.level=1
        self.high_score=gf.read_high_score()
