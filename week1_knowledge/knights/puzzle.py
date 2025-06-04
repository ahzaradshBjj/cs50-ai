from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    Not(And(AKnight, AKnave)),   # A can not be both
    Or(AKnight, AKnave),  # A is just one

    # if A is a knight he is telling the true
    Implication(AKnight, And(AKnight, AKnave)),
    # if A is a knave it can not be true what he says (both knight and knave)
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    Not(And(AKnight, AKnave)),  # A can not be both
    Or(AKnight, AKnave),  # A is just one

    Not(And(BKnight, BKnave)),  # B can not be both
    Or(BKnight, BKnave),  # B is just one,

    # If A is knight, what he says is the true
    Implication(AKnight, And(AKnave, BKnave)),
    # If A is knave, what he says is not the true
    Implication(AKnave, Not(And(AKnave, BKnave)))
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
    Not(And(AKnight, AKnave)),  # A can not be both
    Or(AKnight, AKnave),  # A is just one

    Not(And(BKnight, BKnave)),  # B can not be both
    Or(BKnight, BKnave),  # B is just one,

    # A says we are the same kind
    # when A is knight, A and B are the same kind
    Implication(AKnight, And(AKnight, BKnight)),
    # when A is knave, A and B are not the same kind
    Implication(AKnave, Or(And(AKnight, BKnave), And(AKnave, BKnight))),

    # B says we are of different kinds
    # when B is knight, A and B are differents
    Implication(BKnight, Or(And(AKnave, BKnight), And(BKnave, AKnight))),
    # We are the same if B is knave
    Implication(BKnave, Or(And(AKnave, BKnave), And(AKnight, BKnight)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
    Not(And(AKnight, AKnave)),  # A can not be both
    Or(AKnight, AKnave),  # A is just one

    Not(And(BKnight, BKnave)),  # B can not be both
    Or(BKnight, BKnave),  # B is just one,

    Not(And(CKnight, CKnave)),  # C can not be both
    Or(CKnight, CKnave),  # C is just one

    # A says I am a knight or I am a knave, but you do not know which
    Or(
        # When A is a knight, he can be just one but not noth
        Implication(AKnight, And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)))),
        # When A is a knave then he is both a knight and a knave
        Implication(AKnave, And(AKnight, AKnave))
    ),

    # B says A said he is a knave
    # When B is a knight, A actually says he is a knave but he can be both knight or knave
    # Implication(BKnight, And(
    #     Implication(AKnave, AKnight),
    #     Implication(AKnight, AKnight))
    # ),
    And(
        Implication(BKnight, Implication(AKnave, AKnight)),
        Implication(BKnight, Implication(AKnight, AKnight))
    ),

    # When B is a knave, A did not say he is a knave
    # Implication(BKnave, And(
    #     Implication(AKnight, AKnight),
    #     Implication(AKnave, AKnight))
    # ),

    # B says C is a knave
    # When B is knight, C is a knave
    Implication(BKnight, CKnave),
    # When B is knave, C is a knight
    Implication(BKnave, CKnight),

    # C says A is a knight
    # When C is knight, A is a knight
    Implication(CKnight, AKnight),
    # When C is knave, A is a knave
    Implication(CKnave, AKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
