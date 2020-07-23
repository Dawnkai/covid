import pygame as game
from settings import LOGO_IMAGE, BACKGROUND_IMAGE, DISPLAY_SIZE, CONTAINER_SIZE


class Container:
    """ Main container used for simulations"""
    def __init__(self):
        
        if CONTAINER_SIZE[0] > DISPLAY_SIZE[0] or CONTAINER_SIZE[1] > DISPLAY_SIZE[1]:
            raise ValueError("Container is bigger than display.")

        self.position = (0,0)
        self.size = CONTAINER_SIZE
        self.image = game.image.load(BACKGROUND_IMAGE)
        self.image = game.transform.scale(self.image, self.size)
        self.center = (self.size[0] / 2, self.size[1] / 2)
        self.borders = self._get_borders()
    

    def _center(self):
        """ Automatically center the container, if possible. """
        pos_x = (DISPLAY_SIZE[0] - self.size[0]) / 2
        pos_y = (DISPLAY_SIZE[1] - self.size[1]) / 2
        self.position = (int(pos_x), int(pos_y))
        self.borders = self._get_borders()


    def _get_borders(self):
        """ Automatically calculate container borders.
        :return: dict with borders
        """
        return {
            "left": self.position[0],
            "right": self.position[0] + self.size[0],
            "up": self.position[1],
            "down": self.position[1] + self.size[1]
        }


class Entity:
    """ Class representing in-game object
    :param pos: position of the object (as a tuple)
    :param size: size of the object (as a tuple)
    :param image: image file of the object's sprite
    :param speed: movement speed of the object
    :param parent: container in which the entity is located
    """
    def __init__(self, pos, size, image, speed, parent):

        if pos[0] > DISPLAY_SIZE[0] or pos[1] > DISPLAY_SIZE[1]:
            raise ValueError("Entity is bigger than display.")

        self.position = pos
        self.size = size
        self.speed = speed
        self.image = game.image.load(image)
        self.parent = parent
        # Resize object sprite to fit hitbox
        self.image = game.transform.scale(self.image, self.size)
    

    def _center(self):
        """ Automatically center the object, if possible """
        pos_x = (DISPLAY_SIZE[0] - self.size[0]) / 2
        pos_y = (DISPLAY_SIZE[1] - self.size[1]) / 2
        self.position = (int(pos_x), int(pos_y))
    

    def _move(self, offset_x, offset_y):
        """ Moves the object on the screen (changes it's position)
        :param offset_x: How many units to move on the x axis
        :param offset_y: How many units to move on the y axis
        """

        # If object moves beyond x axis border
        if (self.position[0] + offset_x) < self.parent.borders["left"]:
            self.position = (self.parent.borders["left"], self.position[1])
            return

        elif (self.position[0] + offset_x + self.size[0]) > self.parent.borders["right"]:
            self.position = (self.parent.borders["right"] - self.size[0], self.position[1])
            return

        # If object moves beyond y axis border
        if (self.position[1] + offset_y) < self.parent.borders["up"]:
            self.position = (self.position[0], self.parent.borders["up"])
            return

        elif (self.position[1] + offset_y + self.size[1]) > self.parent.borders["down"]:
            self.position = (self.position[0], self.parent.borders["down"] - self.size[1])
            return
        
        # Otherwise move the object normally
        self.position = (self.position[0] + offset_x, self.position[1] + offset_y)


class App:
    """ Main application window """
    def __init__(self):
        game.init()
        game.display.set_caption("Atom Collisions")

        self.logo = game.image.load(LOGO_IMAGE)
        game.display.set_icon(self.logo)
        self.display = game.display.set_mode(DISPLAY_SIZE)
        self.running = True
        # FPS clock
        self.clock = game.time.Clock()

        # Main container for simulations
        self.container = Container()
        self.container._center()

        # Test object for movement testing
        self.test_entity = Entity((0,0), (50, 50), LOGO_IMAGE, 15, self.container)
        self.test_entity._center()


    def _start(self):
        """ Function that starts the program """

        while self.running:
            # Main loop
            for event in game.event.get():
                if event.type == game.QUIT:
                    self.running = False

                elif event.type == game.KEYDOWN:
                    # Pressing arrow buttons makes the object move
                    if event.key == game.K_LEFT:
                        self.test_entity._move((self.test_entity.speed * -1), 0)
                    elif event.key == game.K_RIGHT:
                        self.test_entity._move(self.test_entity.speed, 0)
                    elif event.key == game.K_UP:
                        self.test_entity._move(0, (self.test_entity.speed * -1))
                    elif event.key == game.K_DOWN:
                        self.test_entity._move(0, self.test_entity.speed)

            # Tick Frames
            self._tick()


    def _tick(self):
        """ Frame function - called every frame """
        # Draw container each frame (prevents image duplication on movement)
        self.display.blit(self.container.image, self.container.position)
        # Draw test entity
        self.display.blit(self.test_entity.image, self.test_entity.position)
        # Update screen
        game.display.update()
        self.clock.tick(60)


if __name__ == '__main__':
    app = App()
    app._start()
