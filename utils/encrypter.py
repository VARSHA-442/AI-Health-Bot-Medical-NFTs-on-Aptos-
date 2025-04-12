from cryptography.fernet import Fernet

def generate_encrypted_file(summary_text, output_path="encrypt.txt", key_path="key.txt"):
    key = Fernet.generate_key()
    cipher = Fernet(key)

    encrypted_summary = cipher.encrypt(summary_text.encode())

    with open(output_path, "wb") as file:
        file.write(encrypted_summary)

    with open(key_path, "wb") as key_file:
        key_file.write(key)

    return output_path, key_path
