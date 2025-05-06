import os
import requests
from dotenv import load_dotenv

# Load existing .env variables
load_dotenv()

# Get client ID and secret from .env
client_id = os.getenv("EBAY_CLIENT_ID")
client_secret = os.getenv("EBAY_CLIENT_SECRET")

# Basic check
if not client_id or not client_secret:
    print("❌ Missing client ID or secret in .env.")
    exit()

# Encode credentials for Basic Auth
import base64
auth_string = f"{client_id}:{client_secret}"
auth_encoded = base64.b64encode(auth_string.encode()).decode()

# Prepare request
url = "https://api.ebay.com/identity/v1/oauth2/token"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {auth_encoded}"
}
data = {
    "grant_type": "client_credentials",
    "scope": "https://api.ebay.com/oauth/api_scope"
}

# Make request
response = requests.post(url, headers=headers, data=data)

# Handle response
if response.status_code == 200:
    token = response.json().get("access_token")
    print("✅ Token retrieved!")

    # Update .env file
    with open(".env", "r") as f:
        lines = f.readlines()

    with open(".env", "w") as f:
        for line in lines:
            if line.startswith("EBAY_ACCESS_TOKEN="):
                f.write(f"EBAY_ACCESS_TOKEN={token}\n")
            else:
                f.write(line)

    print("✅ .env file updated with new token!")
else:
    print("❌ Failed to get token.")
    print("Status:", response.status_code)
    print("Response:", response.text)
