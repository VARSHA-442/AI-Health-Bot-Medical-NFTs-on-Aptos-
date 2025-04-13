# In utils/mint_nft.py
import requests

def mint_nft_to_patron(ipfs_hash, wallet_address):
    url = "https://api.nftmintingplatform.com/mint"


  # Replace with the correct URL
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer your_token",  # If needed
    }
    payload = {
        "ipfs_hash": ipfs_hash,
        "wallet_address": wallet_address
    }
    
    # Adding verify=False to bypass SSL certificate verification temporarily
    response = requests.post(url, headers=headers, json=payload, verify=False)
    
    # Check the response and handle it accordingly
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None
