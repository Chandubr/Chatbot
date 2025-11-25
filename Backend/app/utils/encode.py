import base64

def encode_key(key: str) -> str:
    """Encode a string key using Base64."""
    key_bytes = key.encode('utf-8')
    encoded_bytes = base64.b64encode(key_bytes)
    return encoded_bytes.decode('utf-8')

def decode_key(encoded_key: str) -> str:
    """Decode a Base64-encoded string key."""
    encoded_bytes = encoded_key.encode('utf-8')
    key_bytes = base64.b64decode(encoded_bytes)
    return key_bytes.decode('utf-8')

print(encode_key("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"))