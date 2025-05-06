# main.py

from ebay.ebay_api import fetch_sold_items

def main():
    keyword = "ps5"
    sold_items = fetch_sold_items(keyword, entries=10)

    if not sold_items:
        print("No sold items found or API call failed.")
        return

    for i, item in enumerate(sold_items, 1):
        print(f"\nItem {i}")
        print(f"Title: {item['title']}")
        print(f"Price: £{item['price']}")
        print(f"Condition: {item['condition']}")
        print(f"URL: {item['url']}")

if __name__ == "__main__":
    main()
