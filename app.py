from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    item_data = None
    error = None

    if request.method == 'POST':
        item_id = request.form.get('item_id')
        print(f"📦 Fetching item ID: {item_id}")

        access_token = os.getenv("EBAY_ACCESS_TOKEN")
        if not access_token:
            error = "Access token not found."
            return render_template("index.html", error=error)

        url = f"https://api.ebay.com/buy/browse/v1/item/get_item_by_legacy_id?legacy_item_id={item_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-EBAY-C-MARKETPLACE-ID": "EBAY_GB"
        }

        response = requests.get(url, headers=headers)
        print(f"📢 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")

        if response.status_code == 200:
            item_data = response.json()
        else:
            error = "Item not found or invalid ID."

    return render_template("index.html", item=item_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)
