##from io import FileIO
import os, shutil
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import csv
import KeywordCleanup, CSVCleanup, Autotrader_DeepSearch,ShowCars,GetUserQuery

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
            # if any(keyword.lower() in title.lower() for keyword in exclusions):
            #     continue

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


def scrape_autotrader_listings(url, exclusions, max_pages=9999):
    """
    Scrapes up to max_pages listings from Autotrader while filtering out excluded keywords.
    """
    service = Service(executable_path=r"C:\\Users\\togoo\\Desktop\\Self Improvement\\Coding Projects\\CarSearchCA\\chromedriver-win64\\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-webgl")
    options.add_argument("--disable-gpu")  # Disable GPU for better compatibility
    options.add_argument("--blink-settings=imagesEnabled=false") 
    options.add_argument("--log-level=3")  # Fatal-only logs
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Avoid "Controlled by automation" message
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2,  # Block images
        "profile.default_content_setting_values.notifications": 2,  # Block notifications
        "profile.managed_default_content_settings.stylesheets": 2,  # Block CSS
    })
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
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
            time.sleep(6)  # Wait for the next page to load
        except Exception as e:
            print("No more pages found or error occurred:", e)
            break

    driver.quit()
    return all_listings


def save_to_csv(listings, file_name, filedir = "null"):
    """
    Saves listings to a CSV file with the specified file name.
    """
    fieldnames = ['Title', 'Price', 'Location', 'Mileage', 'Link']
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for listing in listings:
            writer.writerow(listing)
    
    if filedir != "null":
        shutil.move(file_name,filedir)


def main():
    search_url,max_pages,exclusions,filters = GetUserQuery.main()

    #modified_url = f"https://www.autotrader.ca/cars/{make}/{model}/?rcp=15&rcs=0&srt=35&pRng={price_min}%2C{price_max}&prx={max_distance}&loc=Kanata%2C%20ON&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch"

    #search_url = modified_url##"https://www.autotrader.ca/cars/tesla/model%203/?rcp=15&rcs=0&srt=35&pRng=3000%2C35000&prx=-1&loc=Kanata%2C%20ON&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch"

    # print("Search URL: ",search_url)
    # print("Exclusion Keywords: ",exclusions)
    listings = scrape_autotrader_listings(search_url, exclusions, max_pages=max_pages)
    datestr = datetime.now().strftime(f"%Y-%m-%d_%H-%M-%S")
    if listings:
        print(f"Found {len(listings)} listings. Saving to CSV...")
        folder_name = f"{filters['make']}_{filters['model']}"
        folder_path = str(os.path.join(os.getcwd(), folder_name))
        file_name = f"{filters['price_min']}-{filters['price_max']}_{filters['min_mileage']}-{filters['max_mileage']}_{filters['min_year']}-{filters['max_year']}_{datestr}.csv"
        # Step 2: Check if the folder exists
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder_name}' created at: {folder_path}")
        else:
            print(f"Folder '{folder_name}' already exists. Files will be added to it.")
        
        #TODO: Individual folders for each car, and reduce redundant CSV files. 
        save_to_csv(listings, file_name,folder_path)
        print(f"Listings saved to {file_name}.")
        return folder_path +"\\" + file_name
    else:
        print("No listings found.")
        return ""

if __name__ == "__main__":
    keyword = "sport"#str(input("Enter Keyword: "))
    filename = main()
    filename = CSVCleanup.csvmain(filename)
    filename = Autotrader_DeepSearch.deep_search_main(filename)
    filename = KeywordCleanup.keycleanup(keyword,filename)
    ShowCars.showcarsmain(filename)
