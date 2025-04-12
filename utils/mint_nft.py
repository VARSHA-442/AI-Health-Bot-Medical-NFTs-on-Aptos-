import requests

def mint_nft_to_patron(metadata_cid, wallet_address):
    url = "https://api.patron.ai/v1/nft/mint"  # placeholder, update from docs

    headers = {
        "Authorization": "Bearer YOUR_PATRON_API_KEY",  # if needed
        "Content-Type": "application/json"
    }

    payload = {
        "recipient": wallet_address,
        "metadata_uri": f"https://gateway.pinata.cloud/ipfs/{metadata_cid}",
        "collection_name": "AIHealthBot",
        "name": "AI Health Summary",
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()