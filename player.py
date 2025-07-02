class Player:
    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    @property
    def name(self):
        return self.__name
    @property
    def score(self):
        return self.__score
    @score.setter
    def score(self, value):
        self.__score = max(0, value)

    def __str__(self):
        return f"{self.name} {self.score}"