import unittest

from pydantic import ValidationError

from app.models.mission import Mission


class MissionModelTests(unittest.TestCase):
    def test_accepts_finite_coordinates(self):
        mission = Mission(target_x=1.25, target_y=-2.5)

        self.assertEqual(mission.target_x, 1.25)
        self.assertEqual(mission.target_y, -2.5)

    def test_rejects_non_finite_coordinates(self):
        invalid_values = [float("nan"), float("inf"), float("-inf")]

        for value in invalid_values:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    Mission(target_x=value, target_y=0.0)

                with self.assertRaises(ValidationError):
                    Mission(target_x=0.0, target_y=value)


if __name__ == "__main__":
    unittest.main()
