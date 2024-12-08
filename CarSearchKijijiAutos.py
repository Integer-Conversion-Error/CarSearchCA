import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import KeywordCleanup, CSVCleanup, Autotrader_DeepSearch,ShowCars

def fetch_listings_from_page(driver, exclusions):
    """
    Extracts all listings from the current page and filters out those containing exclusion keywords.
    """
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    listings = []
    listing_wrappers = soup.find_all('div', class_='dealer-split-wrapper')

    for wrapper in listing_wrappers:
        try:
            # Extract listing link
            link_element = wrapper.find('a', class_='inner-link')
            link = "https://www.autotrader.ca" + link_element['href'] if link_element else "N/A"

            # Extract title
            title_element = wrapper.find('span', class_='title-with-trim')
            title = title_element.text.strip() if title_element else "N/A"

            # Skip listings with excluded keywords
            if any(keyword.lower() in title.lower() for keyword in exclusions):
                continue

            # Extract price
            price_element = wrapper.find('span', class_='price-amount')
            price = price_element.text.strip() if price_element else "N/A"

            # Extract location
            location_element = wrapper.find('span', class_='proximity-text')
            location = location_element.text.strip() if location_element else "N/A"

            # Extract mileage
            mileage_element = wrapper.find('span', class_='odometer-proximity')
            mileage = mileage_element.text.strip() if mileage_element else "N/A"

            listings.append({
                'Title': title,
                'Price': price,
                'Location': location,
                'Mileage': mileage,
                'Link': link,
            })
        except Exception as e:
            print(f"Error parsing listing: {e}")

    return listings


def scrape_autotrader_listings(url, exclusions, max_pages=5):
    """
    Scrapes up to max_pages listings from Autotrader while filtering out excluded keywords.
    """
    service = Service(executable_path=r"C:\\Users\\togoo\\Desktop\\Self Improvement\\Coding Projects\\CarSearchCA\\chromedriver-win64\\chromedriver.exe")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    all_listings = []
    current_page = 1

    while current_page <= max_pages:
        print(f"Scraping page {current_page}...")

        # Extract and filter listings from the current page
        listings = fetch_listings_from_page(driver, exclusions)
        all_listings.extend(listings)

        # Check if there's a next page and navigate to it
        try:
            next_page_button = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'.page-item[data-page="{current_page + 1}"] a'))
            )
            next_page_button.click()
            current_page += 1
            time.sleep(3)  # Wait for the next page to load
        except Exception as e:
            print("No more pages found or error occurred:", e)
            break

    driver.quit()
    return all_listings


def save_to_csv(listings, file_name):
    """
    Saves listings to a CSV file with the specified file name.
    """
    fieldnames = ['Title', 'Price', 'Location', 'Mileage', 'Link']
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for listing in listings:
            writer.writerow(listing)


def main():
    #make = input("Enter make of car: ") ##TODO: MAKE SEARCHES MORE DYNAMIC
    #model = input("Enter model of car: ")
    #priceMin = input("Enter min price: $")
    #priceMax = input("Enter max price: $")
    search_url = "https://www.autotrader.ca/cars/tesla/model%203/?rcp=15&rcs=0&srt=35&pRng=3000%2C35000&prx=-1&loc=Kanata%2C%20ON&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch"
    #modified_url = "https://www.autotrader.ca/cars/{make}/{model}/?rcp=15&rcs=0&srt=35&pRng={priceMin}%2C{priceMax}&prx=-1&loc=Kanata%2C%20ON&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch"
    print("Scraping listings from Autotrader.ca...")

    # Keywords to exclude from the listings
    exclusions = ["Standard Range", "SR+", "Standard", "RWD"]

    max_pages = 999
    listings = scrape_autotrader_listings(search_url, exclusions, max_pages=max_pages)

    if listings:
        print(f"Found {len(listings)} listings. Saving to CSV...")
        file_name = "Autotrader_Listings_Filtered.csv"
        save_to_csv(listings, file_name)
        print(f"Listings saved to {file_name}.")
        return file_name
    else:
        print("No listings found.")
        return ""

if __name__ == "__main__":
    keyword = "Performance"
    filename = main()
    filename = CSVCleanup.csvmain(filename)
    filename = Autotrader_DeepSearch.deep_search_main(filename)
    filename = KeywordCleanup.keycleanup(keyword,filename)
    ShowCars.showcarsmain(filename)
