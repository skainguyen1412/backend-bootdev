class Human:
    def sprint_right(self) -> None:
        

    def sprint_left(self) -> None:
        pass

    def sprint_up(self) -> None:
        pass

    def sprint_down(self) -> None:
        pass

    def __raise_if_cannot_sprint(self) -> None:
        pass

    def __use_sprint_stamina(self) -> None:
        pass

    # don't touch below this line

    def move_right(self) -> None:
        self.__pos_x += self.__speed

    def move_left(self) -> None:
        self.__pos_x -= self.__speed

    def move_up(self) -> None:
        self.__pos_y += self.__speed

    def move_down(self) -> None:
        self.__pos_y -= self.__speed

    def get_position(self) -> tuple[int, int]:
        return self.__pos_x, self.__pos_y

    def __init__(self, pos_x: int, pos_y: int, speed: int, stamina: int) -> None:
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__speed = speed
        self.__stamina = stamina

