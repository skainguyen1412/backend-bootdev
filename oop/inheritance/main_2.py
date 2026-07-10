class Human:
    def __init__(self, name: str) -> None:
        self.__name = name

    def get_name(self) -> str:
        return self.__name


## don't touch above this line


class Archer(Human):
    def __init__(self, name: str, num_arrows: int) -> None:
        super().__init__(name)
        self.__num_arrows = num_arrows

    def get_num_arrows(self) -> int:
        return self.__num_arrows

    def use_arrows(self, num: int) -> None:
        if self.__num_arrows < num:
            raise ValueError("not enough arrows")

        self.__num_arrows -= num


class Crossbowman(Archer):
    def __init__(self, name: str, num_arrows: int) -> None:
        super().__init__(name, num_arrows)

    def triple_shot(self, target: Human) -> str:
        self.use_arrows(3)
        name = target.get_name()

        return f"{name} was shot by 3 crossbow bolts"
