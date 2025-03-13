class Data:
    def __init__(self, ui):
        self.ui = ui
        self.coins = 0
        self._max_health = 5
        self._health = self._max_health
        self._has_diamond = False

        self._enemy_count = 0
        self._kills = 0
        self._coin_count = 0
        self.score = 0

        self._level_complete = False
        self._light_world = False

        self.ui.create_hearts(self._max_health, self._health)
        self.ui.create_diamond(self._has_diamond)

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

    def calculate_score(self):
        self.score = int((self._kills/self._enemy_count + self.coins/self._coin_count) * 100)
        if self.score == 0:
            self.score = 0
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