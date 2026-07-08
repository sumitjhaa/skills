"""
09.19 Structured Generation — JSON Schema-Constrained Decoding
Built with only numpy, scipy, matplotlib.
"""
import numpy as np


class JSONSchema:
    """Simple JSON schema for constrained generation."""

    def __init__(self, schema_dict):
        self.schema = schema_dict

    def get_allowed_tokens(self, partial_json, vocab_indices, token_strings):
        """Return mask of valid next tokens given partial JSON."""
        # Simplified: track JSON state machine
        text = " ".join(token_strings)
        if not partial_json:
            return self._mask_for_state("start")

        # Check what we're building
        in_key = '":' in text and not text.rstrip().endswith('":')
        in_value = ':' in text and not text.rstrip().endswith(',') and not text.rstrip().endswith('{')

        mask = np.ones(len(vocab_indices), dtype=bool)

        # Always allow whitespace, separators terminators
        for i, tok in enumerate(token_strings):
            if tok in (' ', ',', '}'):
                continue

        return mask

    def _mask_for_state(self, state):
        # Placeholder: return all tokens allowed
        return np.ones(100, dtype=bool)


class ConstrainedDecoder:
    """
    Logit masking for structured output generation.
    """

    def __init__(self, vocab_size=100):
        self.vocab_size = vocab_size
        self.logits = np.random.randn(vocab_size)

    def generate_with_schema(self, schema, num_tokens=20):
        schema_obj = JSONSchema(schema) if schema else None
        generated_tokens = []
        generated_text = []

        for step in range(num_tokens):
            # Get base logits
            self.logits = np.random.randn(self.vocab_size)
            # Apply constraint mask
            if schema_obj:
                mask = schema_obj.get_allowed_tokens(
                    generated_text, list(range(self.vocab_size)), generated_text
                )
                self.logits[~mask] = -1e9
            # Sample
            probs = np.exp(self.logits - np.max(self.logits))
            probs = probs / probs.sum()
            token = np.random.choice(self.vocab_size, p=probs)
            generated_tokens.append(token)
            generated_text.append(f"tok_{token}")

        return generated_text


class JSONConstraint:
    """Track JSON structure to mask invalid tokens."""

    def __init__(self, schema):
        self.schema = schema  # {"type": "object", "properties": {...}}

    def get_valid_next(self, partial):
        """Return list of token IDs that are valid next."""
        stripped = partial.strip()
        if not stripped:
            return [ord('{')]  # must start with {
        if stripped == "{":
            return self._valid_keys()
        if stripped.endswith(":"):
            return self._valid_value_tokens()
        return list(range(32, 127))

    def _valid_keys(self):
        return [ord('"')]

    def _valid_value_tokens(self):
        return [ord('"'), ord('t'), ord('f'), ord('n'), ord('0'), ord('{'), ord('[')]


def mask_logits(logits, valid_tokens, vocab_size=256):
    mask = np.ones(vocab_size, dtype=bool)
    mask[valid_tokens] = True
    logits[~mask] = -1e9
    return logits


if __name__ == "__main__":
    schema = {"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "number"}}}
    constraint = JSONConstraint(schema)

    states = ["", "{", '{"name"', '{"name": ']
    for state in states:
        valid = constraint.get_valid_next(state)
        chars = [chr(v) if 32 <= v < 127 else f"\\x{v:02x}" for v in valid[:5]]
        print(f"State '{state[:20]:20s}' -> valid next: {chars}{'...' if len(valid) > 5 else ''}")

    # Decoder demo
    decoder = ConstrainedDecoder(vocab_size=256)
    output = decoder.generate_with_schema(schema, num_tokens=15)
    print(f"\nGenerated tokens: {output}")
