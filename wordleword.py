from fancyword import FancyWord


class WordleWord(FancyWord):
    def __init__(self, w):
        super().__init__(w)

    def setCorrect(self, pos):
        self.setColorAt(pos, "green")

    def setMisplaced(self, pos):
        self.setColorAt(pos, "yellow")

    def setUnused(self, pos):
        self.setColorAt(pos, "gray")

    def isCorrect(self, pos):
        if self.colorAt(pos) == "green":
            return True

    def isMisplaced(self, pos):
        if self.colorAt(pos) == "yellow":
            return True

    def isNotUsed(self, pos):
        if self.colorAt(pos) == "gray":
            return True
