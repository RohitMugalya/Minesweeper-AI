from typing import Self, Hashable


class Proposition:
    __instances: dict[Hashable, Self] = {}

    def __new__(cls, statement):
        if statement not in cls.__instances:
            cls.__instances[statement] = super().__new__(cls)

        return cls.__instances[statement]

    def __init__(self, statement: Hashable):
        self._state: Tautology | Contradiction
        self.statement = statement

    @staticmethod
    def from_bool(boolean: bool):
        assert isinstance(boolean, (bool, Tautology, Contradiction))

        if isinstance(boolean, (Tautology, Contradiction)):
            return boolean
        if boolean is True:
            return Tautology()
        if boolean is False:
            return Contradiction()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: bool):
        self._state = self.from_bool(value)  # NOQA

    @property
    def propositions(self) -> set[Self]:
        return {self}

    def evaluate(self):
        return self.state

    def __bool__(self):
        raise TypeError("Proposition can't be converted to bool")

    def __eq__(self, other: Self):
        return self.statement == other.statement

    def __lt__(self, other: Self):
        return self.statement < other.statement

    def __hash__(self):
        return hash(self.statement)

    def __repr__(self):
        return repr(self.statement)

    def __str__(self):
        return str(self.statement)


class Tautology(Proposition):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, "T")

        return cls.__instance

    def __init__(self):  # NOQA
        self.statement = "T"

    def evaluate(self) -> Self:
        return self

    def __bool__(self):
        return True


class Contradiction(Proposition):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, "F")

        return cls.__instance

    def __init__(self):  # NOQA
        self.statement = "F"

    def evaluate(self):
        return self

    def __bool__(self):
        return False
