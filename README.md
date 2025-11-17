# Robot Memory Inspection System (RMIS)

这是一个面向“机器人记忆年检”的小项目，用来演示：

- 怎么给机器人（或智能体）设计“记忆”结构
- 怎么检查一条记忆是否存在（missing / ok）
- 怎么给记忆打一个“健康分”（Memory Health Score）
- 怎么用 Python 写一个简单的诊断脚本，并在命令行运行

目前项目结构很简单，适合作为入门示例，也可以作为简历中的算法/系统设计项目展示。

---

## 功能概览

- `episodic_memory.py`  
  - 存储和读取“事件记忆”（Episodic Memory），包括：
    - 轨迹信息（trajectory）
    - 传感器信息（sensors）
    - 时间戳（timestamp）

- `memory_health_score.py`  
  - 根据记忆内容，计算一个简单的“记忆健康度”：
    - freshness（新鲜度）
    - completeness（完整度）
    - 一个 0–1 的总评分（score）
    - 一句文字说明（comment）

- `diagnose.py`  
  - 先检查记忆是否存在
  - 再调用记忆健康度模块，对记忆进行打分
  - 打印出结构化的诊断结果（包含 JSON 样式的输出）

---

## 如何运行

1. 确保已经安装 Python 3（Windows / Mac 均可）
2. 将仓库代码下载到本地（可以用网页下载 ZIP）
3. 打开命令行（Windows 可用 cmd），进入项目目录，例如：

   ```bash
   cd Desktop\rmis-project


