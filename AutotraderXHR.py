import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to fetch and parse JSON-LD content using Selenium
def fetch_and_parse_json_ld():
    url = "https://www.autotrader.ca/cars/tesla/model%203/?rcp=50&rcs=0&srt=35&pRng=3000%2C35000&prx=-1&loc=Kanata%2C%20ON&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver_path = r"C:\\Users\\togoo\\Desktop\\Self Improvement\\Coding Projects\\CarSearchCA\\chromedriver-win64\\chromedriver.exe"  # Replace with the path to your ChromeDriver executable
    driver = webdriver.Chrome(service=Service(driver_path), options=options)

    try:
        driver.get(url)

        # Wait for the network to be idle
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Allow time for dynamic content to load
        time.sleep(5)

        # Extract JSON-LD content
        json_ld_elements = driver.find_elements(By.XPATH, "//script[@type='application/ld+json']")
        parsed_data = []

        for element in json_ld_elements:
            json_content = element.get_attribute("innerHTML")
            try:
                data = json.loads(json_content)
                parsed_data.append(data)
            except json.JSONDecodeError:
                print("Error parsing JSON-LD content")

        # Save parsed data to a file
        with open("parsed_json_ld_content.json", "w", encoding="utf-8") as file:
            json.dump(parsed_data, file, indent=4)

        print("Parsed JSON-LD content saved to 'parsed_json_ld_content.json'")

    except Exception as e:
        print(f"Error fetching data: {e}")

    finally:
        driver.quit()

# Function to read JSON-LD file and extract specific fields from "ListItem"
def get_list_item_details_from_file():
    try:
        with open("parsed_json_ld_content.json", "r", encoding="utf-8") as file:
            content = json.load(file)

        list_item_details = []

        # Traverse through JSON content to find "ListItem" entries
        def extract_items(data):
            previtems = []
            if isinstance(data, dict):
                if data.get("@type") == "ListItem" and "item" in data:
                    item = data["item"]
                    if "@type" in item and "@id" in item and "name" in item:
                        
                        if "new, used & certified pre-owned" not in item["name"] and item["@type"] != "SearchResultsPage" and item not in previtems:
                            list_item_details.append({
                                "@type": item["@type"],
                                "@id": item["@id"],
                                "name": item["name"]
                            })
                        previtems.append(item)
                for key, value in data.items():
                    extract_items(value)
            elif isinstance(data, list):
                for entry in data:
                    extract_items(entry)

        extract_items(content)
        return list_item_details

    except Exception as e:
        print(f"Error reading or processing file: {e}")
        return []

if __name__ == "__main__":
    fetch_and_parse_json_ld()
    list_item_details = get_list_item_details_from_file()
    print("List Item Details:", json.dumps(list_item_details, indent=4))
    print(f"{len(list_item_details)} listings")
