# tracks the player's progress

class UserData:
    def __init__(self):
        self._level = 0
        self._scores = [0, 0, 0]

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def scores(self):
        return self._scores

    @property
    def score1(self):
        return self._scores[0]
        
    @score1.setter
    def score1(self, value):
        self._scores[0] = value
            
    @property
    def score2(self):
        return self._scores[1]
        
    @score2.setter
    def score2(self, value):
        self._scores[1] = value
            
    @property
    def score3(self):
        return self._scores[2]
        
    @score3.setter
    def score3(self, value):
        self._scores[2] = value

    def update_score(self, score):
        # ensure that the score is being updated for a valid level
        if 0 <= self.level < len(self._scores):
            self._scores[self.level] = score