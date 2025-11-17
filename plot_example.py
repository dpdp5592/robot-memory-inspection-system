# file: plot_example.py
"""
从虚拟机器人环境收集一条轨迹和力传感器数据，
画出轨迹和力随时间变化的图，并保存为 PNG 图片。
"""

from simple_env import run_episode
import matplotlib.pyplot as plt


def plot_trajectory_and_force(traj, force_log, save_path="episode_plot.png"):
    steps = list(range(len(traj)))

    # 创建一个图，有两个子图：上面轨迹，下面力
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6), sharex=True)

    # 轨迹
    ax1.plot(steps, traj, marker="o")
    ax1.set_ylabel("Position")
    ax1.set_title("Robot Trajectory")

    # 力传感器
    ax2.plot(range(len(force_log)), force_log, marker="x")
    ax2.set_xlabel("Step")
    ax2.set_ylabel("Force")
    ax2.set_title("Force Sensor")

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"图像已保存到：{save_path}")


if __name__ == "__main__":
    traj, sensors = run_episode()
    force_log = sensors.get("force_log", [])
    print("轨迹：", traj)
    print("力传感器：", force_log)

    plot_trajectory_and_force(traj, force_log, "good_episode.png")
