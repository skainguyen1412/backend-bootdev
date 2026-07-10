from main import Human

TestCase = tuple[int, int, int, str, int, int]

run_cases: list[TestCase] = [
    (0, 0, 5, "left", -5, 0),
    (0, 0, 5, "right", 5, 0),
    (0, 0, 5, "up", 0, 5),
]

submit_cases: list[TestCase] = run_cases + [
    (0, 0, 5, "down", 0, -5),
    (10, 10, 2, "left", 8, 10),
    (10, 10, 2, "right", 12, 10),
    (10, 10, 2, "up", 10, 12),
    (10, 10, 2, "down", 10, 8),
]


def test(
    pos_x: int,
    pos_y: int,
    speed: int,
    move_direction: str,
    expected_output_x: int,
    expected_output_y: int,
) -> bool:
    print("---------------------------------")
    print("Inputs:")
    print(f" * pos_x: {pos_x}")
    print(f" * pos_y: {pos_y}")
    print(f" * speed: {speed}")
    print(f" * move_direction: {move_direction}")
    expected_output = (expected_output_x, expected_output_y)
    human = Human(pos_x, pos_y, speed)
    if move_direction == "left":
        human.move_left()
    elif move_direction == "right":
        human.move_right()
    elif move_direction == "up":
        human.move_up()
    elif move_direction == "down":
        human.move_down()
    result = human.get_position()
    print(f"Expected x: {expected_output_x}")
    print(f"Actual   x: {result[0]}")
    print(f"Expected y: {expected_output_y}")
    print(f"Actual   y: {result[1]}")
    if result == expected_output:
        return True
    return False


def main() -> None:
    passed = 0
    failed = 0
    skipped = len(submit_cases) - len(test_cases)
    for test_case in test_cases:
        correct = test(*test_case)
        if correct:
            print("Pass")
            passed += 1
        else:
            print("Fail")
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

