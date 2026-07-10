class Siege:
    def __init__(self, max_speed: int, efficiency: int) -> None:
        self.max_speed = max_speed
        self.efficiency = efficiency

    def get_trip_cost(self, distance: int, food_price: int) -> float:
        return (distance / self.efficiency) * food_price

    def get_cargo_volume(self) -> float | None:
        pass


class BatteringRam(Siege):
    def __init__(
        self,
        max_speed: int,
        efficiency: int,
        load_weight: int,
        bed_area: int,
    ) -> None:
        super().__init__(max_speed, efficiency)
        self.load_weight = load_weight
        self.bed_area = bed_area

    def get_trip_cost(self, distance: int, food_price: int) -> float:
        return super().get_trip_cost(distance, food_price) + (load_weight * 0.01)

    def get_cargo_volume(self) -> float:
        return self.bed_area * 2


class Catapult(Siege):
    def __init__(self, max_speed: int, efficiency: int, cargo_volume: int) -> None:
        super().__init__(max_speed, efficiency)
        self.cargo_volume = cargo_volume

    def get_cargo_volume(self) -> int:
        return self.cargo_volume
