import requests

PINATA_API_KEY = "3755c3257b00533236bf"
PINATA_SECRET_API_KEY = "3c57c5293975a54eb3d7d0e71e07ef69f4c991e269698ac9bae99810155a891b"

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
        return ipfs_hash
    else:
        print("❌ Failed to upload:", response.text)
        return None
