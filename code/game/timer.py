from pygame.time import get_ticks

class Timer:
    def __init__(self, length):
        self.length = length
        self.start_time = get_ticks()
        self.old_time = 0
        self.active = False

    def activate(self):
        self.active = True
        self.start_time = get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0
    
    def update(self):
        current_time = get_ticks()
        if current_time - self.start_time >= self.length:
            self.deactivate()

    def get_time(self):
        if self.active:
            current_time = get_ticks()
            return int(current_time - self.start_time)
        
    def unpause(self):
        if self.old_time != None:
            self.start_time = get_ticks() - self.old_time
