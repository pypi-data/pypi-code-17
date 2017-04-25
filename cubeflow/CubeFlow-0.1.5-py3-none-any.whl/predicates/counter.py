class Counter:

    def __init__(self, value: int) -> None:
        self._value = value

    def __call__(self, _) -> bool:
        self._value -= 1
        return self._value >= 0
