# file: experiment_compare.py
"""
多次运行正常策略和异常策略，对比平均记忆健康度。
"""

from memory_health_score import compute_memory_health
from episodic_memory import EpisodicMemory
from simple_env import run_episode
from abnormal_run import run_abnormal_episode


def run_and_eval(run_func, episodes=20):
    scores = []
    for i in range(episodes):
        traj, sensors = run_func()
        mem = EpisodicMemory()
        mem.add(f"ep_{i}", traj, sensors)
        item = mem.get(f"ep_{i}")
        health = compute_memory_health(item)
        scores.append(health["score"])
    avg_score = sum(scores) / len(scores)
    return scores, avg_score


if __name__ == "__main__":
    print("=== 进行实验：正常策略 vs 异常策略 ===")

    good_scores, good_avg = run_and_eval(run_episode, episodes=20)
    print(f"正常策略 20 次，平均 score = {good_avg:.3f}")
    print("每次得分：", good_scores)

    bad_scores, bad_avg = run_and_eval(run_abnormal_episode, episodes=20)
    print(f"\n异常策略 20 次，平均 score = {bad_avg:.3f}")
    print("每次得分：", bad_scores)

    print("\n结论：")
    if good_avg > bad_avg:
        print("正常策略的平均记忆健康度明显高于异常策略，说明当前健康度设计有区分力。")
    else:
        print("目前健康度没有明显区分两种策略，建议调整打分规则。")
