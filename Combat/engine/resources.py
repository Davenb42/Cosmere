from dataclasses import dataclass


@dataclass
class Resource:
    current: int
    maximum: int

    def __init__(self, current: int, max: int = None, maximum: int = None):
        if max is not None:
            self.current = current
            self.maximum = max
        else:
            self.current = current
            self.maximum = maximum if maximum is not None else current

    def gain(self, amount: int):
        self.current = min(self.maximum, self.current + amount)

    def lose(self, amount: int):
        self.current = max(0, self.current - amount)

    def set(self, amount: int):
        self.current = max(0, min(self.maximum, amount))

    def __str__(self):
        return f"{self.current}/{self.maximum}"