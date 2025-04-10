from game.timer import Timer

# manages level data
class Data:
    def __init__(self, ui):
        self.ui = ui
        self.coins = 0
        self._max_health = 5
        self._health = self._max_health
        self._has_diamond = False

        # timer
        self._game_timer = Timer(-1)
        self._game_timer.activate()
   
        # score calculations
        self._enemy_count = 0
        self._kills = 0
        self._coin_count = 0
        self.score = [0, 0, 0]
        self.total_time = 0

        # level properties
        self._level_complete = False
        self._light_world = False
        self._change_timer = Timer(5000)

        # creating ui features
        self.ui.create_hearts(self._max_health, self._health)
        self.ui.create_diamond(self._has_diamond)
        self.ui.create_bar(192)
        self.ui.create_timer(0)

    # ui
    @property
    def health(self):
        return self._health
   
    @health.setter
    def health(self, value):
        self._health = value
        self.ui.create_hearts(self._max_health, value)
    
    @property
    def max_health(self):
        return self._max_health

    @property
    def has_diamond(self):
        return self._has_diamond
    
    @has_diamond.setter
    def has_diamond(self, value):
        self._has_diamond = value
        self.ui.create_diamond(value)

    @property
    def game_timer(self):
        return self._game_timer
    
    def update_timer(self, time):
        self.ui.create_timer(time)

    
    # score
    @property
    def enemy_count(self):
        return self._enemy_count
   
    @enemy_count.setter
    def enemy_count(self, value):
        self._enemy_count = value

    @property
    def kills(self):
        return self._kills
   
    @kills.setter
    def kills(self, value):
        self._kills = value

    @property
    def coin_count(self):
        return self._coin_count
   
    @coin_count.setter
    def coin_count(self, value):
        self._coin_count = value

    def calculate_score(self, level):
        self.level = level
        self.kill_ratio = self.kills / self._enemy_count if self._enemy_count > 0 else 0
        self.coin_ratio = self.coins / self._coin_count if self._coin_count > 0 else 0

        # level 1
        if self.level == 0:
            self.min_time = 100000
            self.min_kills = 0.6
            self.min_coins = 0.2
        
        if self.total_time <= self.min_time:
            self.score[0] = 1
        if self.kill_ratio >= self.min_kills:
            self.score[1] = 1
        if self.coin_ratio >= self.min_coins:
            self.score[2] = 1
        return self.score
  
    
    # level properties
    @property
    def level_complete(self):
        return self._level_complete
   
    @level_complete.setter
    def level_complete(self, value):
        self._level_complete = value

    @property
    def light_world(self):
        return self._light_world
   
    @light_world.setter
    def light_world(self, value):
        self._light_world = value

    @property
    def change_timer(self):
        return self._change_timer
   
    def update_bar(self, value):
        if not self._change_timer.active:
            self.ui.create_bar(5000)
        else:
            self.ui.create_bar(value)