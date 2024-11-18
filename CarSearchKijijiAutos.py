import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import random
import json


def fetch_listings(url):
    """
    Fetches and parses car listings from Kijiji Autos with a randomized user-agent and rate-limiting detection.
    """
    ua = UserAgent()  # Initialize fake user-agent generator
    headers = {
        'User-Agent': ua.random  # Use a random user-agent for each request
    }
    
    response = requests.get(url, headers=headers)
    
    # Check for rate-limiting
    if response.status_code == 429:
        print("Rate limit detected! Waiting before retrying...")
        time.sleep(60)  # Wait for a minute before retrying
        return fetch_listings(url)  # Retry fetching the same URL

    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    print(response.text)
    listings = soup.find_all('div', class_='listing-item')  # Update tag and class as per website structure

    results = []
    for listing in listings:
        try:
            title = listing.find('h2', class_='title').text.strip()
            price = listing.find('span', class_='price').text.strip()
            link = listing.find('a', class_='link')['href']
            full_link = f"https://www.kijijiautos.ca{link}"
            results.append({'Title': title, 'Price': price, 'Link': full_link})
        except AttributeError:
            # Handle cases where an expected element is missing
            continue

    return results

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time

def scroll_and_fetch_listings(url, scroll_pause_time=2, max_scrolls=5):
    """
    Scrolls the page to load more listings and extracts JSON data from the script tag.
    """
    # Set up the WebDriver (Replace with the path to your ChromeDriver)
    driver = webdriver.Chrome(executable_path="C:\\Users\\togoo\\.vscode\\extensions\\ms-python.vscode-pylance-2024.11.2\\dist\\.cache\\local_indices\\a21729d13b1aa9525d79f20a18d1a4cfa56c16c517ddaf5a07cf10a6a6810f70\\chromedriver.json")
    driver.get(url)

    # Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

    # Scroll down to load more listings
    for _ in range(max_scrolls):
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)  # Pause to let new content load

    # Extract the page source after scrolling
    page_source = driver.page_source
    driver.quit()

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    script_tags = soup.find_all('script', {'type': 'application/ld+json'})

    # Extract listings from the relevant JSON script
    for script in script_tags:
        try:
            json_data = json.loads(script.string)
            if json_data.get('@type') == 'ItemList':
                return json_data.get('itemListElement', [])
        except (json.JSONDecodeError, KeyError):
            continue

    return []






def scrape_kijiji_autos(base_url, pages=5, delay=3):
    """
    Scrapes multiple pages of Kijiji Autos listings with random delays and user-agents.
    :param base_url: URL of the Kijiji Autos listings.
    :param pages: Number of pages to scrape.
    :param delay: Maximum time (in seconds) to wait between page requests.
    """
    all_results = []

    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")
        page_url = f"{base_url}?page={page}"  # Modify if pagination URL differs
        listings = fetch_listings(page_url)
        all_results.extend(listings)
        time.sleep(random.uniform(1, delay))  # Random delay to mimic human behavior

    return all_results

def main():
    url = 'https://www.kijijiautos.ca/cars/tesla/model-3/#ms=135%3B5&od=down&p=3000%3A35000&sb=rel'
    listings = scroll_and_fetch_listings(url)

    # Display results
    if listings:
        for i, listing in enumerate(listings, start=1):
            print(f"Listing {i}:")
            print(f"  Position: {listing.get('position', 'N/A')}")
            print(f"  Name: {listing.get('name', 'N/A')}")
            print(f"  Description: {listing.get('description', 'N/A')}")
            print(f"  Image: {listing.get('image', 'N/A')}")
            print("-" * 40)
    else:
        print("No listings found.")

if __name__ == "__main__":
    main()