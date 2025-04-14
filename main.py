import pygame
import sys
import math
import cmath
import read_svg, cal_coefficients, conf

# Initialize pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = conf.width, conf.height
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graph")

# Colors
WHITE = (255, 255, 255)
BLUE = (52, 122, 235)
PINK = (185, 167, 196)
LIME = (52, 235, 201)
BLACK = (0, 0, 0)
TRANSLUCENT_WHITE = (255, 255, 255, 50)
TRANSLUCENT_LIME = (52, 235, 201, 80)  # LIME with transparency
LIGHT_YELLOW = (255, 255, 128)
TRANSLUCENT_YELLOW = (255, 255, 128, 50)

# Grid sizes
LARGE_GRID_SIZE = conf.grid_size
SMALL_GRID_SIZE = conf.grid_size // 2

origin = [WIDTH // 2, HEIGHT // 2]

# Clock for controlling the frame rate
clock = pygame.time.Clock()

persistent_surface = pygame.Surface((WIDTH, HEIGHT))
persistent_surface.fill(BLACK)


def compute_complex(c, w, t):
    # Compute the complex number using Euler's formula: c * e^(i * w * pi * 2 * t)
    angle = w * 2 * math.pi * t  # angle in radians
    return c * cmath.exp(1j * angle)


class ArrowObject:
    def __init__(
        self,
        start_x,
        start_y,
        angular_frequency,
        size=conf.size,
        coefficient=0.1 + 0j,
        time=0,
        angular_frequency_multiplier=1,
    ):
        self.position = complex(start_x, start_y)
        self.size = size * abs(coefficient)
        self.w = angular_frequency * angular_frequency_multiplier
        self.coefficient = coefficient
        self.triangle_ratio = 0.1
        self.time = time
        self.triangle_angle = 20

    def draw(self, screen, persist=False):
        vector = compute_complex(self.coefficient, self.w, self.time)
        angle = cmath.phase(vector) * 180 / math.pi  # Convert to degrees

        self.x = self.position.real
        self.y = self.position.imag
        starting_pos = (self.x, self.y)
        ending_pos = (
            self.x + self.size * math.cos(math.radians(angle)),
            self.y + self.size * math.sin(math.radians(angle)),
        )
        pygame.draw.line(screen, WHITE, starting_pos, ending_pos, 2)

        # draw the triangle at the tip
        triangle = [
            (ending_pos[0], ending_pos[1]),
            (
                ending_pos[0]
                - self.size
                * self.triangle_ratio
                * math.cos(math.radians(angle + self.triangle_angle)),
                ending_pos[1]
                - self.size
                * self.triangle_ratio
                * math.sin(math.radians(angle + self.triangle_angle)),
            ),
            (
                ending_pos[0]
                - self.size
                * self.triangle_ratio
                * math.cos(math.radians(angle - self.triangle_angle)),
                ending_pos[1]
                - self.size
                * self.triangle_ratio
                * math.sin(math.radians(angle - self.triangle_angle)),
            ),
        ]
        pygame.draw.polygon(screen, WHITE, triangle)

        # draw the circle at the base
        circle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            circle_surface, TRANSLUCENT_YELLOW, (self.size, self.size), self.size, 2
        )
        screen.blit(circle_surface, (self.x - self.size, self.y - self.size))

        if persist:
            pygame.draw.circle(persistent_surface, LIME, ending_pos, 2, 0)

    def update(self, base=complex(origin[0], origin[1])):
        self.time = pygame.time.get_ticks() / 1000
        self.position = base


class Figure:
    def __init__(
        self,
        coefficients,
        angular_frequencies,
        origin=origin,
        angular_frequency_multiplier=0.5,
    ):
        self.coefficients = coefficients
        self.angular_frequencies = [
            w * angular_frequency_multiplier for w in angular_frequencies
        ]
        self.time = 0
        self.origin = complex(origin[0], origin[1])
        self.arrows = []
        self.size = conf.size

        for c, w in zip(self.coefficients, self.angular_frequencies):
            base = complex(self.origin.real, self.origin.imag)
            vec = compute_complex(c, w, self.time)
            arrow = ArrowObject(
                start_x=base.real,
                start_y=base.imag,
                angular_frequency=w,
                coefficient=c,
            )
            self.arrows.append(arrow)
            base += vec * self.size

    def draw(self, screen):
        for i, arrow in enumerate(self.arrows):
            persist = i == len(self.arrows) - 1  # True if it's the last arrow
            arrow.draw(screen, persist=persist)

    def update(self):
        self.time = pygame.time.get_ticks() / 1000
        base = complex(self.origin.real, self.origin.imag)
        for arrow in self.arrows:
            arrow.update(base)
            vec = compute_complex(arrow.coefficient, arrow.w, self.time)
            base += vec * self.size


def draw_graph():
    """Draw the graph with grid lines."""
    # Draw the small grid lines with respect to origin
    small_grid_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for x in range(origin[0] % SMALL_GRID_SIZE, WIDTH, SMALL_GRID_SIZE):
        pygame.draw.line(small_grid_surface, TRANSLUCENT_LIME, (x, 0), (x, HEIGHT), 1)
    for y in range(origin[1] % SMALL_GRID_SIZE, HEIGHT, SMALL_GRID_SIZE):
        pygame.draw.line(small_grid_surface, TRANSLUCENT_LIME, (0, y), (WIDTH, y), 1)
    screen.blit(small_grid_surface, (0, 0))
    # Draw the large grid lines with respect to origin
    for x in range(origin[0] % LARGE_GRID_SIZE, WIDTH, LARGE_GRID_SIZE):
        pygame.draw.line(screen, PINK, (x, 0), (x, HEIGHT), 1)
    for y in range(origin[1] % LARGE_GRID_SIZE, HEIGHT, LARGE_GRID_SIZE):
        pygame.draw.line(screen, BLUE, (0, y), (WIDTH, y), 1)

    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 1)
    pygame.draw.line(screen, WHITE, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 1)


def main():
    global scroll

    # arrow = ArrowObject(
    #     start_x=origin[0],
    #     start_y=origin[1],
    #     angular_frequency=0.1,
    #     coefficient=0.5 + 0.5j,
    # )

    # figure = Figure(
    #     coefficients=[0.5 + 0.5j, 0.2 - 0.2j, 0.1 + 0.05j, 0.05 - 0.1j, 0.01 + 0.01j],
    #     angular_frequencies=[0, 1, -1, 2, -2],
    # )

    svg_file = "Pi-symbol.svg"

    points = read_svg.get_points(2500, svg_file)

    coefficients = cal_coefficients.get_coefficients(points, 800)
    coefficients[0] = 0
    angular_frequencies = cal_coefficients.get_angular_frequencies(800)

    # print(coefficients[:10])
    # print(angular_frequencies[:10])

    figure = Figure(
        coefficients=coefficients,
        angular_frequencies=angular_frequencies,
        angular_frequency_multiplier=conf.speed,
    )

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Drawing
        screen.fill(BLACK)
        screen.blit(persistent_surface, (0, 0))

        draw_graph()

        # Create an arrow object
        # arrow.update()
        # arrow.draw(screen)

        figure.update()
        figure.draw(screen)

        pygame.display.flip()
        clock.tick(165)


if __name__ == "__main__":
    main()
