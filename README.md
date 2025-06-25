<div align="center">
  <h1>Zhed Solver</h1>

  <p>
    <strong>Heuristic solver for Zhed puzzle game</strong>
  </p>
</div>

## About

## Installation

Install using [uv](https://docs.astral.sh/uv)

```bash
uv sync
```

## Usage

All levels are encoded in [levels.yaml](./src/zhed/data//levels.yaml) and can be visualized with the `zhed view` command.

```bash
zhed view 64
```

```txt
╭───────────────────────╮
│ Level 64              │
├───────────────────────┤
│ □ □ □ □ □ □ □ □ □ □ □ │
│ □ □ □ □ 1 □ □ 2 □ □ □ │
│ □ □ 2 □ □ □ □ □ □ □ □ │
│ □ □ □ □ □ 1 □ □ □ □ □ │
│ □ □ □ □ □ □ □ 1 □ ◎ □ │
│ □ □ □ 2 □ □ □ □ □ □ □ │
│ □ □ □ 1 □ □ □ □ □ □ □ │
│ □ 1 2 3 □ □ □ □ 1 1 □ │
│ □ □ □ 1 □ □ 2 □ □ □ □ │
│ □ □ □ □ 2 3 □ □ □ □ □ │
│ □ □ □ □ □ □ □ □ □ □ □ │
╰───────────────────────╯
```

A backtracking solver is implemented and can be run with the `zhed solve` command.

```bash
zhed solve 10
```

```txt
Level 10 solved in 0.70 seconds.
Solution:
- (2, 4) -> L
- (1, 3) -> D
- (4, 2) -> R
- (2, 5) -> D
- (5, 5) -> D
```

## Related work

- [Optimizing Solvers for NP-Complete Zhed Puzzles](https://ir.library.oregonstate.edu/concern/parent/pz50h5011/file_sets/xk81jt90z)
- [Zhed is NP-Complete](https://arxiv.org/pdf/2112.07914)
- [glguy/5puzzle](https://github.com/glguy/5puzzle)
- [MOAAS/ZhedAI](https://github.com/MOAAS/ZhedAI)
