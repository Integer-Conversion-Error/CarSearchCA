import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import random

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

def scrape_kijiji_autos(base_url, pages=1, delay=3):
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
    base_url = 'https://www.kijijiautos.ca/cars/'  # Replace with the correct URL for listings
    pages_to_scrape = 2  # Number of pages to scrape
    results = scrape_kijiji_autos(base_url, pages=pages_to_scrape)

    # Save or display results
    if results:
        for i, result in enumerate(results, start=1):
            print(f"{i}. Title: {result['Title']}, Price: {result['Price']}, Link: {result['Link']}")
    else:
        print("No listings found.")

if __name__ == "__main__":
    main()
