# Simulation
import os
import pygame as game
import random
import math
from settings import LOGO_IMAGE, BACKGROUND_IMAGE, CONTAINER_SIZE, TICK_FRAMES
from enum import Enum
import sys
from utils import calculate_distance, check_collision


# FIXME: Maybe there is a better way to store rgb colors than dict?
color = {
    "INFECTED": (255, 0, 0),  # Red in RGB
    "HEALTHY": (0, 0, 255),  # Blue in RGB
    "CARRIER": (255, 0, 255),  # Purple in RGB
}


class Container:
    """Main container used for simulations."""

    def __init__(self, radius, number_of_atoms, velocity, time_coeff, display):
        """Generate new container.

        :param radius: radius of single atom
        :param number_of_atoms: number of atoms in container
        :param velocity: maximum velocity of single atom
        :param time_coeff: time coefficient to limit simulation time
        :param display: simulation display
        """
        self.position = (0, 0)
        self.size = CONTAINER_SIZE
        self.image = game.image.load(BACKGROUND_IMAGE)
        self.display = display
        # Scale background image to fit container size
        self.image = game.transform.scale(self.image, self.size)
        # Generate atoms
        self.atoms = [
            Atom(radius, self.display, self.size, velocity)
            for i in range(number_of_atoms + 1)
        ]
        # Total ticks since start of the simulation
        self.total_ticks = 0
        self.atom_zero_collisions = 0
        # Ticks between atom zero collisions
        self.ticks_between_collisions = 0
        self.display = display
        # Distance travelled by atom zero between collisions
        self.atom_zero_distances = []

    @property
    def num_healthy(self):
        """Return number of healthy atoms."""
        return len([atom for atom in self.atoms[1:] if atom.type == "HEALTHY"])

    @property
    def num_infected(self):
        """Return number of infected atoms."""
        return len([atom for atom in self.atoms[1:] if atom.type == "INFECTED"])

    @property
    def atom_zero_avg_collisions(self):
        """Return red atom hit frequency."""
        try:
            return round(self.atom_zero_collisions / self.total_ticks, 4)
        except ZeroDivisionError:
            return 0

    @property
    def avg_collision_distance(self):
        """Average distance between collisions."""
        try:
            return round(sum(self.atom_zero_distances) / self.atom_zero_collisions, 3)
        except ZeroDivisionError:
            return 0

    @property
    def borders(self):
        """Automatically calculate container borders.

        :return: dict with borders
        """
        return {
            "left": self.position[0],
            "right": self.position[0] + self.size[0],
            "up": self.position[1],
            "down": self.position[1] + self.size[1],
        }

    def _init_atom_zero(self):
        """Create arom zero at (0,0) coordinates that will spread the virus."""
        self.atoms[0].x = self.atoms[0].radius
        self.atoms[0].y = self.borders["down"] - self.atoms[0].radius
        self.atoms[0].color = color["INFECTED"]
        self.atoms[0].angle = 5 * math.pi / 4
        self.atoms[0].type = "ZERO"

    def _update(self):
        """Update simulation - function called every frame."""
        for atom in self.atoms:
            atom.move()
            self._check_for_collisions()
            atom.draw()
        self.ticks_between_collisions += 1
        self.total_ticks += 1

    def _collide(self, atom_A, atom_B):
        """Function that calculates new angles and speeds for collided particles.

        :param atom_A: first atom
        :param atom_B: second atom
        """

        # Use "Collisions" section for calculating new angle and speed
        # http://archive.petercollingridge.co.uk/book/export/html/6

        # Calculate collisions like on flat surface with arcus tangens
        tangent = math.atan2(atom_A.y - atom_B.y, atom_A.x - atom_B.x)
        # Calculate angle of collision
        angle = 0.5 * math.pi + tangent

        # Calculate new angles
        atom_A.angle = 2 * tangent - atom_A.angle
        atom_B.angle = 2 * tangent - atom_B.angle

        # Swap exchanged speeds
        (atom_A.speed, atom_B.speed) = (atom_B.speed, atom_A.speed)

        # Calculate new directions
        atom_A.x += math.sin(angle)
        atom_A.y -= math.cos(angle)
        atom_B.x -= math.sin(angle)
        atom_B.y += math.cos(angle)

    def _check_for_collisions(self):
        """Check if any atoms have collided."""
        for atom_A in self.atoms:
            for atom_B in self.atoms:
                if atom_A != atom_B:
                    if check_collision(atom_A, atom_B):

                        if atom_A.type == "ZERO" or atom_B == "ZERO":
                            self.atom_zero_collisions += 1

                            if atom_A.type == "ZERO" and atom_B.type == "HEALTHY":
                                atom_B.type = "INFECTED"
                                atom_B.color = color["CARRIER"]
                                self.atom_zero_distances.append(
                                    self.ticks_between_collisions
                                    * atom_A.velocity_vector
                                )

                            elif atom_A.type == "HEALTHY" and atom_B.type == "ZERO":
                                atom_A.type = "INFECTED"
                                atom_A.color = color["CARRIER"]
                                self.atom_zero_distances.append(
                                    self.ticks_between_collisions
                                    * atom_B.velocity_vector
                                )

                            # If atom zero collided, reset tick between collisions counter
                            self.ticks_between_collisions = 0

                        self._collide(atom_A, atom_B)


class Atom:
    """ Class representing single atom """

    def __init__(self, radius, screen, container_size, velocity):
        """Generate atom.

        :param radius: radius of an atom
        :param screen: reference to simulator display
        :param container_size: size of the simulaiton container
        :param velocity: maximum velocity of an atom
        """

        # Start positions on x and y axis
        self.x = random.randint(radius, container_size[0] - radius)
        self.y = random.randint(radius, container_size[1] - radius)

        self.radius = radius
        self.color = color["HEALTHY"]
        self.thickness = 1
        self.speed = [random.randint(0, velocity), random.randint(0, velocity)]
        self.angle = random.uniform(0, math.pi * 2)
        # Main display
        self.screen = screen
        # Container in which atoms are present
        self.container_size = container_size
        self.type = "HEALTHY"

    @property
    def velocity_vector(self):
        """Calculate resultant velocity."""
        return math.sqrt(self.speed[0] ** 2 + self.speed[1] ** 2)

    def draw(self):
        """Draw atom on screen."""
        game.draw.circle(
            self.screen,
            self.color,
            (int(self.x), int(self.y)),
            self.radius,
            self.thickness,
        )

    def bounce(self):
        """Bounce Atom from the walls."""

        # Use "Exceeding boundaries" section for calculating new direction
        # http://archive.petercollingridge.co.uk/book/export/html/6

        if self.x > self.container_size[0] - self.radius:
            self.x = 2 * (self.container_size[0] - self.radius) - self.x
            self.angle = -self.angle

        elif self.x < self.radius:
            self.x = 2 * self.radius - self.x
            self.angle = -self.angle

        if self.y > self.container_size[1] - self.radius:
            self.y = 2 * (self.container_size[1] - self.radius) - self.y
            self.angle = math.pi - self.angle

        elif self.y < self.radius:
            self.y = 2 * self.radius - self.y
            self.angle = math.pi - self.angle

    def move(self):
        """Move Atom by one frame."""
        self.x += math.sin(self.angle) * self.speed[0]
        self.y -= math.cos(self.angle) * self.speed[1]
        self.bounce()


class Simulation:
    """ Main application window """

    def __init__(self, radius, velocity, number_of_atoms, time_coeff, frame):
        """Generate simulation.

        :param radius: radius of a single atom
        :param velocity: maximum velocity of single atom
        :param number_of_atoms: number of atoms in container
        :param time_coeff: time coefficient - M in task contents
        """
        self.display = game.display.set_mode(CONTAINER_SIZE)
        self.running = True
        # FPS clock
        self.clock = game.time.Clock()
        # Container with atoms
        self.container = Container(
            radius, number_of_atoms, velocity, time_coeff, self.display
        )
        self.duration = (velocity * number_of_atoms * time_coeff) // 10
        self.frame = frame

    @property
    def result_frequency(self):
        return round(
            self.container.atom_zero_collisions / self.container.total_ticks, 4
        )

    @property
    def result_distance(self):
        return round(
            sum(self.container.atom_zero_distances)
            / self.container.atom_zero_collisions,
            3,
        )

    def _start(self):
        """Start the simulation."""

        # Create first infected atom
        self.container._init_atom_zero()

        # Main loop
        while self.running and self.duration != 0:
            self._tick()
            self.frame.update()
            self.duration -= 1

    def _tick(self):
        """Frame function - called every frame."""
        # Draw container
        self.display.blit(self.container.image, self.container.position)

        # Update container
        self.container._update()

        # Update windows
        game.display.flip()

        # Tick frame, increasing tick will result in faster simulation
        self.clock.tick(TICK_FRAMES)

    def _exit(self):
        if self.running == True:
            self.running = False
            game.quit()
