<div align="center">
  <h1>Zhed Solver</h1>

  <p>
    <strong>Solver for Zhed puzzle game</strong>
  </p>
</div>

## About

This repo contains:

- [All 100 levels](./src/zhed/data//levels.yaml) from the [Zhed puzzle game](https://play.google.com/store/apps/details?id=com.groundcontrol.zhed) encoded as YAML
- [Solutions](./src/zhed/data/solutions.yaml) for all levels
- A playable terminal-based version of the game
- A fast solver

> Unlike many Zhed solvers available online, this solver does not use a brute-force backtracking search. Instead, it starts at the goal tile and determines which moves unblock a path to the goal tile. See [solver.py](./src/zhed/solver.py) for my implementation.

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
│ • • • • • • • • • • • │
│ • • • • 1 • • 2 • • • │
│ • • 2 • • • • • • • • │
│ • • • • • 1 • • • • • │
│ • • • • • • • 1 • ◎ • │
│ • • • 2 • • • • • • • │
│ • • • 1 • • • • • • • │
│ • 1 2 3 • • • • 1 1 • │
│ • • • 1 • • 2 • • • • │
│ • • • • 2 3 • • • • • │
│ • • • • • • • • • • • │
╰-----------------------╯
```

### `zhed solve`

Run the solver on a specific level or all levels.

```bash
zhed solve
zhed solve 10
```

```rs
Level 10 solved in 0.70 seconds
- (2, 4) -> L
- (1, 3) -> D
- (4, 2) -> R
- (2, 5) -> D
- (5, 5) -> D
```

### `zhed play`

Play a level in the terminal.

```bash
zhed play 10
```

Controls:

| Key     | Action          |
| ------- | --------------- |
| ↑/↓/←/→ | move cursor     |
| w/a/s/d | make move       |
| z/u     | undo move       |
| r       | reset board     |
| 1-9     | set number tile |
| g       | set goal tile   |
| e       | set empty tile  |
| b       | set blank tile  |
| q       | quit            |

### `zhed check`

Verify a known solution by simulating moves and checking that the goal tile is reached.

```bash
zhed check 10
```

### `zhed benchmark`

Run a benchmark comparing the brute-force solver with the fast solver.

```bash
zhed benchmark
```

## Benchmark

I ran a benchmark to compare the brute-force naïve implementation vs the fast solver that starts at the goal tile and works backwards. The fast solver is significantly faster.

| Level | Slow Solver (s) | Fast Solver (s) | Speedup  |
| ----- | --------------- | --------------- | -------- |
| 1     | 0.000067        | 0.000023        | 2.9x     |
| 2     | 0.000027        | 0.000021        | 1.3x     |
| 3     | 0.000324        | 0.000043        | 7.5x     |
| 4     | 0.000408        | 0.000031        | 13.2x    |
| 5     | 0.416128        | 0.000063        | 6586.3x  |
| 6     | 0.961619        | 0.000185        | 5197.6x  |
| 7     | 1.568207        | 0.000252        | 6228.7x  |
| 8     | 25.998828       | 0.000515        | 50484.7x |
| 9     | 1.783234        | 0.000310        | 5749.0x  |
| 10    | 8.010899        | 0.000183        | 43750.2x |
| 11    | timeout         | 0.000217        |          |
| 12    | 47.648170       | 0.004340        | 10979.0x |
| 13    | timeout         | 0.306370        |          |
| 14    | timeout         | 0.001722        |          |
| 15    | timeout         | 26.575541       |          |
| 16    | timeout         | 0.000440        |          |
| 17    | timeout         | 0.000731        |          |
| 18    | timeout         | 0.004900        |          |
| 19    | timeout         | 0.111927        |          |
| 20    | timeout         | 0.965020        |          |
| 21    | timeout         | 0.731862        |          |
| 22    | timeout         | 13.139491       |          |
| 23    | timeout         | 7.105371        |          |
| 24    | timeout         | 0.329705        |          |
| 25    | timeout         | 0.429798        |          |
| 26    | timeout         | 46.792121       |          |
| 27    | timeout         | 9.776571        |          |
| 28    | timeout         | 1.459381        |          |
| 29    | timeout         | timeout         |          |
| 30    | timeout         | 0.003995        |          |

## Related work

- [Optimizing Solvers for NP-Complete Zhed Puzzles](https://ir.library.oregonstate.edu/concern/parent/pz50h5011/file_sets/xk81jt90z)
- [Zhed is NP-Complete](https://arxiv.org/pdf/2112.07914)
- [glguy/5puzzle](https://github.com/glguy/5puzzle)
- [MOAAS/ZhedAI](https://github.com/MOAAS/ZhedAI)
- [mikkelschmidt14/ZhedSolver](https://github.com/mikkelschmidt14/ZhedSolver)

## Notes

In older versions of the app, level 75 is slightly different (note the addition of an extra 1 tile in the upper right of the board). This small change does not significantly affect how the level is played.

```txt
Used in this repo:
• • • • • • • • • • • • • •
• 2 • 2 • 1 • • • • • • • •
• • 1 • 2 • • • • 1 • • • •
• • • • • • • • • • 1 • • •
3 • • • • • • • • • • • • •
• • • • • • 2 1 1 • • • • •
• • • • • • 1 2 1 • • 1 • •
• • • • • • 1 1 2 • • • 1 •
• • • 1 • • • • • • • • • •
• • • 1 • • • • • 1 1 • • •
• • • • 1 • • • • 1 1 • • •
• • 1 • • • • • • • • @ • 1
• • • • • • • • • • • • • •
• • • • • • • • • • • • • •

Seen elsewhere:
• • • • • • • • • • • • • •
• 2 • 2 • 1 • • • • • • • •
• • 1 • 2 • • • • 1 • • • •
• • • • • • • • • • • 1 • •
3 • • • • • • • • • 1 • • •
• • • • • • 2 1 1 • • • • •
• • • • • • 1 2 1 • • 1 • •
• • • • • • 1 1 2 • • • 1 •
• • • 1 • • • • • • • • • •
• • • 1 • • • • • 1 1 • • •
• • • • 1 • • • • 1 1 • • •
• • 1 • • • • • • • • @ • 1
• • • • • • • • • • • • • •
• • • • • • • • • • • • • •
```
