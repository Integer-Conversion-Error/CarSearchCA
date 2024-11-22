import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import json
import csv

def scroll_and_fetch_listings(url, scroll_pause_time=3, max_scrolls=30):
    """
    Scrolls the page to load more listings and extracts JSON data from script tags.
    """
    service = Service(executable_path=r"C:\\Users\\togoo\\Desktop\\Self Improvement\\Coding Projects\\CarSearchCA\\chromedriver-win64\\chromedriver.exe")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)

    # Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

    # Scroll down to load more listings
    for scroll_count in range(max_scrolls):
        print(f"Scrolling... ({scroll_count + 1}/{max_scrolls})")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

    # Extract the page source after scrolling
    page_source = driver.page_source
    driver.quit()

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    script_tags = soup.find_all('script', {'type': 'application/ld+json'})

    listings = []
    for script in script_tags:
        try:
            json_data = json.loads(script.string)
            if json_data.get('@type') == 'ItemList':
                listings.extend(json_data.get('itemListElement', []))
        except (json.JSONDecodeError, KeyError):
            continue

    return listings


def save_to_csv(listings, file_name):
    """
    Saves listings to a CSV file with the specified file name.
    """
    fieldnames = ['Position', 'Name', 'Description', 'Image']
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for listing in listings:
            writer.writerow({
                'Position': listing.get('position', 'N/A'),
                'Name': listing.get('name', 'N/A'),
                'Description': listing.get('description', 'N/A'),
                'Image': listing.get('image', 'N/A'),
            })

def main():
    car_type = "Tesla"
    filters = ">30000"  # Customize this filter dynamically if needed
    base_url = 'https://www.kijijiautos.ca/cars/tesla/model-3/#ms=135%3B5&od=down&p=3000%3A35000&sb=rel'

    print(f"Scraping listings for {car_type} with filters {filters}...")
    listings = scroll_and_fetch_listings(base_url)

    if listings:
        print(f"Found {len(listings)} listings. Saving to CSV...")
        file_name = f"{car_type} {filters.replace('>', '_greater_than_')}.csv"
        save_to_csv(listings, file_name)
        print(f"Listings saved to {file_name}.")
    else:
        print("No listings found.")

if __name__ == "__main__":
    main()
