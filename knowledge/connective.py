import functools
import itertools
from typing import Self

import pandas as pd

from . import proposition

pd.set_option("display.max_columns", None)


class Connective:
    notation = "?"

    def add(self, operand: proposition.Proposition | Self):
        raise NotImplementedError

    def evaluate(self) -> 'proposition.Tautology | proposition.Contradiction':
        raise NotImplementedError

    def entails(self,
                query: 'proposition.Proposition | Connective',
                model: dict[proposition.Proposition, bool] | None = None) -> proposition.Tautology | proposition.Contradiction:

        if model is None:
            model = {}

        for p, state in model.items():
            p.state = state

        propositions = list((self.propositions | query.propositions) - model.keys())
        for model in itertools.product([False, True], repeat=len(propositions)):
            for p, state in zip(propositions, model):
                p.state = state

            if self.evaluate() and not query.evaluate():
                return proposition.Contradiction()

        return proposition.Tautology()

    @property
    def propositions(self) -> set['proposition.Proposition']:
        raise NotImplementedError

    def truth_table(self, result_col_name: str | None = None) -> pd.DataFrame:
        if result_col_name is None:
            result_col_name = repr(self)
        propositions = list(self.propositions)
        propositions.sort()
        n = len(propositions)
        table = pd.DataFrame(columns=propositions + [result_col_name])
        for i, states in enumerate(itertools.product([False, True], repeat=n)):
            for p, state in zip(propositions, states):
                p.state = state
                table.loc[i, p] = state
            table.iloc[i, -1] = self.evaluate()

        return table

    def __bool__(self):
        raise TypeError("Connective can't be converted to bool")


class Unary(Connective):
    def __init__(self, operand: 'proposition.Proposition | Connective'):
        self.operand = operand

    @property
    def propositions(self) -> set['proposition.Proposition']:
        propositions = set()
        if isinstance(self.operand, (proposition.Tautology, proposition.Contradiction)):
            pass
        elif isinstance(self.operand, proposition.Proposition):
            propositions.add(self.operand)
        else:
            propositions.update(self.operand.propositions)

        return propositions

    def __repr__(self):
        return f"{type(self).__name__}({self.operand!r})"

    def __str__(self):
        return self.notation + (
            str(self.operand) if isinstance(self.operand, proposition.Proposition)
            else f"({self.operand!s})"
        )


class Binary(Connective):
    def __init__(self, *operands: 'proposition.Proposition | Connective'):
        # assert len(operands) >= 2
        self.operands: list[proposition.Proposition | Connective] = list(operands)

    def add(self, operand: 'proposition.Proposition | Connective'):
        self.operands.append(operand)

    @property
    def propositions(self) -> set['proposition.Proposition']:
        propositions = set()
        for operand in self.operands:
            if isinstance(operand, (proposition.Tautology, proposition.Contradiction)):
                continue
            if isinstance(operand, proposition.Proposition):
                propositions.add(operand)
            else:
                propositions.update(operand.propositions)

        return propositions

    @staticmethod
    def logic(
            operand1: proposition.Proposition | Connective,
            operand2: proposition.Proposition | Connective
    ) -> proposition.Tautology | proposition.Contradiction:
        raise NotImplementedError

    def evaluate(self) -> 'proposition.Tautology | proposition.Contradiction':
        result = functools.reduce(self.logic, self.operands)
        assert isinstance(result, (proposition.Tautology, proposition.Contradiction))
        return result

    def __repr__(self):
        return f"{type(self).__name__}({', '.join(map(repr, self.operands))})"

    def __str__(self):
        return self.notation.center(len(self.notation) + 2).join(
            f"({operand!s})" if isinstance(operand, Binary) and not isinstance(operand, type(self))
            else str(operand)
            for operand in self.operands
        )


class Not(Unary):
    notation = "~"

    def evaluate(self: Self | proposition.Proposition) -> proposition.Tautology | proposition.Contradiction:
        if isinstance(self, proposition.Proposition):
            return self.evaluate()
        return (
            proposition
            .Proposition
            .from_bool(not self.operand.evaluate())
        )


class And(Binary):
    notation = "^"

    def evaluate(self) -> 'proposition.Tautology | proposition.Contradiction':
        return (
            proposition
            .Proposition
            .from_bool(all(operand.evaluate() for operand in self.operands))
        )


class Or(Binary):
    notation = "v"

    def evaluate(self) -> 'proposition.Tautology | proposition.Contradiction':
        return (
            proposition
            .Proposition
            .from_bool(any(operand.evaluate() for operand in self.operands))
        )


class Xor(Binary):
    notation = "⊕"

    @staticmethod
    def logic(
            operand1: proposition.Proposition | Connective,
            operand2: proposition.Proposition | Connective
    ) -> proposition.Tautology | proposition.Contradiction:
        p = operand1.evaluate()
        q = operand2.evaluate()
        return proposition.Proposition.from_bool((not p and q) or (p and not q))


class Imply(Binary):
    notation = "->"

    @staticmethod
    def logic(
            operand1: proposition.Proposition | Connective,
            operand2: proposition.Tautology | proposition.Contradiction
    ) -> proposition.Tautology | proposition.Contradiction:
        return (
            proposition
            .Proposition
            .from_bool((not operand1.evaluate()) or operand2)
        )

    def evaluate(self) -> 'proposition.Tautology | proposition.Contradiction':
        n = len(self.operands)
        result = proposition.Proposition.from_bool(self.operands[n - 1].evaluate())
        for i in range(n - 2, -1, -1):
            result = self.logic(self.operands[i], result)

        return result


class BiConditional(Binary):
    notation = "<->"

    @staticmethod
    def logic(
            operand1: proposition.Proposition | Connective,
            operand2: proposition.Proposition | Connective
    ) -> proposition.Tautology | proposition.Contradiction:
        p = operand1.evaluate()
        q = operand2.evaluate()
        return proposition.Proposition.from_bool((p and q) or (not p and not q))


if __name__ == "__main__":
    alice = proposition.Proposition("Alice")
    bob = proposition.Proposition("Bob")
    print(And(alice, bob))
    print(repr(And(alice, bob)))
