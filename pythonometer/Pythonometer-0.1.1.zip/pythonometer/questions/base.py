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
    def get_an_answer(self):
        """Get an example answer that is correct."""
        pass
