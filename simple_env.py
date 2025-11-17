# file: simple_env.py
"""
一个非常简单的“虚拟机器人环境”：
- 机器人在一条线上，从 start 走到 goal
- 每一步可以往前走（+1）或不动（0）
- 如果撞到边界，就算是“受力很大”（force=1.0）
- 否则就是轻微接触（force=0.1）
"""

import random


class SimpleRobotEnv:
    def __init__(self, start=0, goal=10, max_steps=20):
        self.start = start
        self.goal = goal
        self.max_steps = max_steps
        self.reset()

    def reset(self):
        """重置环境，回到起点"""
        self.pos = self.start
        self.step_count = 0
        return self.pos

    def step(self, action: int):
        """
        执行一步动作：
        action:
          -1: 向左
           0: 不动
          +1: 向右
        返回：新位置、是否结束、传感器信息
        """
        self.step_count += 1
        old_pos = self.pos

        # 更新位置
        self.pos += action

        # 碰到边界就“撞墙”
        hit_wall = False
        if self.pos < 0:
            self.pos = 0
            hit_wall = True
        elif self.pos > self.goal:
            self.pos = self.goal
            hit_wall = True

        # 是否结束：到达终点 或 走太多步
        done = (self.pos == self.goal) or (self.step_count >= self.max_steps)

        # 假装有一个“力传感器”：撞墙时力大，否则力小
        force = 1.0 if hit_wall else 0.1

        info = {
            "force": force,
            "old_pos": old_pos,
            "new_pos": self.pos,
            "step": self.step_count
        }
        return self.pos, done, info


def run_episode():
    """
    运行一整次“任务”：
    - 从起点走到终点
    - 记录每一步的位置（轨迹）和每一步的受力（力传感器）
    返回：
      trajectory: [pos0, pos1, pos2, ...]
      sensors: {"force_log": [...力数值...]}
    """
    env = SimpleRobotEnv()
    traj = []
    force_log = []

    state = env.reset()
    traj.append(state)
    done = False

    while not done:
        # 简单策略：如果没到终点，就一直往右走（+1）
        if env.pos < env.goal:
            action = 1
        else:
            action = 0

        state, done, info = env.step(action)
        traj.append(state)
        force_log.append(info["force"])

    sensors = {"force_log": force_log}
    return traj, sensors


# 直接运行这个文件时，做一个小测试
if __name__ == "__main__":
    t, s = run_episode()
    print("轨迹：", t)
    print("力传感器：", s)
