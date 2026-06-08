import asyncio
import threading
import time
import unittest
from unittest import mock

import app.main as main
from app.simulation.engine import SimulationEngine


class _CountingRover:
    def __init__(self):
        self.update_count = 0
        self.updated = threading.Event()

    def update(self):
        self.update_count += 1
        self.updated.set()


class SimulationEngineTests(unittest.TestCase):
    def test_stop_halts_background_thread(self):
        rover = _CountingRover()
        engine = SimulationEngine(rover)

        engine.start()
        self.assertTrue(rover.updated.wait(timeout=1), "engine never performed an update")

        engine.stop()
        count_after_stop = rover.update_count
        time.sleep(0.25)

        self.assertFalse(engine._thread.is_alive())
        self.assertEqual(rover.update_count, count_after_stop)


class LifespanTests(unittest.TestCase):
    def test_lifespan_starts_and_stops_engine(self):
        fake_engine = mock.Mock()

        async def exercise_lifespan():
            with mock.patch.object(main, "engine", fake_engine):
                async with main.lifespan(main.app):
                    fake_engine.start.assert_called_once_with()
                    fake_engine.stop.assert_not_called()

            fake_engine.stop.assert_called_once_with()

        asyncio.run(exercise_lifespan())


if __name__ == "__main__":
    unittest.main()
