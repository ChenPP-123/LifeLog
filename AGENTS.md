# AGENTS.md

This file defines how Codex should assist with the LifeLog project.

LifeLog is a learning project, not a feature factory. The main goal is to help
the user build engineering judgment while steadily improving a small Python
application.

## Project Purpose

LifeLog is a terminal task and log manager used to learn:

- Python project structure
- object-oriented design
- layered architecture
- dependency injection
- JSON persistence
- command-line application design
- pytest testing
- Git and GitHub workflow
- GitHub Actions CI
- AI-assisted development and code review

Prefer changes that make the project easier to understand, debug, test, and
extend. Do not optimize for novelty, cleverness, or the number of features.

## Current Stage

The project is currently a small Python CLI application with:

- task management
- log recording
- JSON storage in `data.json`
- pytest test coverage
- GitHub Actions running `python -m pytest`

The current architecture is:

```text
main.py
    -> Cli
    -> TaskManager / LogManager
    -> Storage
    -> data.json
```

Keep this structure clear unless the user explicitly starts a refactoring
sprint.

## Current Responsibilities

### `main.py`

`main.py` is the composition root.

It should:

- create `Storage`
- create `TaskManager` and `LogManager`
- inject managers into `Cli`
- define argparse commands and arguments
- parse arguments and call `cli.run(args)`

It should not contain business logic.

### `lifelog/cli.py`

`Cli` handles command dispatch and terminal output.

It should:

- map command names to handler methods
- call the appropriate manager method
- convert results into user-facing output

It should not read or write JSON directly. It should not own business rules that
belong in managers.

### `lifelog/manager.py`

Managers contain business workflows.

They should:

- load data from storage
- validate task indexes and business inputs
- update model objects
- save changed data
- return simple values that the CLI can display

Managers should not print output or open files directly.

### `lifelog/storage.py`

`Storage` owns JSON persistence.

It should:

- initialize missing or empty data files
- load JSON data
- deserialize dictionaries into model objects
- serialize model objects into JSON
- preserve the current data shape unless a migration task is explicit

Do not move business rules into storage.

### `lifelog/task.py` and `lifelog/log.py`

Models represent domain data and simple behavior.

They should:

- expose clear attributes
- convert to and from dictionaries
- contain behavior that naturally belongs to the model

They should not know about argparse, terminal output, files, or tests.

## Collaboration Role

The user is learning software development through this project.

Codex should:

- explain the current implementation before changing it when the task is new or
  non-trivial
- propose small, inspectable changes
- help define the goal of each sprint or task
- implement local code changes when asked to move the project forward
- add or update tests for behavior changes
- explain failing tests and debugging steps
- review the user's code with a focus on correctness, readability, and
  maintainability
- avoid taking over Git history unless explicitly asked

Codex should not:

- perform broad rewrites without a clear learning goal
- introduce new frameworks just because they are common
- hide complexity behind unnecessary abstractions
- change command names, output formats, or data formats without explicit
  approval
- silently expand the task scope
- treat passing tests as the only quality standard

## Engineering Values

Optimize decisions in this order:

1. Correctness
2. Readability
3. Simplicity
4. Maintainability
5. Performance

Every abstraction must reduce cognitive load. A little repetition is acceptable
when it keeps the code easier to follow.

Prefer:

- clarity over cleverness
- explicit data flow over hidden behavior
- small functions over dense functions
- simple tests over over-mocked tests
- local state over global state
- useful errors over silent failures

Avoid:

- premature extensibility
- deep dependency chains
- large all-at-once refactors
- unnecessary configuration
- design patterns without a concrete need
- abstractions that only remove duplicated text, not duplicated knowledge

## Standard Task Workflow

For each implementation task, follow this workflow:

1. Read the relevant source files and tests first.
2. State the current data flow or call chain if the change affects architecture.
3. Define the smallest reasonable change that satisfies the task.
4. Modify only the files needed for that change.
5. Add or update tests for new behavior or bug fixes.
6. Run `python -m pytest`.
7. Summarize what changed, what was tested, and any remaining risk.

For very small tasks, keep the explanation short, but still inspect the relevant
code before editing.

## Testing Rules

Run the full test suite after code changes:

```bash
python -m pytest
```

Use the existing testing style:

- model tests for `Task` and `Log`
- manager tests with `FakeStorage`
- storage tests with `tmp_path`
- CLI tests with stubs, `SimpleNamespace`, and `capsys`
- `monkeypatch` when time or environment needs to be controlled

New features should usually include:

- normal behavior tests
- boundary or invalid-input tests
- CLI dispatch/output tests when user-facing commands change
- storage compatibility tests when data format changes

Do not write tests that only mirror implementation details. Tests should verify
observable behavior.

## Data Compatibility

The current `data.json` shape is:

```json
{
    "tasks": [],
    "logs": []
}
```

Task objects currently serialize as:

```json
{
    "title": "Write tests",
    "completed": false
}
```

Log objects currently serialize as:

```json
{
    "time": "2026-07-12 18:30:00",
    "content": "Finished Sprint11"
}
```

Any change to persisted data must consider existing user data. Do not change the
storage format unless the task explicitly includes compatibility or migration.

## Current Commands

Keep these commands stable unless the user explicitly requests a CLI redesign:

- `at <title>`: add task
- `rt <index> <new_title>`: rename task
- `lt`: list tasks
- `mt <index>`: toggle task completion
- `dt <index>`: delete task
- `al <content>`: add log
- `sl`: show logs

## Code Review Standard

When reviewing code, prioritize findings over summaries.

Check:

- Does the code do what the task asked?
- Is the change in the right layer?
- Is data flow visible?
- Are invalid inputs handled clearly?
- Could existing `data.json` files break?
- Are tests checking behavior, not just implementation?
- Did the change introduce unnecessary concepts?
- Are names clear enough to reduce comments?
- Is any new dependency justified?
- Can the same result be achieved with less architecture?

If no issues are found, say that clearly and mention any residual testing gaps.

## Learning Roadmap

Guide future work in small sprints. Each sprint should have a concrete learning
goal, implementation goal, and verification standard.

### Stage 1: Make LifeLog a reliable CLI

Focus:

- input validation
- clearer error handling
- stronger tests
- cleaner README usage examples
- packaging as an installable CLI
- versioning and GitHub Releases

Goal:

Make a small command-line application that can be installed, run, tested, and
maintained reliably.

### Stage 2: Move from JSON to SQLite

Focus:

- basic SQL
- SQLite
- data modeling
- storage interfaces
- migration from JSON
- integration tests

Goal:

Understand why dependency injection and storage boundaries matter by supporting
more than one persistence implementation.

### Stage 3: Add an API

Focus:

- HTTP basics
- FastAPI
- request and response models
- API tests
- keeping CLI and API on the same business layer

Goal:

Learn how one core application can support multiple entry points:

```text
CLI -> Manager -> Storage
API -> Manager -> Storage
```

### Stage 4: Add a lightweight frontend

Focus:

- HTML
- CSS
- JavaScript
- browser requests to an API
- simple UI state

Goal:

Build a usable interface without introducing a frontend framework before it is
needed.

### Stage 5: Deployment and operations

Focus:

- Docker basics
- environment variables
- logs
- backups
- CI/CD
- deployment failure modes

Goal:

Understand what it takes for software to run outside the development machine.

## Teaching Style

When explaining code, prefer concrete project references over abstract theory.

Good explanations should answer:

- What problem does this code solve?
- Which layer owns this responsibility?
- What data enters and leaves this function?
- What would break if this changed?
- How do the tests prove the behavior?

Avoid long theory dumps unless the user asks for depth. Link concepts back to
the current codebase.

## Final Check Before Finishing Work

Before completing a task, ask:

- Can any concept be removed?
- Can any abstraction be eliminated?
- Can this become more obvious?
- Would a new engineer understand this quickly?
- Is every piece of complexity paying for itself?

The best solution is the one that solves today's problem while introducing the
fewest new ideas.
