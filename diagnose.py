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
    # 先不加任何记忆，故意触发“缺失记忆”的报告
    simple_diagnose(mem, "demo_traj")
