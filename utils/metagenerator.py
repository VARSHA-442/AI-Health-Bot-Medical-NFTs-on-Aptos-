import hashlib, json, uuid
from datetime import datetime
from .pinata_uploader import upload_to_pinata

def get_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    return sha256.hexdigest()

def create_metadata_json(ipfs_url, file_hash):
    metadata = {
        "name": "SecureDataNFT",
        "description": "Encrypted file stored on IPFS",
        "image": None,
        "encrypted_file_url": ipfs_url,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "hash": file_hash,
        "token_id": str(uuid.uuid4())
    }
    with open("metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
    return "metadata.json"

def upload_metadata(encrypted_file_path, api_key, secret_key):
    file_hash = get_sha256(encrypted_file_path)
    file_ipfs_url = upload_to_pinata(encrypted_file_path, api_key, secret_key)
    if not file_ipfs_url:
        raise Exception("Encrypted file upload failed.")

    metadata_file = create_metadata_json(file_ipfs_url, file_hash)
    metadata_ipfs_url = upload_to_pinata(metadata_file, api_key, secret_key)
    return metadata_ipfs_url