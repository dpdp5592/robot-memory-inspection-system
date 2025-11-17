# file: plot_abnormal_example.py
"""
画出异常策略（乱走策略）的轨迹和力传感器情况。
"""

from abnormal_run import run_abnormal_episode
import matplotlib.pyplot as plt


def plot_trajectory_and_force(traj, force_log, save_path="bad_episode.png"):
    steps = list(range(len(traj)))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6), sharex=True)

    ax1.plot(steps, traj, marker="o")
    ax1.set_ylabel("Position")
    ax1.set_title("Abnormal Policy Trajectory")

    ax2.plot(range(len(force_log)), force_log, marker="x")
    ax2.set_xlabel("Step")
    ax2.set_ylabel("Force")
    ax2.set_title("Abnormal Policy Force")

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"图像已保存到：{save_path}")


if __name__ == "__main__":
    traj, sensors = run_abnormal_episode()
    force_log = sensors.get("force_log", [])
    print("轨迹：", traj)
    print("力传感器：", force_log)

    plot_trajectory_and_force(traj, force_log, "bad_episode.png")
