import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time
import random

# Headers to mimic browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

BASE_URL = "https://www.amazon.in/s?k=samsung+s24+ultra+5g+mobile&crid=28QOY5BKVNH13&sprefix=Sam%2Caps%2C447&ref=nb_sb_ss_mvt-t11-ranker_1_3"


def get_soup(url):
    response = requests.get(url, headers=HEADERS)
    return BeautifulSoup(response.content, "html.parser")

def extract_data(soup):
    products = []

    results = soup.find_all("div", {"data-component-type": "s-search-result"})

    for item in results:
        try:
            # Title
            title = item.h2.text.strip() if item.h2 else "N/A"

            # Price
            price = item.find("span", "a-price-whole")
            price = price.text.strip() if price else "N/A"

            # Rating
            rating = item.find("span", "a-icon-alt")
            rating = rating.text.strip() if rating else "N/A"

            # Image
            image = item.find("img")
            image_url = image["src"] if image else "N/A"

            # Ad / Organic
            ad_tag = item.find("span", string="Sponsored")
            ad_status = "Ad" if ad_tag else "Organic"

            products.append({
                "Title": title,
                "Price": price,
                "Rating": rating,
                "Image": image_url,
                "Type": ad_status
            })

        except Exception as e:
            continue

    return products


def scrape_amazon(pages=3):
    all_products = []

    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")

        url = BASE_URL + f"&page={page}"
        soup = get_soup(url)

        products = extract_data(soup)
        all_products.extend(products)

        time.sleep(random.uniform(2, 4))  # avoid blocking

    return all_products


def save_to_csv(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"amazon_Mobile_{timestamp}.csv"

    keys = data[0].keys()

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"Saved file: {filename}")


if __name__ == "__main__":
    data = scrape_amazon(pages=3)

    if data:
        save_to_csv(data)
    else:
        print("No data found!")
        