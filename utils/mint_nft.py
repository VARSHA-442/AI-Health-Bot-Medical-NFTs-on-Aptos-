# import requests
# def mint_nft_to_patron(ipfs_hash, wallet_address):
#     url = "https://your-backend.com/api/mint"  # Replace with your actual endpoint
#     headers = {
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "wallet_address": wallet_address,
#         "ipfs_hash": ipfs_hash
#     }

#     try:
#         response = requests.post(url, headers=headers, json=payload)
#         response.raise_for_status()  # Raise if 4xx or 5xx
#         try:
#             return response.json()  # Try parsing JSON
#         except requests.exceptions.JSONDecodeError:
#             print("Non-JSON response received:")
#             print(response.text)
#             return {"error": "Invalid JSON returned from server"}
#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {e}")
#         return {"error": str(e)}
import requests

def mint_nft_to_patron(ipfs_hash, wallet_address):
    url = "https://your-nft-api-endpoint"  # replace with real endpoint
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_API_KEY"  # if needed
    }
    payload = {
        "wallet_address": wallet_address,
        "ipfs_hash": ipfs_hash
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        try:
            return response.json()
        except ValueError:
            # JSON parsing failed, show raw response for debugging
            return {
                "success": False,
                "error": "Invalid JSON returned from server",
                "raw_response": response.text,
                "status_code": response.status_code
            }
    except Exception as e:
        return {"success": False, "error": str(e)}
