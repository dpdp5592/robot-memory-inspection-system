# file: memory_health_score.py

import time


def compute_memory_health(memory_item: dict, max_age_seconds: float = 60.0) -> dict:
    """
    根据一条记忆的数据，计算一个简单的“记忆健康度”报告。

    memory_item 是 EpisodicMemory 里的一条记录，例如：
    {
        "trajectory": [...],
        "sensors": {...},
        "timestamp": 12345678.0
    }
    """
    if memory_item is None:
        return {
            "score": 0.0,
            "freshness": 0.0,
            "completeness": 0.0,
            "comment": "没有任何记忆，建议先收集数据。"
        }

    now = time.time()
    age = now - memory_item.get("timestamp", now)

    # 新鲜度：时间越久，freshness 越低
    freshness = 1.0 - min(max(age / max_age_seconds, 0.0), 1.0)

    # 完整度：有轨迹又有传感器就算比较完整
    traj = memory_item.get("trajectory")
    sensors = memory_item.get("sensors")
    if traj and sensors:
        completeness = 1.0
    elif traj or sensors:
        completeness = 0.6
    else:
        completeness = 0.2

    score = round((freshness * 0.6 + completeness * 0.4), 2)

    if score > 0.8:
        comment = "记忆状态良好。"
    elif score > 0.5:
        comment = "记忆一般，可以考虑适当更新。"
    else:
        comment = "记忆质量较差，建议重新采集或修复。"

    return {
        "score": score,
        "freshness": round(freshness, 2),
        "completeness": round(completeness, 2),
        "comment": comment
    }
