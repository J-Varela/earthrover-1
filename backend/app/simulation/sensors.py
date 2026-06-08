import math
from app.simulation.world import OBSTACLES


def nearest_obstacle_distance(x: float, y: float) -> float:
    if not OBSTACLES:
        return 999.0

    distances = [
        math.sqrt((obs["x"] - x) ** 2 + (obs["y"] - y) ** 2)
        for obs in OBSTACLES
    ]

    return round(min(distances), 2)