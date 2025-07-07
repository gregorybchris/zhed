<div align="center">
  <h1>Zhed Solver</h1>

  <p>
    <strong>Solver for Zhed puzzle game</strong>
  </p>
</div>

## About

This repo contains a solver for the [Zhed puzzle game](https://play.google.com/store/apps/details?id=com.groundcontrol.zhed) as well as all levels from the game encoded in [levels.yaml](./src/zhed/data//levels.yaml)

## Installation

Install using [uv](https://docs.astral.sh/uv)

```bash
uv sync
```

## Usage

### `zhed view`

Visualize levels in the terminal.

```bash
zhed view 64
```

```hs
╭-----------------------╮
│ Level 64              │
├-----------------------┤
│ . . . . . . . . . . . │
│ . . . . 1 . . 2 . . . │
│ . . 2 . . . . . . . . │
│ . . . . . 1 . . . . . │
│ . . . . . . . 1 . ◎ . │
│ . . . 2 . . . . . . . │
│ . . . 1 . . . . . . . │
│ . 1 2 3 . . . . 1 1 . │
│ . . . 1 . . 2 . . . . │
│ . . . . 2 3 . . . . . │
│ . . . . . . . . . . . │
╰-----------------------╯
```

### `zhed solve`

Run a backtracking solver on a specific level or all levels

```bash
zhed solve
zhed solve 10
```

```txt
Level 10 solved in 0.70 seconds.
- (2, 4) -> L
- (1, 3) -> D
- (4, 2) -> R
- (2, 5) -> D
- (5, 5) -> D
```

### `zhed play`

Play a level in the terminal

```bash
zhed play 10
```

Controls:

```txt
• ↑/↓/←/→  |  move cursor
• w/a/s/d  |  make move
• z/u      |  undo move
• r        |  reset board
• 1-9      |  set number tile
• g        |  set goal tile
• e        |  set empty tile
• b        |  set blank tile
• q        |  quit
```

### `zhed check`

Check if a solution is already known for a given level.

```bash
zhed check 10
```

## Related work

- [Optimizing Solvers for NP-Complete Zhed Puzzles](https://ir.library.oregonstate.edu/concern/parent/pz50h5011/file_sets/xk81jt90z)
- [Zhed is NP-Complete](https://arxiv.org/pdf/2112.07914)
- [glguy/5puzzle](https://github.com/glguy/5puzzle)
- [MOAAS/ZhedAI](https://github.com/MOAAS/ZhedAI)
- [mikkelschmidt14/ZhedSolver](https://github.com/mikkelschmidt14/ZhedSolver)
