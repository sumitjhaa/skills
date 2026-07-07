# 🎯 String Formatting
<!-- ⏱️ 8 min read | 🟡 Medium | 🧠 Core -->

**What You'll Learn:** Build formatted strings with f-strings, `.format()`, and escape sequences like `\n` and `\t`.

> 💡 **TL;DR — The whole point:** f-strings (`f"Hello {name}"`) embed variables directly into strings; use `\n` for newlines, `\t` for tabs, and raw strings `r"..."` to keep backslashes literal.

## 🔗 Why This Matters
You learned basic `print()` output (Lesson 05), but manually combining strings with `+` is clunky. String formatting is how real programs create polished output — music players show "Now Playing: Song by Artist", scoreboards format "Player: 1500 pts", and reports align columns perfectly.

## The Concept

**f-strings** (Python 3.6+) are the modern way to embed values in strings. Prefix the string with `f` and put variables or expressions inside `{}`. They're faster, cleaner, and more readable than older methods.

Older methods include `.format()` and `%-formatting` — you'll see them in legacy code but avoid them for new projects.

**Escape sequences** let you include special characters: `\n` for newline, `\t` for tab, `\\` for a literal backslash. **Raw strings** (`r"..."`) disable escape processing — perfect for file paths and regular expressions.

## Code Example

```python
"""Music player — now playing display with formatted strings"""

# Current track info
song = "Bohemian Rhapsody"
artist = "Queen"
album = "A Night at the Opera"
duration_sec = 354
progress_sec = 127
rating = 4.8

# f-strings — the modern way
print(f"🎵 Now Playing: {song} by {artist}")
print(f"   Album: {album}")
print(f"   Duration: {duration_sec // 60}:{duration_sec % 60:02d}")
print(f"   Progress: {progress_sec // 60}:{progress_sec % 60:02d}")
print(f"   Rating: {rating}/5.0")

# Expressions inside f-strings
print(f"\nProgress percentage: {progress_sec / duration_sec * 100:.1f}%")
print(f"Next track: {'We Will Rock You' if rating > 4.0 else 'Unknown'}")

# .format() method — older but still in use
print("\n--- Library Entry ---")
print("Track: {} by {} ({})".format(song, artist, album))

# Escape sequences
print("\n--- Playlist ---")
print("1. Come Together\t2. Dream On\t3. Stairway")
print("Lyrics preview:\nIs this the real life?\nIs this just fantasy?")

# Raw strings for file paths
music_path = r"C:\Users\DJ\Music\Classic Rock"
print(f"\nMusic folder: {music_path}")
```

## 🔍 How It Works

- `f"Now Playing: {song} by {artist}"` — f-string embeds variable values directly inside `{}`
- `{duration_sec // 60}:{duration_sec % 60:02d}` — expressions inside f-strings: floor division for minutes, modulo for seconds, `:02d` pads to 2 digits
- `{progress_sec / duration_sec * 100:.1f}` — calculates percentage, `:.1f` formats to 1 decimal place
- `"Track: {} by {} ({})".format(song, artist, album)` — `.format()` inserts arguments into `{}` placeholders in order
- `\n` — newline character, moves to the next line
- `\t` — tab character, aligns to the next tab stop
- `r"C:\Users\DJ\Music\Classic Rock"` — raw string: backslashes are literal, not escape sequences

## ⚠️ Common Pitfall

Mixing up f-string quotes: `f"{song}"` is fine, but `f'{song}'` also works. The problem is when you need quotes inside — `f"He said {name}"` needs the outer quotes to be different from any quotes inside. Also, forgetting `r` before Windows paths: `"C:\new_folder"` prints a newline instead of the path because `\n` is interpreted as an escape.

## 🧠 Memory Aid

**"f-string = formatting string — the 'f' stands for 'fill in the blanks'."** Think of the `{}` as blank spots on a concert ticket that get stamped with the variable's value when the show starts.

## 🏃 Try It

Run the code file:
```bash
python code/01-06-string-formatting.py
```
Then change the song info to your favorite track and add a `played_count` variable to the display.

## 🔗 Related

- [Variables](02-variables.md) — what goes inside the curly braces
- [Input & Output](05-input-output.md) — printing the formatted string

## ➡️ Next

→ [07 — Type Casting](07-type-casting.md)
