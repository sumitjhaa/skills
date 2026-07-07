# 🎯 struct, pickle, shelve, json deep — Serialization
<!-- ⏱️ 16 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Pack/unpack binary data with `struct`, serialize objects with `pickle`, persist dicts with `shelve`, and customize JSON encoding.

> 💡 **TL;DR — The whole point:** `struct` reads/writes binary C-style data, `pickle` saves/loads any Python object, `shelve` gives a persistent dict backed by a database, and `json.dumps`/`json.load` can be extended with custom encoders.

## 🔗 Why This Matters
WAV file readers, network protocol parsers, ML model persistence, and Redis-like caches all need serialization. Understanding these modules means you can write binary parsers, save trained models, and build config systems that handle custom types like `datetime` and `Decimal`.

## The Concept
- `struct.pack(fmt, v1, v2, ...)` → bytes. `struct.unpack(fmt, data)` → tuple. Format strings like `"<4sI"` mean little-endian 4-char string + unsigned int
- `pickle.dump(obj, file)` / `pickle.load(file)`. `__reduce__` on a class defines how it's pickled. WARNING: never unpickle untrusted data (RCE vector)
- `shelve.open(filename)` returns a dict-like object. Values are pickled to a dbm file. Keys must be strings
- `json.dumps(obj, cls=MyEncoder)` — override `default()` in a `JSONEncoder` subclass to handle non-serializable types

## Code Example
```python
"""WAV header parser, ML model save/load, custom JSON with datetime/Decimal."""

import struct, pickle, json, shelve
from datetime import datetime, timezone
from decimal import Decimal


# ─── struct: WAV file header ───
wav_header = struct.pack("<4sI4s4sIHHIIHH",
    b"RIFF", 36, b"WAVE", b"fmt ", 16, 1, 2, 44100, 176400, 4, 16)
riff, size, wave, fmt, flen, audio_fmt, ch, sr, br, align, bits = (
    struct.unpack_from("<4sI4s4sIHHIIHH", wav_header, 0))
print(f"WAV: {ch}ch, {sr}Hz, {bits}bit")

# ─── pickle: ML model roundtrip ───
model = {"weights": [0.42, 0.13, 0.97], "bias": 0.5, "layers": 2}
blob = pickle.dumps(model)
loaded = pickle.loads(blob)
assert model == loaded

class MLModel:
    def __init__(self, weights, bias):
        self.weights, self.bias = weights, bias
    def __reduce__(self):
        return (self.__class__, (self.weights, self.bias))

# ─── json: Custom encoder ───
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, Decimal)):
            return str(obj)
        return super().default(obj)

data = {"amount": Decimal("19.99"), "ts": datetime.now(timezone.utc)}
print(json.dumps(data, cls=CustomEncoder))
```

## 🔍 How It Works
- `struct` format strings: `<>` = endianness, `I` = unsigned int (4 bytes), `H` = unsigned short (2), `f` = float (4), `d` = double (8), `s` = bytes. Prefix with count: `4s` = 4 bytes
- `pickle` protocol versions: 0=text, 2=binary, 3=python3, 4=large objects, 5=out-of-band data. Use `pickle.DEFAULT_PROTOCOL`
- `shelve` writes separate files: `.bak`, `.dat`, `.dir`. Use `shelve.open(filename, writeback=True)` to auto-sync changes to mutable values
- `json` `cls` parameter lets you pass a custom `JSONEncoder`. The `default` method is called for objects that aren't natively serializable

## ⚠️ Common Pitfall
`pickle.load` on untrusted data is a remote code execution vulnerability. Use `json` or a safe format for untrusted sources. `shelve` also uses pickle internally, so same warning applies.

## 🧠 Memory Aid
"`struct` = C bytes ↔ Python. `pickle` = freeze/thaw any object. `shelve` = dict on disk. `json.dumps(cls=...)` = teach JSON new tricks. Endianness: `<` = little, `>` = big."

## 🏃 Try It
Write a PNG header parser using `struct`. The PNG signature is 8 bytes: `\x89PNG\r\n\x1a\n`. After that, chunks have 4-byte length, 4-byte type, data, 4-byte CRC. Extract the IHDR chunk dimensions.

## 🔗 Related
- [Modules & IO](../05_modules_io/lessons/13-io-deep.md) — binary file I/O
- [Concurrent Futures](12-concurrent-futures.md) — parallel processing with pickled data

## ➡️ Next
[gc, dis, sys deep](17-gc-dis-sys.md)
