from c6_l9 import Card

SUITS: list[str] = ["Clubs", "Diamonds", "Hearts", "Spades"]

RANKS: list[str] = [
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "Jack",
    "Queen",
    "King",
    "Ace",
]

TestCase = tuple[str, str, str, str, bool, bool]

run_cases: list[TestCase] = [
    ("Ace", "Hearts", "Queen", "Hearts", False, True),
    ("2", "Spades", "2", "Hearts", False, True),
]

submit_cases: list[TestCase] = run_cases + [
    ("Ace", "Spades", "Ace", "Spades", True, False),
    ("3", "Diamonds", "7", "Clubs", False, False),
    ("King", "Clubs", "King", "Hearts", False, False),
    ("Queen", "Diamonds", "Jack", "Spades", False, True),
    ("10", "Hearts", "10", "Hearts", True, False),
]


def test(
    rank_1: str,
    suit_1: str,
    rank_2: str,
    suit_2: str,
    expected_eq: bool,
    expected_gt: bool,
) -> bool:
    print("---------------------------------")
    print(f"Inputs: {rank_1} of {suit_1}, {rank_2} of {suit_2}")
    print("Expected:")
    print(f" * Equal: {expected_eq}")
    print(f" * Greater than: {expected_gt}")
    print(f" * Less than: {not (expected_eq or expected_gt)}")

    card_1 = Card(rank_1, suit_1)
    card_2 = Card(rank_2, suit_2)
    result_eq = card_1 == card_2
    result_gt = card_1 > card_2
    result_lt = card_1 < card_2
    print("Actual:")
    print(f" * Equal: {result_eq}")
    if result_eq != expected_eq:
        print("Fail")
        return False
    print(f" * Greater than: {result_gt}")
    if result_gt != expected_gt:
        print("Fail")
        return False
    print(f" * Less than: {result_lt}")
    if result_lt != (not (expected_eq or expected_gt)):
        print("Fail")
        return False
    print("Pass")
    return True


def main() -> None:
    passed = 0
    failed = 0
    skipped = len(submit_cases) - len(test_cases)
    for test_case in test_cases:
        correct = test(*test_case)
        if correct:
            passed += 1
        else:
            failed += 1
    if failed == 0:
        print("============= PASS ==============")
    else:
        print("============= FAIL ==============")
    if skipped > 0:
        print(f"{passed} passed, {failed} failed, {skipped} skipped")
    else:
        print(f"{passed} passed, {failed} failed")


test_cases: list[TestCase] = submit_cases
if "__RUN__" in globals():
    test_cases = run_cases

main()
