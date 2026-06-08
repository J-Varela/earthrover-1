import unittest

from app.simulation.rover import Rover


class RoverMissionTests(unittest.TestCase):
    def test_short_mission_clamps_to_target_without_overshooting(self):
        rover = Rover()
        rover.set_mission(0.6, 0.0)

        rover.update()

        self.assertAlmostEqual(rover.x, 0.6)
        self.assertAlmostEqual(rover.y, 0.0)
        self.assertIsNone(rover.mission)
        self.assertEqual(rover.speed, 0.0)
        self.assertEqual(rover.path[-1], (0.6, 0.0))

    def test_mission_under_half_unit_still_reaches_target(self):
        rover = Rover()
        rover.set_mission(0.4, 0.0)

        rover.update()

        self.assertAlmostEqual(rover.x, 0.4)
        self.assertAlmostEqual(rover.y, 0.0)
        self.assertIsNone(rover.mission)
        self.assertEqual(rover.speed, 0.0)
        self.assertEqual(rover.path[-1], (0.4, 0.0))

    def test_manual_move_cancels_active_mission(self):
        rover = Rover()
        rover.set_mission(0.6, 0.0)

        rover.command("forward")
        rover.update()

        self.assertAlmostEqual(rover.x, 1.0)
        self.assertAlmostEqual(rover.y, 0.0)
        self.assertIsNone(rover.mission)
        self.assertEqual(rover.speed, 1.0)
        self.assertEqual(rover.path[-1], (1.0, 0.0))

    def test_stop_command_cancels_active_mission(self):
        rover = Rover()
        rover.set_mission(3.0, 0.0)

        rover.command("stop")
        rover.update()

        self.assertAlmostEqual(rover.x, 0.0)
        self.assertAlmostEqual(rover.y, 0.0)
        self.assertIsNone(rover.mission)
        self.assertEqual(rover.speed, 0.0)
        self.assertEqual(rover.path, [(0.0, 0.0)])

    def test_turn_command_cancels_active_mission(self):
        rover = Rover()
        rover.set_mission(3.0, 0.0)

        rover.command("left")
        rover.update()

        self.assertAlmostEqual(rover.x, 0.0)
        self.assertAlmostEqual(rover.y, 0.0)
        self.assertEqual(rover.heading, 345.0)
        self.assertIsNone(rover.mission)
        self.assertEqual(rover.speed, 0.0)

    def test_backward_move_respects_obstacle_collision(self):
        rover = Rover()
        rover.x = -1.5
        rover.y = 1.0
        rover.heading = 0.0

        rover.command("backward")

        self.assertAlmostEqual(rover.x, -1.5)
        self.assertAlmostEqual(rover.y, 1.0)
        self.assertEqual(rover.speed, 0.0)
        self.assertEqual(rover.path, [(0.0, 0.0)])

    def test_blocked_mission_clears_active_mission(self):
        rover = Rover()
        rover.set_mission(5.0, 0.0)

        rover.update()
        rover.update()

        self.assertAlmostEqual(rover.x, 1.0)
        self.assertAlmostEqual(rover.y, 0.0)
        self.assertIsNone(rover.mission)
        self.assertEqual(rover.speed, 0.0)
        self.assertEqual(rover.path[-1], (1.0, 0.0))

    def test_depleted_battery_blocks_manual_movement(self):
        rover = Rover()
        rover.battery = 0.1

        rover.command("forward")

        self.assertAlmostEqual(rover.x, 0.0)
        self.assertAlmostEqual(rover.y, 0.0)
        self.assertEqual(rover.speed, 0.0)
        self.assertEqual(rover.battery, 0.0)
        self.assertEqual(rover.path, [(0.0, 0.0)])

    def test_depleted_battery_clears_active_mission_without_moving(self):
        rover = Rover()
        rover.battery = 0.1
        rover.set_mission(3.0, 0.0)

        rover.update()

        self.assertAlmostEqual(rover.x, 0.0)
        self.assertAlmostEqual(rover.y, 0.0)
        self.assertIsNone(rover.mission)
        self.assertEqual(rover.speed, 0.0)
        self.assertEqual(rover.battery, 0.0)
        self.assertEqual(rover.path, [(0.0, 0.0)])

    def test_telemetry_includes_lidar_scan(self):
        rover = Rover()
        telemetry = rover.telemetry()

        self.assertIn("lidar", telemetry)
        self.assertIsInstance(telemetry["lidar"], list)
        self.assertGreater(len(telemetry["lidar"]), 0)
        sample = telemetry["lidar"][0]
        self.assertIn("angle", sample)
        self.assertIn("distance", sample)


if __name__ == "__main__":
    unittest.main()
