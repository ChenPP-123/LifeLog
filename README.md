# LifeLog

LifeLog 是一个基于 Python 的终端任务和生活日志管理工具。它不依赖数据库，所有数据都保存在项目根目录的 `data.json` 中，适合在命令行中快速记录和查看。

## 功能

- 创建、查看、完成、重命名和删除任务
- 创建和查看生活日志
- 首次运行时自动创建本地数据文件

## 环境要求

- Python 3.10 或更高版本

## 安装

建议在虚拟环境中安装依赖：

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install -r requirements.txt
```

## 使用

所有命令都通过 `main.py` 执行：

```bash
python main.py <command> [arguments]
```

### 任务命令

| 命令 | 作用 |
| --- | --- |
| `at <title>` | 添加任务 |
| `lt` | 查看任务列表 |
| `mt <index>` | 切换任务的完成状态 |
| `rt <index> <new_title>` | 重命名任务 |
| `dt <index>` | 删除任务 |

示例：

```bash
python main.py at "Write tests"
python main.py lt
python main.py mt 1
python main.py rt 1 "Write better tests"
python main.py dt 1
```

任务编号从 `1` 开始。任务列表中，`[ ]` 表示未完成，`[*]` 表示已完成。

### 日志命令

| 命令 | 作用 |
| --- | --- |
| `al <content>` | 添加日志 |
| `sl` | 查看日志列表 |

示例：

```bash
python main.py al "Finished the first milestone."
python main.py sl
```

日志会记录创建时间，并按以下格式显示：

```text
YYYY-MM-DD HH:MM:SS:
    content
```

任务编号不存在或输入为空时，程序会输出对应的错误信息。

## 数据文件

默认数据文件是项目根目录下的 `data.json`。文件不存在或为空时，LifeLog 会初始化为：

```json
{
    "tasks": [],
    "logs": []
}
```

## 开发

运行测试：

```bash
pytest
```

运行代码格式化和检查：

```bash
ruff format .
ruff check .
```

## 项目结构

```text
.
├── lifelog/
│   ├── cli.py       # 命令分发和终端输出
│   ├── log.py       # 日志模型
│   ├── manager.py   # 任务和日志业务逻辑
│   ├── storage.py   # data.json 读写
│   └── task.py      # 任务模型
├── tests/           # 自动化测试
├── data.json        # 本地数据文件
├── main.py          # 程序入口
├── pyproject.toml   # 项目和工具配置
└── requirements.txt # 依赖列表
```
