import requests
from cryptography.fernet import Fernet
from utils.encrypter import generate_encrypted_file

summary_text = "This is the health summary to encrypt."  # Replace with actual summary
encrypt_file, key_file = generate_encrypted_file(summary_text)

# Read the key
with open(key_file, "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

with open(encrypt_file, "rb") as file:
    encrypted_summary = file.read()


PINATA_API_KEY = "9a17fbd24197fae05247"
PINATA_SECRET_API_KEY = "dbcf4aad6f2f69a99e66aefe0bf32f6f5f64aefe5e9716d728b2b9df130eb5a3"

def upload_to_pinata(file_path):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY
    }
    with open(file_path, "rb") as file:
        response = requests.post(url, files={"file": file}, headers=headers)
    if response.status_code == 200:
        ipfs_hash = response.json()["IpfsHash"]
        print(f"✅ Uploaded to IPFS: https://gateway.pinata.cloud/ipfs/{ipfs_hash}")
        return ipfs_hash
    else:
        print("❌ Failed to upload:", response.text)
        return None

# Upload to IPFS
upload_to_pinata(encrypt_file)