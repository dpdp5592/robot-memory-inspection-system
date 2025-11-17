# file: abnormal_run.py
"""
对比：正常策略 vs 乱走策略 的记忆健康度。
"""

from episodic_memory import EpisodicMemory
from memory_health_score import compute_memory_health
from simple_env import run_episode, SimpleRobotEnv


def run_abnormal_episode(max_steps=20):
    """
    运行一整次“异常任务”：
    - 机器人不再老老实实往右走，而是左右乱晃
    - 这样更容易撞到边界，force 会经常变成 1.0
    """
    env = SimpleRobotEnv(max_steps=max_steps)
    traj = []
    force_log = []

    state = env.reset()
    traj.append(state)
    done = False

    import random

    while not done:
        # 乱走策略：随机往左或往右
        action = random.choice([-1, 1])
        state, done, info = env.step(action)
        traj.append(state)
        force_log.append(info["force"])

    sensors = {"force_log": force_log}
    return traj, sensors


def build_memory_and_health(traj, sensors):
    """
    构建一条记忆，并计算健康度。
    """
    mem = EpisodicMemory()
    mem.add("episode", traj, sensors)
    item = mem.get("episode")
    health = compute_memory_health(item)
    return health


if __name__ == "__main__":
    # 1. 正常策略（run_episode）：一直往右走，尽量不撞墙
    good_traj, good_sensors = run_episode()
    good_health = build_memory_and_health(good_traj, good_sensors)

    print("=== 正常策略（good policy） ===")
    print("轨迹：", good_traj)
    print("力传感器：", good_sensors)
    print("健康度：", good_health)

    # 2. 异常策略（run_abnormal_episode）：左右乱走，更容易撞墙
    bad_traj, bad_sensors = run_abnormal_episode()
    bad_health = build_memory_and_health(bad_traj, bad_sensors)

    print("\n=== 异常策略（bad policy） ===")
    print("轨迹：", bad_traj)
    print("力传感器：", bad_sensors)
    print("健康度：", bad_health)

    print("\n对比结果：")
    print(f"正常策略 score = {good_health['score']}")
    print(f"异常策略 score = {bad_health['score']}")
