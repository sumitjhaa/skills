"""Email validation and data cleaning — string methods in action"""

raw_email = "  Harry.Potter@HOGWARTS.UK  "
raw_hashtag = "#Python #HarryPotter #100DaysOfCode"
csv_line = "Harry,Ron,Hermione,Ginny,Neville"

print("=== Input Cleaning ===")
cleaned_email = raw_email.strip().lower()
print(f"  Raw: '{raw_email}'")
print(f"  Cleaned: '{cleaned_email}'")

print("\n=== Validation ===")
print(f"  Contains '@': {'@' in cleaned_email}")
print(f"  Has digits: {any(c.isdigit() for c in cleaned_email)}")

print("\n=== Hashtag Parsing ===")
tags = raw_hashtag.split()
print(f"  Raw hashtags: {tags}")
clean_tags = [tag.strip("#").lower() for tag in tags]
print(f"  Clean tags: {clean_tags}")
rejoined = " | ".join(clean_tags)
print(f"  Rejoined: {rejoined}")

print("\n=== CSV Parsing ===")
wizard_list = csv_line.split(",")
print(f"  Wizards: {wizard_list}")
for i, wizard in enumerate(wizard_list, 1):
    print(f"    {i}. {wizard.strip()}")

print("\n=== Search & Replace ===")
message = "You're a wizard, Harry."
print(f"  Find 'wizard': {message.find('wizard')}")
print(f"  Replace: {message.replace('Harry', 'Hermione')}")

print(f"\n  zfill example: {'7'.zfill(3)}")
