# file: episodic_memory.py

import time

class EpisodicMemory:
    def __init__(self):
        self.store = {}

    def add(self, key, trajectory, sensors):
        self.store[key] = {
            "trajectory": trajectory,
            "sensors": sensors,
            "timestamp": time.time()
        }

    def get(self, key):
        return self.store.get(key, None)
