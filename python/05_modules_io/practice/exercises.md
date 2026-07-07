# Phase 05 — Practice Exercises

## 1. 🟢 Custom Config Parser
Write a function `parse_ini(path)` that reads an INI-style config file and returns a dict of sections with key-value pairs.
> 💡 Hint: Lines starting with `[` are section headers; `key=value` lines belong to the current section.

## 2. 🟢 Dice Roller Simulator
Write `roll_dice(num=2, sides=6)` that returns a list of rolls and the total. Use Monte Carlo to estimate the probability of each possible sum.
> 💡 Hint: `random.randint(1, sides)` for each die; run 100K trials for probability estimates.

## 3. 🟡 Meeting Scheduler
Write `find_slots(booked_slots, duration_minutes, start_hour=9, end_hour=17)` that finds available time slots of a given duration in a day.
> 💡 Hint: Generate all 30-minute slots; filter out overlaps with booked_slots.

## 4. 🟡 CSV Aggregator
Write `aggregate_csv(input_path, output_path, group_by_col, value_col)` that groups rows by one column and sums values in another.
> 💡 Hint: Use `csv.DictReader` and a dict of running totals.

## 5. 🟡 File Organizer by Date
Write `organize_by_date(directory)` that moves files into subdirectories named `YYYY/MM/` based on their last-modified timestamp.
> 💡 Hint: `datetime.fromtimestamp(f.stat().st_mtime)` gives you the modified time.

## 6. 🟡 JSON Data Validator
Write `validate_users(json_path)` that loads a JSON array of users and checks each has required fields: `id`, `name`, `email`. Report missing fields.
> 💡 Hint: Loop through items; use `all(k in user for k in required)`.

## 7. 🔴 Regex Log Parser
Write `analyze_log(log_path)` that parses a server log and returns error counts by module, top 5 error messages, and request count per hour.
> 💡 Hint: Use `re.finditer` with capture groups; sort by frequency with `Counter`.

## 8. 🔴 Password Manager
Write `store_passwords(path, accounts)` and `retrieve_password(path, service)` that save/load encrypted passwords using hashlib + secrets.
> 💡 Hint: Store as JSON with PBKDF2-hashed passwords; use UUID as lookup keys.

## 9. 🔴 Backup Script
Write `backup_project(source, dest)` that creates a timestamped zip backup, verifies the archive exists, and reports disk usage before/after.
> 💡 Hint: `shutil.make_archive` + `shutil.disk_usage` for reporting.

## 10. 🔴 Markdown Link Extractor
Write `extract_markdown_links(md_text)` using regex to extract all `[text](url)` patterns from markdown.
> 💡 Hint: Pattern: `r"\[([^\]]+)\]\(([^)]+)\)"` captures link text and URL.

## 11. 🟡 Shopping Cart with `decimal`
Write `ShoppingCart` that stores items with prices as `Decimal` strings. Add `add_item(name, price_str)`, `total()`, and `tax(rate_str)`. Demonstrate that float-based pricing gives wrong totals for 3+ items with 8% tax.

Then extend with a `configparser`-based config that loads `[tax]` and `[currency]` settings from an INI string.
> 💡 Hint: `Decimal("0.1") * 3 == Decimal("0.3")` but `0.1 * 3 == 0.30000000000000004`.
