from main_3 import Archer, Hero

HeroArgs = tuple[str, int]
ArcherArgs = tuple[str, int, int]
TestCase = tuple[HeroArgs, ArcherArgs, int | None, str | None, bool]

run_cases: list[TestCase] = [
    (("Hercules", 200), ("Pericles", 100, 2), 190, None, False),
    (("Zeus", 1000), ("Hades", 900, 1), None, "not enough arrows", True),
    (("Aquiles", 150), ("Aneas", 80, 1), 140, None, False),
]

submit_cases: list[TestCase] = run_cases + [
    (("Hecate", 300), ("Ares", 50, 0), None, "not enough arrows", True),
    (("Icarus", 60), ("Daedalus", 40, 2), 40, None, True),
]


def test(
    hero_args: HeroArgs,
    archer_args: ArcherArgs,
    expected_result: int | None,
    expected_err: str | None = None,
    twice: bool = False,
) -> bool:
    hero = Hero(*hero_args)
    archer = Archer(*archer_args)

    print("---------------------------------")
    print(f"Hero:   {hero.get_name()}, Health: {hero.get_health()}")
    print(f"Archer: {archer.get_name()}, Arrows: {archer_args[2]}")
    print("")
    try:
        print(f"{archer.get_name()} tries to shoot {hero.get_name()}")
        archer.shoot(hero)
        if twice:
            print(f"{archer.get_name()} tries to shoot {hero.get_name()} again")
            archer.shoot(hero)
        result = hero.get_health()

        if expected_err:
            print(f"Expected exception: {expected_err}")
            print("Actual exception:   None")
            return False

        print(f"Expected {hero.get_name()} health: {expected_result}")
        print(f"Actual   {hero.get_name()} health: {result}")
        if result == expected_result:
            return True
        return False
    except Exception as error:
        print(f"Expected Exception: {expected_err}")
        print(f"Actual Exception:   {error}")
        if str(error) == expected_err:
            return True
        else:
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
