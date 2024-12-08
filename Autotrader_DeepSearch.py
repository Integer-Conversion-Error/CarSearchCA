import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def extract_details_with_webdriver(driver, url):
    """
    Extracts highlights, specifications, and features from a car's detail page using WebDriver.
    """
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "highlightWidget"))
        )

        # Extract highlights
        highlights = []
        try:
            highlight_elements = driver.find_elements(By.CSS_SELECTOR, "#hl-card-body .list-text")
            highlights = [element.text.strip() for element in highlight_elements]
        except Exception:
            pass

        # Extract specifications
        specifications = {}
        try:
            spec_elements = driver.find_elements(By.CSS_SELECTOR, "#sl-card-body .list-item")
            for element in spec_elements:
                key = element.find_element(By.CSS_SELECTOR, ".col-xs-6").text.strip()
                value = element.find_element(By.CSS_SELECTOR, "strong").text.strip()
                specifications[key] = value
        except Exception:
            pass

        # Extract features
        features = []
        try:
            feature_elements = driver.find_elements(By.CSS_SELECTOR, "#fo-card-body .list-text")
            features = [element.text.strip() for element in feature_elements]
        except Exception:
            pass

        return {
            "Highlights": "; ".join(highlights),
            "Specifications": "; ".join([f"{key}: {value}" for key, value in specifications.items()]),
            "Features": "; ".join(features),
        }
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return {
            "Highlights": "N/A",
            "Specifications": "N/A",
            "Features": "N/A",
        }


def count_rows_in_csv(file_path):
    """
    Counts the number of rows in a CSV file, excluding the header.

    Parameters:
    - file_path (str): The path to the CSV file.

    Returns:
    - int: The number of rows in the CSV file (excluding the header).
    """
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header row
        row_count = sum(1 for _ in reader)
    return row_count

def convert_seconds_to_hms(seconds):
    """
    Converts a given number of seconds into hours, minutes, and seconds.

    Parameters:
    - seconds (int): The total number of seconds.

    Returns:
    - tuple: A tuple containing hours, minutes, and seconds.
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    print(f"ETA: {hours}h, {minutes}m, {remaining_seconds:.2f}s")

def update_csv_with_details(input_csv, output_csv, driver_path):
    """
    Reads an input CSV, adds additional information from links using WebDriver, and writes to an output CSV.
    """
    chromedriver_path = r"C:\\Users\\togoo\\Desktop\\Self Improvement\\Coding Projects\\CarSearchCA\\chromedriver-win64\\chromedriver.exe"

    adblocker_crx_path = r"C:\\Users\\togoo\\Desktop\\Self Improvement\\Coding Projects\\CarSearchCA\\CarSearchCA\\CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_61_2_0.crx"

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_extension(adblocker_crx_path)

    # Initialize the WebDriver
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    totalrows = count_rows_in_csv(input_csv)
    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)

    # Add new columns
    fieldnames = reader.fieldnames + ["Highlights", "Specifications", "Features"]
    updated_rows = []
    sum_elapsed = []
    #start_time = time.time()
    for row in rows:
        start_time = time.time()
        link = row.get("Link")
        if link and link.startswith("http"):
            print(f"Processing link: {link}")
            details = extract_details_with_webdriver(driver, link)
            row.update(details)
        else:
            print(f"Invalid or missing link for row: {row}")
            row.update({"Highlights": "N/A", "Specifications": "N/A", "Features": "N/A"})
        updated_rows.append(row)
        time.sleep(2)
        elapsed_time = time.time() - start_time
        sum_elapsed.append(elapsed_time)
        avgtime = 0
        for etime in sum_elapsed:
            avgtime += etime
        
        avgtime /= float(len(sum_elapsed))
        avgtime *= totalrows
        print(f"Elapsed time: {elapsed_time:.4f} seconds")
        convert_seconds_to_hms(avgtime)
        totalrows -= 1
        # Optional delay to avoid being flagged by the site
        #time.sleep(0.5)

    # Close the driver
    driver.quit()

    # Write updated data to output CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)


def deep_search_main(input_csv = "Autotrader_Listings_Filtered.csv"):
    output_csv = input_csv.split(".")[0]+"_DeepSearch.csv"  # Output file name
    driver_path = r"C:\\Users\\togoo\\Desktop\\Self Improvement\\Coding Projects\\CarSearchCA\\chromedriver-win64\\chromedriver.exe"
    
    print("Updating CSV with additional details from links using WebDriver...")
    update_csv_with_details(input_csv, output_csv, driver_path)
    print(f"Updated data saved to {output_csv}")
    return output_csv


if __name__ == "__main__":
    deep_search_main()
