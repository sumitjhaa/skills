# 🎯 Input & Output
<!-- ⏱️ 7 min read | 🟢 Easy | 🧠 Core -->

**What You'll Learn:** Accept user input with `input()` and control `print()` output with `sep` and `end` parameters.

> 💡 **TL;DR — The whole point:** `input()` reads text from the user (always returns a string), `print()` outputs text; use `sep` to control spacing and `end` to control line endings.

## 🔗 Why This Matters
Variables and operators (Lessons 02-04) let you store and calculate, but your programs are still static. `input()` makes your programs interactive — like a quiz game that actually responds to the player's name and score. Without it, every run produces the same output.

## The Concept

`input()` reads a line of text from the user. It **always** returns a string — even if the user types a number. You can pass a prompt string as an argument to tell the user what to type.

`print()` is more flexible than it first appears. The `sep` parameter controls what goes between multiple arguments (default is a space). The `end` parameter controls what goes at the end (default is a newline). Combine them to create polished output.

Think of a quiz game: `input()` asks "What's your name?", stores the answer, then `print()` displays a personalized welcome message.

## Code Example

```python
"""Quiz game — player registration with input() and print()"""

print("=== QUIZ ARENA ===")
print("=" * 18)

# Get player info
player_name = input("Enter your name: ")
score = input("Enter your starting score: ")

# Welcome message with custom sep/end
print("\nWelcome", player_name, "!", sep="... ", end="\n\n")
print("Your journey begins with", score, "points.")

# Display leaderboard format using sep
print("\nCurrent Leaderboard:")
print("Rank", "Player", "Score", sep=" | ")
print("-" * 25)
print("1st", player_name, score, sep=" | ")
print("2nd", "Bot_Alpha", "850", sep=" | ")
print("3rd", "Bot_Beta", "720", sep=" | ")

# Progress bar using end
print("\nLoading", end="")
print(".", end="")
print(".", end="")
print(".", end="")
print(" Ready!")
```

## 🔍 How It Works

- `input("Enter your name: ")` — prints the prompt, waits for user input, returns whatever was typed as a string
- `player_name` — stores the returned string
- `print("\nWelcome", player_name, "!", sep="... ", end="\n\n")` — joins the three arguments with `"... "` instead of space, and ends with two newlines
- `sep=" | "` in the leaderboard — creates a table-like format with pipe separators
- `print(".", end="")` — prints a dot without a newline, so the next `print()` continues on the same line, creating a loading animation effect

## ⚠️ Common Pitfall

Forgetting that `input()` always returns a string. If you ask for a number and try to do math, you'll get a TypeError: `score + 50` fails if `score = "100"`. Always cast with `int()` or `float()` when you need numeric input. Also, `input()` can return an empty string if the user just presses Enter — check for that before using the value.

## 🧠 Memory Aid

**"input() goes in, print() goes out — like a conversation with your program."** Think of `input()` as the quiz host asking you a question, and `print()` as the host announcing your score to the audience.

## 🏃 Try It

Run the code file:
```bash
python code/01-05-input-output.py
```
Then modify the prompt to ask for the player's age and display it in the welcome message.

## 🔗 Related

- [String Formatting](06-string-formatting.md) — more powerful output control with f-strings
- [Type Casting](07-type-casting.md) — converting input strings to numbers for calculations

## ➡️ Next

→ [06 — String Formatting](06-string-formatting.md)
