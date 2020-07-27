import pygame as game
import math

class Ball:
    def __init__(self, radius, cord, vel, color, a):
        self.r = radius
        self.v = vel
        self.loc = cord
        self.angle = a
        self.color = color
        self.speed = math.sqrt(self.v[0]**2 + self.v[1]**2)

class Game:
    def __init__(self):
        game.init()
        self.win = game.display.set_mode((800, 600))
        game.display.set_caption("Kolizje")
        self.running = True
        # 3 testing balls
        self.atoms = [Ball(10, [400, 200], [10, 0], (255, 0, 0), math.pi/2), Ball(10, [500, 100], [0, 10], (0, 255, 0), math.pi), Ball(10, [650, 500], [10, 10], (0, 0, 255), 7*math.pi/4)]

    def _start(self):
        while self.running:

            for event in game.event.get():
                if event.type == game.QUIT:
                    self.running = False

            self.win.fill((0, 0, 0))
            for atom in self.atoms:
                game.draw.circle(self.win, atom.color, (int(atom.loc[0]), int(atom.loc[1])), atom.r)
                atom.loc[0] += math.sin(atom.angle) * atom.v[0]
                atom.loc[1] -= math.cos(atom.angle) * atom.v[1]
                self._colide(atom)
                game.display.update()
            game.time.delay(100)
        game.quit()

    # for each atom in self.atoms which is not A check if 2 atoms collide with each other
    def _colide(self, A):
        for at in self.atoms:
            if at != A:
                if collision(A, at):
                    collision_type = parallel(A, at)
                    # A speeds up, B stops
                    if collision_type == 7:
                        A.v = [A.v[0] + at.v[0], A.v[1] + at.v[1]]
                        at.v = [0, 0]
                    # B speeds up, A stops
                    if collision_type == 6:
                        at.v = [A.v[0] + at.v[0], A.v[1] + at.v[1]]
                        A.v = [0, 0]
                    # A and B change velocity and angles
                    if collision_type == 5:
                        A.v, at.v = at.v, A.v
                        A.angle, at.angle = at.angle, A.angle
                    # B gets A horizontal velocity + exchange angles
                    if collision_type == 4:
                        at.v[0] = A.v[0]
                        A.v[0] = 0
                        A.angle, at.angle = at.angle, A.angle
                    # A gets B horizontal velocity + exchange angles
                    if collision_type == 3:
                        A.v[0] = at.v[0]
                        at.v[0] = 0
                        A.angle, at.angle = at.angle, A.angle
                    # B gets A vertical velocity + exchange angles
                    if collision_type == 2:
                        at.v[1] = A.v[1]
                        A.v[1] = 0
                        A.angle, at.angle = at.angle, A.angle
                    # A gets B vertical velocity + exchange angles
                    if collision_type == 1:
                        A.v[1] = at.v[1]
                        at.v[1] = 0
                        A.angle, at.angle = at.angle, A.angle

def distance(A, B):
    dist = math.sqrt((A.loc[0]-B.loc[0])**2 + (A.loc[1]-B.loc[1])**2)
    return dist

def collision(A, B):
    if distance(A, B) < 22/10*A.r:
        return True
    return False

def float_compare(a,b):
    d = 0.01  # tolerance of comparison
    if 0 < a < b-d:
        return 1  # (0, 90) degree
    if b-d <= a:
        return 2  # <90,180) degree

    return 0

# values (1-4) angle difference (0, 90), value 5 angle difference (90, 180), values (6-7) angle =0
# 0 - no collision, 1- x collide 1-> 2, 2- x collide 2-> 1, 3- y collide 1-> 2, 4- y collide 2-> 1,
# 5 - x,y collision, 6 - supercollision 1-> 2, 7 - supercollision 2-> 1
def parallel(A, B):

    # the same direction B hits A
    if A.angle == B.angle and B.speed > A.speed:
        return 7

    # the same direction A hits B
    if A.angle == B.angle and A.speed > B.speed:
        return 6

    # obtuse angle between A and B
    if float_compare(abs(A.angle - B.angle), math.pi/2) == 2:
        return 5

    # B.angle =/= 90 or 270 and acute angle between A and B
    if float_compare(abs(A.angle - B.angle), math.pi/2) == 1 and B.v[0] == 0:
        return 4

    # A.angle =/= 90 or 270 and acute angle between A and B
    if float_compare(abs(A.angle - B.angle), math.pi/2) == 1 and A.v[0] == 0:
        return 3

    # B.angle =/= 0 or 180 and acute angle between A and B
    if float_compare(abs(A.angle - B.angle), math.pi/2) == 1 and B.v[1] == 0:
        return 2

    # A.angle =/= 0 or 180 and acute angle between A and B
    if float_compare(abs(A.angle - B.angle), math.pi/2) == 1 and A.v[1] == 0:
        return 1
    # No collision
    return 0


if __name__ == "__main__":
    app = Game()
    app._start()