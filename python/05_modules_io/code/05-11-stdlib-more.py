"""More practical stdlib: decimal, configparser, glob, timeit, base64, zipfile, tempfile"""
from decimal import Decimal, ROUND_HALF_UP
from configparser import ConfigParser
import glob
import timeit
import base64
import zipfile
import tempfile
import os
from pathlib import Path

print("=== decimal — precise money math ===")
price = Decimal("19.99")
tax = price * Decimal("0.08")
total = price + tax
print(f"${price} + tax (${tax:.2f}) = ${total:.2f}")
print(f"Float would be: {19.99 * 1.08:.17f}  # imprecise!")
print(f"Rounded: {total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}")

print("\n=== configparser — .ini files ===")
cfg = ConfigParser()
cfg.read_string("[database]\nhost = localhost\nport = 5432\n")
print(f"DB: {cfg['database']['host']}:{cfg['database']['port']}")

print("\n=== glob — file pattern matching ===")
# Use the code dir itself as example
pattern = os.path.join(os.path.dirname(__file__) or ".", "05-*.py")
matches = sorted(glob.glob(pattern))
print(f"Found {len(matches)} files matching 05-*.py: {[Path(m).name for m in matches[:3]]}...")

print("\n=== timeit — benchmarking ===")
setup = "nums = list(range(1000))"
stmt_list = "[x*2 for x in nums]"
stmt_gen = "list(x*2 for x in nums)"
t_list = timeit.timeit(stmt_list, setup, number=10000)
t_gen = timeit.timeit(stmt_gen, setup, number=10000)
print(f"List comp:  {t_list:.4f}s")
print(f"Generator:  {t_gen:.4f}s")
print(f"Faster: {'list comp' if t_list < t_gen else 'generator'}")

print("\n=== base64 — API-safe binary encoding ===")
token = base64.urlsafe_b64encode(b"user:api_key_12345").decode()
print(f"Encoded token: {token}")
decoded = base64.urlsafe_b64decode(token.encode()).decode()
print(f"Decoded: {decoded}")

print("\n=== zipfile + tempfile ===")
with tempfile.TemporaryDirectory() as tmpdir:
    zip_path = Path(tmpdir) / "example.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("data.txt", "Hello from ZIP!")
        zf.writestr("config.json", '{"version": 1}')
    with zipfile.ZipFile(zip_path, "r") as zf:
        print(f"ZIP contains: {zf.namelist()}")
        print(f"  data.txt → {zf.read('data.txt').decode()}")
    print(f"Temp dir {tmpdir} will auto-delete after this block")
print("Temp dir cleaned up (no longer exists).")
