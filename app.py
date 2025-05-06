from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

EBAY_BASE_URL = "https://api.ebay.com/buy/browse/v1"

def get_headers():
    return {
        "Authorization": f"Bearer {os.getenv('EBAY_ACCESS_TOKEN')}",
        "Content-Type": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_GB"
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    item_data = None
    search_results = None
    error = None

    if request.method == 'POST':
        mode = request.form.get('mode')

        if mode == 'id':
            item_id = request.form.get('item_id')
            url = f"{EBAY_BASE_URL}/item/get_item_by_legacy_id?legacy_item_id={item_id}"
            response = requests.get(url, headers=get_headers())

            if response.status_code == 200:
                item_data = response.json()
            else:
                error = "Item not found with that ID."

        elif mode == 'search':
            query = request.form.get('query')
            postcode = request.form.get('postcode')
            offset = int(request.args.get('offset', 0))

            filters = []
            if postcode:
                filters.append(f"itemLocationPostalCode:{postcode}")

            filter_str = ",".join(filters)
            filter_query = f"&filter={filter_str}" if filters else ""

            search_url = f"{EBAY_BASE_URL}/item_summary/search?q={query}&limit=20&offset={offset}{filter_query}"
            response = requests.get(search_url, headers=get_headers())

            if response.status_code == 200:
                search_results = response.json().get("itemSummaries", [])
            else:
                error = "No results found or search failed."

    return render_template("index.html", item=item_data, results=search_results, error=error)

if __name__ == '__main__':
    app.run(debug=True)
