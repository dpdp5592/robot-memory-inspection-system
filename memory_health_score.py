# file: memory_health_score.py

import time


def compute_memory_health(memory_item: dict, max_age_seconds: float = 60.0) -> dict:
    """
    根据一条记忆的数据，计算一个“记忆健康度”报告。

    memory_item 格式示例：
    {
        "trajectory": [...],
        "sensors": {
            "force_log": [...]
        },
        "timestamp": 12345678.0
    }
    """
    # 情况 1：根本没有记忆
    if memory_item is None:
        return {
            "score": 0.0,
            "freshness": 0.0,
            "completeness": 0.0,
            "force_factor": 0.0,
            "comment": "没有任何记忆，建议先收集数据。"
        }

    now = time.time()
    age = now - memory_item.get("timestamp", now)

    # ========= 1. 新鲜度 =========
    # 时间越久，freshness 越低
    freshness = 1.0 - min(max(age / max_age_seconds, 0.0), 1.0)

    # ========= 2. 完整度 =========
    traj = memory_item.get("trajectory")
    sensors = memory_item.get("sensors")
    if traj and sensors:
        completeness = 1.0
    elif traj or sensors:
        completeness = 0.6
    else:
        completeness = 0.2

    # ========= 3. 力传感器因子 =========
    # 如果有 force_log，撞墙多则惩罚分数
    force_factor = 1.0  # 理想情况下，力很小 → factor 接近 1
    force_log = None
    if isinstance(sensors, dict):
        force_log = sensors.get("force_log")

    if force_log and len(force_log) > 0:
        avg_force = sum(force_log) / len(force_log)
        max_force = max(force_log)

        # 简单规则：
        #   平均力越大，认为“撞得越多、越重”
        #   我们做一个 0~1 的归一化，超过 1 就按 1 算
        avg_force_norm = min(avg_force, 1.0)
        max_force_norm = min(max_force, 1.0)

        # 综合成一个 [0,1] 的“撞墙程度”
        collision_level = (avg_force_norm * 0.5 + max_force_norm * 0.5)
        # 变成一个“力因素”：1 表示完全正常，0 表示非常差
        force_factor = 1.0 - collision_level
    else:
        # 没有力信息，就不加惩罚
        force_factor = 1.0

    # ========= 综合得分 =========
    # 基础分：看新鲜度 + 完整度
    base_score = freshness * 0.5 + completeness * 0.5
    # 再乘上力因素（撞得多 → force_factor 小 → 总分下降）
    score = round(base_score * force_factor, 2)

    # ========= 文本说明 =========
    if score > 0.8:
        comment = "记忆状态良好，行为稳定。"
    elif score > 0.5:
        comment = "记忆一般，存在一定风险，建议观察是否有异常受力。"
    else:
        comment = "记忆质量较差，可能存在频繁碰撞或异常行为，建议检查策略或环境。"

    return {
        "score": score,
        "freshness": round(freshness, 2),
        "completeness": round(completeness, 2),
        "force_factor": round(force_factor, 2),
        "comment": comment
    }
