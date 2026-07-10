class Human:
    def __init__(self, pos_x: int, pos_y: int, speed: int) -> None:
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__speed = speed

    def move_right(self) -> None:
        self.__pos_x += self.__speed

    def move_left(self) -> None:
        self.__pos_x -= self.__speed

    def move_up(self) -> None:
        self.__pos_y += self.__speed

    def move_down(self) -> None:
        self.__pos_y -= self.__speed

    def get_position(self) -> tuple[int, int]:
        return (self.__pos_x, self.__pos_y)

