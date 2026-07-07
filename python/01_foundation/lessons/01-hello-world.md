# 🎯 Hello World & Comments
<!-- ⏱️ 5 min read | 🟢 Easy | 🧠 Core -->

**What You'll Learn:** Write your first Python program using `print()`, and document code with comments and docstrings.

> 💡 **TL;DR — The whole point:** `print()` outputs text to the screen; comments (`#`) and docstrings (`""" """`) are ignored by Python and exist only for humans reading your code.

## 🔗 Why This Matters
This is the ceremonial first step every programmer takes. Once you can print output and leave notes for yourself, you can start experimenting with code and actually seeing what it does. Every program you'll ever write will use `print()` for debugging and results.

## The Concept

Think of `print()` as the Matrix's "construct loading" message — it's how the program communicates with the outside world. You pass what you want to display inside parentheses, and Python sends it to the terminal.

Comments (`#`) are like Morpheus leaving notes in the code for Neo. They're invisible to the machine but invaluable to humans reading your code. Docstrings (`""" """`) are multi-line comments at the top of files or functions that explain what the code does — Python remembers them as documentation.

## Code Example

```python
"""Neo's first message to the Matrix"""

# This is a single-line comment — Python ignores this
print("Wake up, Neo...")  # inline comment too

"""
This is a docstring.
Python stores this as documentation.
It can span multiple lines.
"""
print("The Matrix has you.")
```

## 🔍 How It Works

- `"""Neo's first message..."""` — docstring at the top describes the file's purpose
- `# This is a single-line comment` — completely ignored by Python; for the reader
- `print("Wake up, Neo...")` — calls the `print()` function, passing a string argument
- `# inline comment too` — a comment after some code, explaining that specific line
- `"""This is a docstring..."""` — another docstring, this time in the middle of the file
- Docstrings are accessible via `help()` and documentation tools — comments are not

## ⚠️ Common Pitfall

Forgetting quotes around your string: `print(Hello)` will crash with a `NameError`. Always wrap text in `" "` or `' '` — Python thinks unquoted words are variable names. Also, don't confuse `#` comments with `""" """` docstrings — use comments for inline explanations, docstrings for file/function documentation.

## 🧠 Memory Aid

**"Print needs parentheses, strings need quotes — the two P's of output."** Think of `print()` as a cannon that fires whatever you load into it. Load a string (`"Hello"`) and it fires text. Forget quotes and the cannon jams.

## 🏃 Try It

Run the code file:
```bash
python code/01-01-hello-world.py
```
Then edit the string to print your own name. Try adding a second `print()` call.

## 🔗 Related

- [String Formatting](06-string-formatting.md) — printing more complex output with f-strings

## ➡️ Next

→ [02 — Variables & Dynamic Typing](02-variables.md)
