# ebay/ebay_api.py

import requests
from config.settings import EBAY_APP_ID

def fetch_sold_items(keyword, entries=10):
    url = "https://svcs.ebay.com/services/search/FindingService/v1"

    params = {
        "OPERATION-NAME": "findCompletedItems",
        "SERVICE-VERSION": "1.13.0",
        "SECURITY-APPNAME": EBAY_APP_ID,
        "RESPONSE-DATA-FORMAT": "JSON",
        "REST-PAYLOAD": "true",
        "keywords": keyword,
        "paginationInput.entriesPerPage": entries,
        "itemFilter(0).name": "SoldItemsOnly",
        "itemFilter(0).value": "true"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        items = data['findCompletedItemsResponse'][0]['searchResult'][0].get('item', [])

        return [{
            "title": i['title'][0],
            "price": float(i['sellingStatus'][0]['currentPrice'][0]['__value__']),
            "condition": i.get("condition", [{}])[0].get("conditionDisplayName", "Unknown"),
            "url": i['viewItemURL'][0]
        } for i in items]

    except Exception as e:
        print(f"❌ Error fetching sold items: {e}")
        return []
