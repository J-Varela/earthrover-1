import math


def simulate_lidar(rover, obstacles, max_range=5.0, rays=36):
    """Simulate a 2D lidar scan from the rover's current position.

    Args:
        rover: Object with x, y, and heading attributes.
        obstacles: List of dictionaries with "x" and "y" coordinates.
        max_range: Maximum lidar range in the same units as rover and obstacles.
        rays: Number of discrete rays to emit around the rover.

    Returns:
        A list of scan results. Each entry contains "angle" and "distance".
    """

    scans = []

    # Emit a set number of rays evenly around the rover.
    for i in range(rays):
        angle_deg = rover.heading + (i * 360 / rays)
        angle = math.radians(angle_deg)

        # Initialize the ray distance to the maximum range.
        best_distance = max_range

        for obstacle in obstacles:
            dx = obstacle["x"] - rover.x
            dy = obstacle["y"] - rover.y

            # Compute the straight-line distance to the obstacle.
            distance = math.sqrt(dx * dx + dy * dy)
            obstacle_angle = math.atan2(dy, dx)

            # Find the angular difference between the ray and obstacle direction.
            diff = abs(math.atan2(
                math.sin(angle - obstacle_angle),
                math.cos(angle - obstacle_angle),
            ))

            # Treat obstacles within a small angular window as hit candidates.
            if diff < math.radians(5) and distance < best_distance:
                best_distance = distance

        scans.append({
            "angle": angle_deg,
            "distance": round(best_distance, 2)
        })

    return scans