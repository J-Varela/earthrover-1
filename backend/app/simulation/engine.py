import threading


class SimulationEngine:
    def __init__(self, rover):
        self.rover = rover
        self._thread = None
        self._stop_event = threading.Event()

    def start(self):
        if self._thread and self._thread.is_alive():
            return

        self._stop_event.clear()
        self._thread = threading.Thread(target=self.run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()

        if self._thread:
            self._thread.join(timeout=1)

    def run(self):
        while not self._stop_event.is_set():
            self.rover.update()
            if self._stop_event.wait(0.1):
                break