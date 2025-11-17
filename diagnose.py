# file: diagnose.py

import time
import json

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


def simple_diagnose(memory: EpisodicMemory, key: str):
    data = memory.get(key)
    if data is None:
        report = {
            "issue_type": "missing_memory",
            "confidence": 0.9,
            "evidence": [f"key '{key}' not found"],
            "recommended_fix": ["collect_more_data"]
        }
    else:
        report = {
            "issue_type": "ok",
            "confidence": 0.95,
            "evidence": ["memory exists"],
            "recommended_fix": []
        }

    print("诊断结果：")
    print(json.dumps(report, ensure_ascii=False, indent=4))
    return report


if __name__ == "__main__":
    mem = EpisodicMemory()

    print("【第一次年检】什么记忆都没有：")
    simple_diagnose(mem, "demo_traj")

    print("\n现在往记忆里加一条记录……\n")
    # 给机器人加一条“demo_traj”的记忆
    fake_traj = [0, 1, 2, 3]       # 假装是机器人的轨迹
    fake_sensors = {"force": 0.1}  # 假装是传感器信息
    mem.add("demo_traj", fake_traj, fake_sensors)

    print("【第二次年检】已经有记忆了：")
    simple_diagnose(mem, "demo_traj")

