# Advanced Go & Interview Prep

Comprehensive preparation for senior Go interviews — runtime internals, system design, DSA patterns, and design patterns.

## Structure

| Category | Directory | What's Inside |
|----------|-----------|--------------|
| **Go Internals** | [`go-internals/`](./go-internals) | Slices, maps, memory allocator, GMP scheduler, channels, GC, defer/panic/recover, `sync.Pool` |
| **System Design** | [`system-design/`](./system-design) | HLD MCQs — Rate Limiter, Consistent Hashing, Key-Value Store, URL Shortener, YouTube, Chat, News Feed, etc. |
| **DSA Patterns** | [`dsa/`](./dsa) | 22 algorithm patterns with MCQs and Go solutions — Two Pointers, DP, BFS/DFS, Graphs, Trees, Backtracking, etc. |
| **Design Patterns** | [`design-patterns/`](./design-patterns) | All 23 GoF patterns in Python with real-world examples |

## Go Internals Topics

| Topic | Dir |
|-------|-----|
| Slice internals | `go-internals/slicesgo/` |
| Map internals | `go-internals/mapsgo/` |
| Memory allocation & escape analysis | `go-internals/memoryallocation/` |
| GMP Scheduler | `go-internals/goscheduler(GMP Model)/` |
| Channel internals | `go-internals/channel-internals/` |
| Garbage Collection | `go-internals/garbage_collection_mechanidm/` |
| `sync.Pool` GC bypass | `go-internals/bypassing_gc/` |
| Defer/Panic/Recover | `go-internals/defer_panic_recover_internal/` |

## Run

```bash
# Go internals — each is a standalone main package
go run ./go-internals/slicesgo
go run ./go-internals/mapsgo

# DSA solutions — run tests
go test ./dsa/...
```

## Repo

Previously `advanced-go-internals`, restructured into topic categories for interview preparation.
