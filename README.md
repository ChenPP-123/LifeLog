# LifeLog

LifeLog 是一个基于 Python 的终端任务与日志管理工具。

它目前提供两类能力：

- 任务管理
- 日志记录

所有数据都保存在本地 `data.json` 文件中，适合直接在命令行里快速使用。

## 功能

### Task

- 新增任务
- 查看任务列表
- 标记任务完成 / 未完成
- 重命名任务
- 删除任务

### Log

- 新增日志
- 查看日志列表

## 安装

```bash
pip install -r requirements.txt
```

## 运行

项目入口是 `main.py`：

```bash
python main.py <command> [args]
```

第一次运行时，如果 `data.json` 不存在，程序会自动创建一个默认文件。

## 命令说明

### 任务

- `at <title>`: 新增任务
- `lt`: 查看任务列表
- `mt <index>`: 切换第 `index` 个任务的完成状态
- `rt <index> <new_title>`: 重命名第 `index` 个任务
- `dt <index>`: 删除第 `index` 个任务

示例：

```bash
python main.py at "Write tests"
python main.py lt
python main.py mt 1
python main.py rt 1 "Write better tests"
python main.py dt 1
```

### 日志

- `al <content>`: 新增日志
- `sl`: 查看日志列表

示例：

```bash
python main.py al "Finished the first milestone."
python main.py sl
```

## 输出格式

- 任务列表会按编号输出。
- 未完成任务显示为 `[ ]`。
- 已完成任务显示为 `[*]`。
- 日志会按时间输出，格式为：

```text
YYYY-MM-DD HH:MM:SS:
    content
```

## 数据存储

默认数据文件为项目根目录下的 `data.json`。

结构如下：

```json
{
    "tasks": [],
    "logs": []
}
```

## 测试

```bash
python -m pytest
```

测试覆盖了以下内容：

- `Task` 和 `Log` 的数据转换
- `Storage` 的读写行为
- `TaskManager` 和 `LogManager` 的业务流程
- `Cli` 的命令分发和输出格式

## 项目结构

```text
lifelog/
main.py
tests/
```
