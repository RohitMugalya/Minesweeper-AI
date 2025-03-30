from itertools import combinations

from connective import *
from proposition import *


def check_knowledge(knowledge: Connective, propositions: list[Proposition]):
    for symbol in propositions:
        if knowledge.entails(symbol):
            print(f"{symbol}: YES")
        elif knowledge.entails(Not(symbol)):
            print(f"{symbol}: NO")
        else:
            print(f"{symbol}: MAYBE")


a = Proposition((0, 0))
b = Proposition((0, 1))
c = Proposition((0, 2))
d = Proposition((1, 0))
e = Proposition((1, 2))
f = Proposition((2, 0))
g = Proposition((2, 1))
h = Proposition((2, 2))

x = Proposition((5, 5))
y = Proposition((5, 6))

knowledge_base = And()


def add_knowledge(cells, count) -> Connective:
    kb = Or()
    for i, combination in enumerate(combinations(cells, count), start=1):
        logic = And()
        kb.add(logic)
        for cell in combination:
            logic.add(cell)

        for cell in cells:
            if cell not in combination:
                logic.add(Not(cell))

    return kb


cells1 = [a, b, c, d, e, f, g, h]
count1 = 7
cells2 = [x, c, y]
count2 = 0

knowledge_base.add(add_knowledge(cells1, count1))
knowledge_base.add(add_knowledge(cells2, count2))

print(knowledge_base)
check_knowledge(knowledge_base, cells1 + cells2)
