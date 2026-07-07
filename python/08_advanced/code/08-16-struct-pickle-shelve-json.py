"""08-16-struct-pickle-shelve-json.py — WAV header parser, ML model save/load, custom JSON."""

import struct
import pickle
import json
from datetime import datetime, date, timezone
from decimal import Decimal


def parse_wav_header(data: bytes) -> dict:
    riff, size, wave, fmt, fmt_len, audio_fmt, num_ch, sample_rate, byte_rate, block_align, bits_per = (
        struct.unpack_from("<4sI4s4sIHHIIHH", data, 0)
    )
    return {
        "format": audio_fmt, "channels": num_ch, "sample_rate": sample_rate,
        "byte_rate": byte_rate, "bits_per_sample": bits_per,
    }


def ml_model_roundtrip():
    model = {"weights": [0.42, 0.13, 0.97], "bias": 0.5, "layers": 2}
    blob = pickle.dumps(model)
    loaded = pickle.loads(blob)
    assert model == loaded
    print(f"ML model pickled: {len(blob)} bytes, restored OK")
    return loaded


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def custom_json_serialize():
    data = {"event": "sale", "amount": Decimal("19.99"), "timestamp": datetime.now(timezone.utc)}
    encoded = json.dumps(data, cls=CustomEncoder)
    print(f"Custom JSON: {encoded}")
    return encoded


if __name__ == "__main__":
    header = parse_wav_header(b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x02\x00\x44\xac\x00\x00\x10\xb1\x02\x00\x04\x00\x10\x00")
    print(f"WAV: {header}")
    ml_model_roundtrip()
    custom_json_serialize()
