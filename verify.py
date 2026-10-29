import random
from decimal import Decimal, getcontext

from astroid import a216877, by_columns

DATA = [
    1, 5, 9, 17, 21, 33, 49, 61, 81, 105, 125, 145, 169, 205, 233, 273, 309, 357,
    393, 437, 485, 529, 565, 629, 681, 741, 805, 873, 933, 997, 1073, 1133, 1205,
    1289, 1377, 1453, 1537, 1633, 1725, 1793, 1889, 1989, 2081, 2177, 2293, 2393,
    2497, 2621, 2721, 2833,
]


def by_definition(n):
    getcontext().prec = 60
    third = Decimal(2) / Decimal(3)
    bound = Decimal(n) ** third + Decimal(10) ** -40
    powers = [Decimal(x) ** third for x in range(n + 1)]
    count = 4 * n + 1
    for x in range(1, n):
        for y in range(1, n):
            if powers[x] + powers[y] <= bound:
                count += 4
    return count


def check_data():
    assert [a216877(n) for n in range(len(DATA))] == DATA
    print("formula agrees with the %d terms of A216877" % len(DATA))


def check_definition():
    for n in list(range(0, 61)) + [64, 100, 125]:
        assert a216877(n) == by_definition(n), n
    print("walk equals the definition (60-digit arithmetic) for n = 0..60, 64, 100, 125")


def check_columns():
    for n in range(1, 3001):
        assert a216877(n) == by_columns(n), n
    print("walk equals the exact column count for n = 1..3000")
    random.seed(216877)
    cases = [random.randrange(3000, 300000) for _ in range(60)]
    cases += [125 * k ** 3 for k in (2, 3, 5, 8, 10)]
    cases += [10**5, 10**5 + 1, 10**6 - 1, 10**6]
    for n in cases:
        assert a216877(n) == by_columns(n), n
    print("walk equals the exact column count for %d further n up to 10^6" % len(cases))


if __name__ == "__main__":
    check_data()
    check_definition()
    check_columns()
    print("all checks passed")
