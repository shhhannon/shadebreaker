class Data:
    def __init__(self, ui):
        self.ui = ui
        self.coins = 0
        self._max_health = 5
        self._health = self._max_health
        self._has_diamond = False

        self._level_complete = False

        self.ui.create_hearts(self._max_health, self._health)
        self.ui.create_diamond(self._has_diamond)

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
    def level_complete(self):
        return self._level_complete
   
    @level_complete.setter
    def level_complete(self, value):
        self._level_complete = value