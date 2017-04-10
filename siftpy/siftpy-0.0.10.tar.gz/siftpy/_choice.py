from siftpy._exceptions import InvalidChoiceException

class Question(object):

    def __init__(self, choices, display_prop):
        self.choices = choices
        self.__display_prop = display_prop

    @property
    def ask(self):
        if self.__display_prop:
            return {str(i): getattr(choice, self.__display_prop) for i, choice in enumerate(choices)}
        return self.choices


class Choice(object):
    def __init__(self, choices, callback, display_prop):
        self.pending = True
        self.__choices = {str(i): choice for i, choice in enumerate(choices)}
        self.__callback = callback
        self.__display_prop = display_prop        

    @property
    def question(self):
        if self.__display_prop:
            return {i: getattr(choice, self.__display_prop) for i, choice in self.__choices.items()}
        return self.__choices

    def choose(self, i):
        index = str(i)
        if index not in self.__choices:
            raise InvalidChoiceException("Answer '{}'' is not present in the list of choices".format(index))
        answer = [self.__choices[index]]
        self.pending = False
        self.__callback(answer)