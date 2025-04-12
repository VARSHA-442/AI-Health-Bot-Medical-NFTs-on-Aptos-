from cryptography.fernet import Fernet
import os

# Make sure the key is securely stored!
key = Fernet.generate_key()
cipher = Fernet(key)

def generate_encrypted_file(data: str, output_path="encrypted_summary.json"):
    encrypted_data = cipher.encrypt(data.encode())

    # Save encrypted data to file
    with open(output_path, 'wb') as file:
        file.write(encrypted_data)

    return os.path.abspath(output_path)