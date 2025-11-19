def xor_encrypt_decrypt(data: bytes, key: str) -> bytes:
    key_bytes = key.encode()
    return bytes([data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data))])

def encrypt_file_xor(input_path, output_path, key):
    with open(input_path, "rb") as f:
        data = f.read()

    result = xor_encrypt_decrypt(data, key)

    with open(output_path, "wb") as f:
        f.write(result)

def decrypt_file_xor(input_path, output_path, key):
    encrypt_file_xor(input_path, output_path, key)  # XOR is symmetric
