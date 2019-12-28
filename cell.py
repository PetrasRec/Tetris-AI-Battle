
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0, 0, 0)

    def is_free(self):
        return self.color[0] == 0 and self.color[1] == 0 and self.color[2] == 0

    def clear_cell(self):
        self.color = (0, 0, 0)