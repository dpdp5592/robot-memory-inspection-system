# file: diagnose.py

# file: diagnose.py

import json
from episodic_memory import EpisodicMemory
from memory_health_score import compute_memory_health


def save_report_to_file(report: dict, filename: str):
    """把诊断结果保存为一个 JSON 文件。"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=4)
    print(f"\n诊断报告已保存到文件：{filename}")

def simple_diagnose(memory: EpisodicMemory, key: str):
    data = memory.get(key)

    # 先根据有没有记忆，给出基本结论
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

    # 再调用“记忆健康度”模块，给一个分数
    health = compute_memory_health(data)
    report["memory_health"] = health  # 把健康度信息塞到报告里

    print("诊断结果：")
    print(json.dumps(report, ensure_ascii=False, indent=4))
    return report



if __name__ == "__main__":
    mem = EpisodicMemory()

    print("【第一次年检】什么记忆都没有：")
    simple_diagnose(mem, "demo_traj")

    print("\n现在往记忆里加一条记录……\n")
    fake_traj = [0, 1, 2, 3]
    fake_sensors = {"force": 0.1}
    mem.add("demo_traj", fake_traj, fake_sensors)

    print("【第二次年检】已经有记忆了：")
    report = simple_diagnose(mem, "demo_traj")

    # 把第二次年检的结果保存成一个 JSON 文件
    save_report_to_file(report, "diagnose_report.json")
