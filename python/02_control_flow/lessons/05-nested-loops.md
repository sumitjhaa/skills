# 🎯 Nested Loops
<!-- ⏱️ 8 min read | 🟡 Medium | 🧠 Applied -->

**What You'll Learn:** Combine loops inside loops to work with 2D data, create patterns, and generate grids.

> 💡 **TL;DR — The whole point:** A loop inside another loop — the inner loop runs completely for each iteration of the outer loop; total iterations = outer × inner.

## 🔗 Why This Matters
Loop control (Lesson 04) helps you manage single loops. But real problems often have layers — like a Squid Game tournament bracket (rounds × matches), a multiplication table (rows × columns), or a sports league schedule (teams × opponents). Nested loops handle multi-dimensional repetition.

## The Concept

A nested loop is a loop inside another loop. The **outer loop** represents rows or rounds; the **inner loop** represents columns or matches per round. For each iteration of the outer loop, the inner loop runs completely through.

The total iterations is `outer_count × inner_count`. A 3×4 grid runs the inner body 12 times. Tracing nested loops on paper helps — write the outer variable, then run through all inner values for each outer value.

## Code Example

```python
"""Squid Game — tournament brackets and game board"""

# Tournament bracket — rounds × matches per round
print("=== Squid Game Tournament Bracket ===")
players = ["Gi-hun", "Sang-woo", "Ali", "Sae-byeok", "Il-nam", "Mi-nyeo", "Jun-ho", "Deok-su"]
round_num = 1
while len(players) > 1:
    print(f"\nRound {round_num}:")
    winners = []
    for i in range(0, len(players) - 1, 2):
        print(f"  Match: {players[i]} vs {players[i+1]}")
        winners.append(players[i])  # first player always wins for demo
    players = winners
    round_num += 1
print(f"\nChampion: {players[0]}")

# Grid pattern — 3 rows × 4 columns of player markers
print("\n=== Game Board (3×4 Grid) ===")
for row in range(3):
    for col in range(4):
        print(f"  [{row},{col}]", end="")
    print()

# Multiplication table style — score combinations
print("\n=== Score Multiplier Table ===")
for base_score in [100, 200, 300]:
    for multiplier in [1, 2, 3]:
        print(f"  {base_score} × {multiplier} = {base_score * multiplier}")
    print()
```

## 🔍 How It Works

- Outer `while` loop runs rounds until one player remains
- Inner `for` loop processes matches within each round: `range(0, len(players) - 1, 2)` steps by 2 for pairings
- The grid: outer `row` loop (0, 1, 2) runs 3 times; for each row, inner `col` loop (0, 1, 2, 3) runs 4 times = 12 total prints
- After inner loop finishes, `print()` moves to the next line (no extra arguments = newline only)
- The score table: each base_score (3 values) gets paired with each multiplier (3 values) = 9 combinations

## ⚠️ Common Pitfall

Using the same loop variable name for both inner and outer loops (`for i in ...` nested in `for i in ...`). The inner loop overwrites the outer `i`, causing bugs after the inner loop ends. Use different names: `row`/`col`, `i`/`j`, `outer`/`inner`. Also, forgetting that the inner loop resets completely for each outer iteration.

## 🧠 Memory Aid

**"Nested loops are like a clock — the minute hand (outer) ticks once, while the second hand (inner) completes a full 60-second cycle."** For each minute (outer), seconds run 0-59 (inner complete run).

## 🏃 Try It

Run the code file:
```bash
python code/02-05-nested-loops.py
```
Then modify the grid to print a 5×5 checkerboard pattern alternating `[X]` and `[O]`.

## 🔗 Related

- [For Loops](02-for-loops.md) — the loops that go inside each other
- [Loop Control](04-loop-control.md) — break/continue apply to the innermost loop only

## ➡️ Next

→ [06 — Match/Case](06-match-case.md)
