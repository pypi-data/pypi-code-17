from typing import Any


class Comparison(object):
    def __init__(
        self,
        value: Any,
        target: Any = None,
        negate: bool = False,
        negate_term: str = ""
    ):
        """
        Test value against target
        :param value: Value being tested
        :param target: Value being tested against
        :param fail_message: Message to display on failure
        :param negate: Negate comparison
        :param negate_term: String in message to represent negation
        """
        self.value = value
        self.target = target
        self.negate: bool = negate
        self.negate_term = negate_term
        self.message_parts = (
            repr(self.value),
            self.negate_term,
            self.name,
            repr(self.target)
        )
        self.on_init()

    @staticmethod
    def on_init():
        """
        Callback function called on initialization
        :return: 
        """
        pass

    @staticmethod
    def on_compare(result: bool, message: str):
        """
        Callback function called after comparision is completed
        :param result: Boolean of comparison result
        :param message: String of comparison result
        :return: 
        """
        pass

    def compare(self):
        """
        Function called for comparison
        :return: Boolean if comparison passed or failed
        """
        raise NotImplemented()

    @property
    def name(self):
        """
        Normalized name of comparison for message
        :return: Name of comparison
        """
        from expectlib.utils import from_pascal_to_snake

        return from_pascal_to_snake(self.__class__.__name__) \
            .replace("_", " ")

    def __call__(self, fail_message=""):
        """
        Runtime function for comparison
        :return: 
        """
        result = self.compare()
        self.called = True

        if self.negate is True:
            result = not result

        message_from_parts = ' '.join(filter(None, self.message_parts))
        message = ": ".join(filter(None, [message_from_parts, fail_message]))

        self.on_compare(result, message)

        assert result, message


class Not(Comparison):
    """
    Mixin to create negated comparisons
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.negate = True


class Equal(Comparison):
    def compare(self):
        return self.value == self.target


class DoesntEqual(Equal, Not):
    pass


class GreaterThan(Comparison):
    def compare(self):
        return self.value > self.target


class GreaterThanOrEqual(Comparison):
    def compare(self):
        return self.value >= self.target


class LesserThan(Comparison):
    def compare(self):
        return self.value < self.target


class LesserThanOrEqual(Comparison):
    def compare(self):
        result = self.value <= self.target
        return result


class Is(Comparison):
    def compare(self):
        return self.value is self.target


class Isnt(Is, Not):
    pass


class Empty(Comparison):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_parts = (
            str(self.value),
            self.negate_term,
            self.name
        )

    def compare(self):
        if self.value is None:
            return True

        if isinstance(self.value, str) or isinstance(self.value, list):
            return len(self.value) == 0

        return False


class Contain(Comparison):
    def compare(self):
        return self.target in self.value


class DoesNotContain(Contain, Not):
    pass


class Match(Comparison):
    def compare(self):
        import re
        return re.match(self.target, self.value)


class DoesntMatch(Match, Not):
    pass


class StartWith(Comparison):
    def compare(self):
        text: str = self.value
        return text.startswith(self.target)


class DoesntStartWith(StartWith, Not):
    pass


class EndWith(Comparison):
    def compare(self):
        text: str = self.value
        return text.endswith(self.target)


class DoesntEndWith(EndWith, Not):
    pass
