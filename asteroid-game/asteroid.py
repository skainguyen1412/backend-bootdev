import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", (self.x, self.y), self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position = self.velocity * dt
