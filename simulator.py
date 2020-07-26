import pygame as game
import random
import math
from settings import LOGO_IMAGE, BACKGROUND_IMAGE, CONTAINER_SIZE


# FIXME: Maybe there is a better way to store rgb colors than dict?
color = {
    "INFECTED": (255, 0, 0), # Red in RGB
    "HEALTHY": (0, 0, 255) # Blue in RGB
}


class Container:
    """ Main container used for simulations"""
    def __init__(self):
        self.position = (0,0)
        self.size = CONTAINER_SIZE
        self.image = game.image.load(BACKGROUND_IMAGE)
        # Scale background image to fit container size
        self.image = game.transform.scale(self.image, self.size)


    @property
    def borders(self):
        """ Automatically calculate container borders.
        :return: dict with borders
        """
        return {
            "left": self.position[0],
            "right": self.position[0] + self.size[0],
            "up": self.position[1],
            "down": self.position[1] + self.size[1]
        }


class Atom:
    """ Class representing single atom """

    def __init__(self, radius, screen, container):
        """ Generate atom
        :param radius: radius of an atom
        :param screen: reference to main display
        :param container: container object where to put atoms
        """

        # Start positions on x and y axis
        self.x = random.randint(radius, container.size[0]-radius)
        self.y = random.randint(radius, container.size[1]-radius)

        self.radius = radius
        self.color = color['HEALTHY']
        self.thickness = 1
        self.speed = random.random()
        self.angle = random.uniform(0, math.pi*2)
        # Main display
        self.screen = screen
        # Container in which atoms are present
        self.container = container


    def draw(self):
        """ Draw atom on screen """
        game.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius, self.thickness)


    def bounce(self):
        """ Bounce Atom from the walls """

        # Use "Exceeding boundaries" section for calculating new direction
        # http://archive.petercollingridge.co.uk/book/export/html/6

        if self.x > self.container.size[0] - self.radius:
            self.x = 2*(self.container.size[0] - self.radius) - self.x
            self.angle = - self.angle

        elif self.x < self.radius:
            self.x = 2*self.radius - self.x
            self.angle = - self.angle

        if self.y > self.container.size[1] - self.radius:
            self.y = 2*(self.container.size[1] - self.radius) - self.y
            self.angle = math.pi - self.angle

        elif self.y < self.radius:
            self.y = 2*self.radius - self.y
            self.angle = math.pi - self.angle


    def move(self):
        """ Move Atom by one frame """
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.bounce()


class App:
    """ Main application window """

    def __init__(self, radius, number_of_atoms):
        """ Generate main game
        :param radius: radius of single atom
        :param number_of_atoms: number of atoms in container
        """
        game.init()
        game.display.set_caption("Atom Collisions")

        self.logo = game.image.load(LOGO_IMAGE)
        game.display.set_icon(self.logo)
        self.display = game.display.set_mode(CONTAINER_SIZE)
        self.running = True
        # FPS clock
        self.clock = game.time.Clock()
        # Container with atoms
        self.container = Container()
        # Generate atoms
        self.atoms = [Atom(radius, self.display, self.container) for i in range(number_of_atoms)]
    

    def _start(self):
        """ Start the simulation """
        while self.running:

            for event in game.event.get():
                if event.type == game.QUIT:
                    self.running = False
            
            self._tick()


    def _tick(self):
        """ Frame function - called every frame """
        self.display.blit(self.container.image, self.container.position)
        for atom in self.atoms:
            atom.move()
            atom.draw()
        game.display.flip()
        # Tick frame, increasing tick will result in faster simulation
        self.clock.tick(60)


if __name__ == '__main__':
    app = App(15, 10)
    app._start()
