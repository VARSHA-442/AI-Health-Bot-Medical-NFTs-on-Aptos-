from cryptography.fernet import Fernet
from app import generate_summary

from cryptography.fernet import Fernet

def generate_encrypted_file(summary_text):
    key = Fernet.generate_key()
    cipher = Fernet(key)

    encrypted_summary = cipher.encrypt(summary_text.encode())

    with open("encrypt.txt", "wb") as file:
        file.write(encrypted_summary)

    with open("key.txt", "wb") as key_file:
        key_file.write(key)

    return "encrypt.txt", "key.txt"