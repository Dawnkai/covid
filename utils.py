# Utility functions
import math


def calculate_distance(A, B):
    """Get distance between atoms A and B."""
    return math.sqrt((A.x - B.x) ** 2 + (A.y - B.y) ** 2)

def check_collision(A, B):
    """Check if atom A and B collided."""
    return calculate_distance(A, B) < 21 / 10 * A.radius

def get_statistics(atoms):
    """Count number of infected atoms and healthy atoms."""
    healthy = 0
    infected = 0
    for atom in atoms[1:]:
        if atom.type == "HEALTHY":
            healthy += 1
        else:
            infected += 1
    return [healthy, infected]
