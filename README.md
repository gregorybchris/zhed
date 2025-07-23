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

| Level | Slow Solver | Fast Solver | Speedup  |
| ----- | ----------- | ----------- | -------- |
| 1     | 0.00007s    | 0.00002s    | 2.8x     |
| 2     | 0.00003s    | 0.00002s    | 1.3x     |
| 3     | 0.00031s    | 0.00005s    | 6.4x     |
| 4     | 0.00026s    | 0.00003s    | 8.3x     |
| 5     | 0.25156s    | 0.00006s    | 4203.7x  |
| 6     | 0.70209s    | 0.00020s    | 3514.1x  |
| 7     | 1.39966s    | 0.00021s    | 6656.0x  |
| 8     | 28.10545s   | 0.00052s    | 53631.8x |
| 9     | 2.10857s    | 0.00024s    | 8906.3x  |
| 10    | 7.54504s    | 0.00016s    | 47803.9x |
| 11    | timeout     | 0.00023s    |          |
| 12    | timeout     | 0.00415s    |          |
| 13    | timeout     | 0.29711s    |          |
| 14    | timeout     | 0.00175s    |          |
| 15    | timeout     | 27.48294s   |          |
| 16    | timeout     | 0.00045s    |          |
| 17    | timeout     | 0.00072s    |          |
| 18    | timeout     | 0.04178s    |          |
| 19    | timeout     | 0.01315s    |          |
| 20    | timeout     | 1.16194s    |          |

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
