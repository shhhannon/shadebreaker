# tracks the player's progress

class UserData:
    def __init__(self):
        self._level = 0
        self._scores = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # [time, kills, coins]

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def scores(self):
        return self._scores

    def update_score(self, score):
        # ensure that the score is being updated for a valid level
        if 0 <= self.level < len(self._scores):
            self._scores[self.level] = score