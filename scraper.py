# scraper.py

from bs4 import BeautifulSoup
import requests
import csv
import os

CSV_FILE = "out.csv"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5'
}
FIELDS = ["ASIN", "Title", "Brand", "Price", "Rating", "Review Count", "Availability", "Image URL", "Category", "Description"]

def write_headers():
    if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
        with open(CSV_FILE, "w", newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(FIELDS)

def extract_asin(url):
    for key in ["/dp/", "/gp/product/"]:
        if key in url:
            return url.split(key)[1].split("/")[0]
    return "NA"

def get_text(soup, selector):
    tag = soup.select_one(selector)
    return tag.get_text(strip=True).replace(',', '') if tag else "NA"

def scrape_amazon_product(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "lxml")
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

    try:
        data = {
            "ASIN": extract_asin(url),
            "Title": get_text(soup, "span#productTitle"),
            "Brand": get_text(soup, "a#bylineInfo"),
            "Price": get_text(soup, "span#priceblock_ourprice") or get_text(soup, "span#priceblock_dealprice"),
            "Rating": get_text(soup, "span.a-icon-alt"),
            "Review Count": get_text(soup, "span#acrCustomerReviewText"),
            "Availability": get_text(soup, "div#availability span"),
            "Image URL": soup.select_one("#imgTagWrapperId img")['src'] if soup.select_one("#imgTagWrapperId img") else "NA",
            "Category": " > ".join([c.get_text(strip=True) for c in soup.select("a.a-link-normal.a-color-tertiary")]) or "NA",
            "Description": " | ".join([b.get_text(strip=True).replace(',', '') for b in soup.select("div#feature-bullets ul li span")]) or "NA"
        }

        if data["Title"] == "NA":
            return {"error": "Product details not found. Amazon may have blocked the request or changed the page structure."}

        with open(CSV_FILE, "a", newline='', encoding='utf-8') as f:
            csv.writer(f).writerow([data[field] for field in FIELDS])

        return data

    except Exception as e:
        return {"error": f"Parsing failed: {str(e)}"}
