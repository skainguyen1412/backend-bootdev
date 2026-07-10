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

