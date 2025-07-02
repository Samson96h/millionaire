class Question:
    def __init__(self,question, variants, correct):
        self.__question = question
        self.__variants = variants
        self.__correct = correct
    @property
    def question(self):
        return self.__question
    @property
    def variants(self):
        return self.__variants
    @property
    def correct(self):
        return self.__correct

    def __str__(self):
        line = ""
        line += "\n" + self.__question + "\n"
        for i, a in enumerate(self.__variants, 1):
            line += f"{i}. {a} \n"
        return line