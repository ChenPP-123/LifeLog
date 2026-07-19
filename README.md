# LifeLog

LifeLog 是一个基于 Python 的终端任务和生活日志管理工具。它使用 SQLite 在本地保存数据，适合在命令行中快速记录和查看。

## 功能

- 创建、查看、完成、重命名和删除任务
- 创建和查看生活日志
- 首次运行时自动创建本地 SQLite 数据库

## 环境要求

- Python 3.13 或更高版本

## 安装

建议在虚拟环境中安装 LifeLog：

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install .
```

## 使用

安装后，使用 `lifelog` 命令：

```bash
lifelog <command> [arguments]
```

在源码目录中，也可以不安装，直接运行：

```bash
python -m lifelog <command> [arguments]
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
lifelog at "Write tests"
lifelog lt
lifelog mt 1
lifelog rt 1 "Write better tests"
lifelog dt 1
```

任务编号从 `1` 开始。任务列表中，`[ ]` 表示未完成，`[*]` 表示已完成。

### 日志命令

| 命令 | 作用 |
| --- | --- |
| `al <content>` | 添加日志 |
| `sl` | 查看日志列表 |

示例：

```bash
lifelog al "Finished the first milestone."
lifelog sl
```

日志会记录创建时间，并按以下格式显示：

```text
YYYY-MM-DD HH:MM:SS:
    content
```

任务编号不存在或输入为空时，程序会输出对应的错误信息。

## 数据库

默认数据库文件名为 `lifelog.db`，其位置由 `lifelog.config.DATABASE_FILE` 配置。首次运行时会自动创建任务和日志数据表。

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
│   ├── config.py    # 项目路径和数据库配置
│   ├── exceptions.py # 自定义异常
│   ├── log.py       # 日志模型
│   ├── manager.py   # 任务和日志业务逻辑
│   ├── sqlite.py    # SQLite 读写
│   ├── __main__.py  # 命令行入口
│   └── task.py      # 任务模型
├── tests/           # 自动化测试
├── lifelog.db       # 本地 SQLite 数据库
├── pyproject.toml   # 项目和工具配置
└── requirements.txt # 依赖列表
```
