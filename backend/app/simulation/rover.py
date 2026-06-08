import math
import threading
from typing import Optional

from app.simulation.lidar import simulate_lidar
from app.simulation.sensors import nearest_obstacle_distance
from app.simulation.world import OBSTACLES


class Rover:
    """A simple simulation model for a rover.

    Tracks position, heading, speed, battery state, and path history.
    Commands update the rover state, and telemetry returns a status snapshot.
    """

    def __init__(self):
        self._lock = threading.RLock()
        # Current position in world coordinates.
        self.x: float = 0.0
        self.y: float = 0.0
        # Heading in degrees (0 points to the positive x axis).
        self.heading: float = 0.0
        # Current speed; positive for forward, negative for backward.
        self.speed: float = 0.0
        # Remaining battery percentage.
        self.battery: float = 100.0
        # Path history, stored as a list of visited coordinates.
        self.path: list = [(0.0, 0.0)]
        # Current mission target.
        self.mission: Optional[dict] = None

    @staticmethod
    def _required_battery(distance: float) -> float:
        return 0.2 * distance

    def _consume_battery(self, distance: float, *, cancel_mission: bool = False) -> bool:
        required = self._required_battery(distance)
        if self.battery + 1e-9 < required:
            self.battery = 0.0
            self.speed = 0.0
            if cancel_mission:
                self.mission = None
            return False

        self.battery = max(self.battery - required, 0.0)
        return True

    def command(self, action: str):
        """Execute a rover command and update the internal state."""
        with self._lock:
            self.mission = None

            if action == "forward":
                if not self._consume_battery(1.0):
                    return

                # Predict the next position and check for nearby obstacles.
                next_x = self.x + math.cos(math.radians(self.heading))
                next_y = self.y + math.sin(math.radians(self.heading))
                if nearest_obstacle_distance(next_x, next_y) < 0.75:
                    self.battery = min(self.battery + self._required_battery(1.0), 100.0)
                    self.speed = 0.0
                    return

                # Move one unit forward in the current heading.
                self.x = next_x
                self.y = next_y
                self.speed = 1.0
                self.path.append((round(self.x, 2), round(self.y, 2)))

            elif action == "backward":
                if not self._consume_battery(1.0):
                    return

                # Predict the next backward position and check for nearby obstacles.
                next_x = self.x - math.cos(math.radians(self.heading))
                next_y = self.y - math.sin(math.radians(self.heading))
                if nearest_obstacle_distance(next_x, next_y) < 0.75:
                    self.battery = min(self.battery + self._required_battery(1.0), 100.0)
                    self.speed = 0.0
                    return

                # Move one unit backward in the current heading.
                self.speed = -1.0
                self.x = next_x
                self.y = next_y
                self.path.append((round(self.x, 2), round(self.y, 2)))

            elif action == "left":
                # Rotate left by 15 degrees without changing position.
                self.heading = (self.heading - 15) % 360
                self.speed = 0.0

            elif action == "right":
                # Rotate right by 15 degrees without changing position.
                self.heading = (self.heading + 15) % 360
                self.speed = 0.0

            elif action == "stop":
                # Stop the rover while preserving position and heading.
                self.speed = 0.0

    def set_mission(self, target_x: float, target_y: float):
        with self._lock:
            self.mission = {"target_x": target_x, "target_y": target_y}

    def update(self):
        """Update rover mission state and move toward the target."""
        with self._lock:
            if self.mission is None:
                return

            target_x = self.mission.get("target_x")
            target_y = self.mission.get("target_y")

            if target_x is None or target_y is None:
                return

            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance <= 1e-9:
                self.mission = None
                self.speed = 0.0
                return

            # Steer directly toward the target.
            self.heading = math.degrees(math.atan2(dy, dx)) % 360
            step_distance = min(1.0, distance)

            if not self._consume_battery(step_distance, cancel_mission=True):
                return

            next_x = self.x + math.cos(math.radians(self.heading)) * step_distance
            next_y = self.y + math.sin(math.radians(self.heading)) * step_distance

            if nearest_obstacle_distance(next_x, next_y) < 0.75:
                self.battery = min(
                    self.battery + self._required_battery(step_distance),
                    100.0,
                )
                self.mission = None
                self.speed = 0.0
                return

            self.x = next_x
            self.y = next_y
            self.path.append((round(self.x, 2), round(self.y, 2)))

            if step_distance >= distance:
                self.mission = None
                self.speed = 0.0
                return

            self.speed = 1.0

    def telemetry(self):
        """Return the current rover status for API responses."""
        with self._lock:
            return {
                "x": round(self.x, 2),
                "y": round(self.y, 2),
                "heading": round(self.heading, 2),
                "speed": self.speed,
                "battery": round(max(self.battery, 0), 2),
                "nearest_obstacle_distance": nearest_obstacle_distance(self.x, self.y),
                "lidar": simulate_lidar(self, OBSTACLES),
                "mission": self.mission,
                # Keep the latest 100 path points to limit payload size.
                "path": self.path[-100:],
            }
