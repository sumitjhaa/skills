"""String operations — vectorized str methods, regex, extraction."""
import pandas as pd
import numpy as np


print("=== String Operations ===")

df = pd.DataFrame({
    "name": ["Alice Smith", "Bob Johnson", "Charlie Brown", "Diana Ross", "Eve Davis"],
    "email": [
        "alice.smith@example.com",
        "bob@test.org",
        "charlie@company.co.uk",
        "diana@web.net",
        "eve@demo.io",
    ],
    "phone": ["(212) 555-0101", "415-555-0202", "+1 (310) 555-0303", "555-0404", "N/A"],
    "notes": ["First purchase", None, "VIP customer", "Returned item", None],
})

print(f"Data:\n{df}")

print(f"\nBasic string methods:")
print(f"  Name lower: {df['name'].str.lower().tolist()}")
print(f"  Name split (first): {df['name'].str.split().str[0].tolist()}")
print(f"  Name split (last):  {df['name'].str.split().str[-1].tolist()}")

print(f"\nContains / startswith:")
print(f"  Contains 'alice' (case=False): {df['email'].str.contains('alice', case=False).tolist()}")
print(f"  Ends with .com: {df['email'].str.endswith('.com').tolist()}")

print(f"\nExtract email parts:")
extracted = df["email"].str.extract(r"(\w+)@(\w+)\.(\w+)")
extracted.columns = ["username", "domain", "tld"]
print(f"{extracted}")

print(f"\nClean phone numbers:")
df["phone_clean"] = df["phone"].str.replace(r"\D", "", regex=True)
print(f"  {df['phone_clean'].tolist()}")

print(f"\nMissing notes:")
print(f"  Is null: {df['notes'].isna().tolist()}")
print(f"  Fill:    {df['notes'].fillna('No notes').tolist()}")
