import abc

ABC = abc.ABCMeta('ABC', (object,), {}) # compatible with Python 2 *and* 3


class Question(ABC):
    """Abstract base class for all questions."""

    @abc.abstractmethod
    def get_question_text(self):
        """Get the question text."""
        pass

    @abc.abstractmethod
    def check_answer(self, answer):
        """Check if an answer is correct"""
        pass

    @abc.abstractmethod
    def get_correct_answers(self):
        """Get some example answers that are correct."""
        pass

    @abc.abstractmethod
    def get_wrong_answers(self):
        """Get some answers that are wrong."""
        pass


class WrongAnswer(Exception):
    """A wrong answer has been supplied."""
    pass
