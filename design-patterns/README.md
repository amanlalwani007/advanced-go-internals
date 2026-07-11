# Design Patterns in Python

All 23 Gang of Four (GoF) design patterns implemented in Python with **practical, real-world examples**.

## Structure

```
design-patterns-python/
├── interview_important/  # ★ 12 patterns most asked in interviews
│   ├── singleton.py            App config manager (thread-safe)
│   ├── factory_method.py       Logistics delivery system
│   ├── abstract_factory.py     Cross-platform UI toolkit
│   ├── builder.py              SQL query builder
│   ├── adapter.py              Payment gateway unification
│   ├── decorator.py            HTTP middleware pipeline
│   ├── proxy.py                Lazy-loading image proxy
│   ├── observer.py             Stock market notifications
│   ├── strategy.py             File compression (Zip/Tar/Gzip)
│   ├── command.py              Text editor undo/redo
│   ├── chain_of_responsibility.py  Support ticket escalation
│   └── state.py                Vending machine states
├── creational/          # 1 remaining pattern
│   ├── prototype.py            Document template cloning
├── structural/          # 4 remaining patterns
│   ├── bridge.py               Remote control × device matrix
│   ├── composite.py            File system explorer
│   ├── facade.py               Home theater orchestration
│   └── flyweight.py            Text editor character styles
├── behavioral/          # 6 remaining patterns
│   ├── interpreter.py          Math expression parser
│   ├── iterator.py             Paginated API client
│   ├── mediator.py             Air traffic control
│   ├── memento.py              Document snapshot rollback
│   ├── template_method.py      Data mining framework
│   └── visitor.py              Code analysis (linting, complexity)
└── main.py              # Run all 23 examples
```

## Usage

```bash
# Run a single interview-important pattern
python interview_important/singleton.py

# Run all patterns
python main.py
```

## Patterns by Category

| Category | Count | Patterns |
|---|---|---|
| **★ Interview Important** | **12** | Singleton, Factory Method, Abstract Factory, Builder, Adapter, Decorator, Proxy, Observer, Strategy, Command, Chain of Responsibility, State |
| **Creational** | 1 | Prototype |
| **Structural** | 4 | Bridge, Composite, Facade, Flyweight |
| **Behavioral** | 6 | Interpreter, Iterator, Mediator, Memento, Template Method, Visitor |

## Requirements

- Python 3.10+

No third-party packages required.
