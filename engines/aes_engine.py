from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key_from_password(password: str):
    digest = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(digest)

def encrypt_file_aes(input_path, output_path, password):
    key = generate_key_from_password(password)
    fernet = Fernet(key)

    with open(input_path, "rb") as f:
        data = f.read()

    encrypted = fernet.encrypt(data)

    with open(output_path, "wb") as f:
        f.write(encrypted)

def decrypt_file_aes(input_path, output_path, password):
    key = generate_key_from_password(password)
    fernet = Fernet(key)

    with open(input_path, "rb") as f:
        encrypted = f.read()

    try:
        decrypted = fernet.decrypt(encrypted)
    except:
        return False  # wrong password or corrupted file

    with open(output_path, "wb") as f:
        f.write(decrypted)

    return True
