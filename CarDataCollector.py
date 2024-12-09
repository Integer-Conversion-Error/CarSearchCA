from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import time

def get_makes_from_autotrader():
    """
    Fetches all car makes from the AutoTrader.ca website.

    Args:
        headless (bool): Run the browser in headless mode (default: True).

    Returns:
        list: A list of car makes available on AutoTrader.ca.
    """
    # Setup Chrome WebDriver options
    options = Options()
    # if headless:
    #options.add_argument("--headless")  # Run browser in headless mode
    #options.add_argument("--enable-unsafe-webgpu")
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

    # Initialize WebDriver
    service = Service(
        executable_path=r"C:\\Users\\togoo\\Desktop\\Self Improvement\\Coding Projects\\CarSearchCA\\chromedriver-win64\\chromedriver.exe",
        service_args=["--log-path=chromedriver.log"]
    )
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open AutoTrader.ca
        driver.get("https://www.autotrader.ca")
        time.sleep(3)  # Wait for the page to load

        # Locate the rfMakes dropdown and fetch all makes
        makes_dropdown = driver.find_element(By.ID, "rfMakes")
        makes_options = makes_dropdown.find_elements(By.TAG_NAME, "option")
        makes = [option.text.strip() for option in makes_options if option.text.strip()]
        return makes

    except Exception as e:
        print(f"An error occurred while fetching makes: {e}")
        return []

    finally:
        # Close the WebDriver
        driver.quit()

def get_models_from_autotrader(manufacturer, headless=True):
    """
    Fetches all car models for a given manufacturer from AutoTrader.ca.

    Args:
        manufacturer (str): The name of the carmaker (e.g., "Tesla").
        headless (bool): Run the browser in headless mode (default: True).

    Returns:
        list: A list of car models available for the given manufacturer.
    """
    # Setup Chrome WebDriver options
    options = Options()
    if headless:
        options.add_argument("--headless")  # Run browser in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU for better compatibility
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Initialize WebDriver
    service = Service(executable_path=r"C:\\Users\\togoo\\Desktop\\Self Improvement\\Coding Projects\\CarSearchCA\\chromedriver-win64\\chromedriver.exe")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    try:
         # Open AutoTrader.ca
        driver.get("https://www.autotrader.ca")
        time.sleep(3)  # Wait for the page to load

        # Select the manufacturer from the dropdown
        makes_dropdown = driver.find_element(By.ID, "rfMakes")
        makes_options = makes_dropdown.find_elements(By.TAG_NAME, "option")
        
        # Find the manufacturer option
        manufacturer_value = None
        for option in makes_options:
            if option.text.strip().lower() == manufacturer.lower():
                manufacturer_value = option.get_attribute("value")
                break

        if not manufacturer_value:
            print(f"Manufacturer '{manufacturer}' not found in the dropdown.")
            return []

        makes_dropdown.send_keys(manufacturer_value)
        time.sleep(2)

        # Fetch the list of models from the updated dropdown
        models_dropdown = driver.find_element(By.ID, "rfModel")  # Adjust this ID based on AutoTrader's page
        models_options = models_dropdown.find_elements(By.TAG_NAME, "option")
        
        # Extract and return model names
        models = [option.text.strip() for option in models_options if option.text.strip()]
        return models
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    finally:
        # Close the WebDriver
        driver.quit()

# # Example usage
# if __name__ == "__main__":
#     manufacturer = "Tesla"
#     allmanufacturers = get_makes_from_autotrader()
#     print(allmanufacturers)
#     #models = get_models_from_autotrader(manufacturer, headless=True)
#     #print(f"Models for {manufacturer}: {models}")


def get_specs_from_api(make, model, trim, year):
    #TODO: Add API implementation, either from Edmunds https://developer.edmunds.com/api-documentation/vehicle/spec_engine_and_transmission/v2/
    #or https://github.com/rOpenGov/mpg or https://www.fueleconomy.gov/feg/ws/index.shtml
    
    return 0


def extract_car_companies(html_content):
    """
    Extracts car company names from the provided HTML content.
    
    Args:
        html_content (str): A string containing the HTML to parse.
    
    Returns:
        list: A list of car company names.
    """
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all <li> elements within the <ul> with the specified class
    li_elements = soup.select('ul.list-options li')
    
    # Extract the text content of each <li> tag, ignoring the count in parentheses
    car_companies = [li.a.text.split('(')[0].strip().lower() for li in li_elements if li.a]
    
    return car_companies

# companyhtml = r'<ul class="list-options dropdown-menu nav-pills nav-stacked" id="rfMakes"><li data-dropdownvalue="Acura"><a>Acura <span class="option-count">(93)</span></a></li><li data-dropdownvalue="Alfa Romeo"><a>Alfa Romeo <span class="option-count">(34)</span></a></li><li data-dropdownvalue="American Motors (AMC)"><a>American Motors (AMC) <span class="option-count">(2)</span></a></li><li data-dropdownvalue="Aston Martin"><a>Aston Martin <span class="option-count">(2)</span></a></li><li data-dropdownvalue="Audi"><a>Audi <span class="option-count">(298)</span></a></li><li data-dropdownvalue="Bentley"><a>Bentley <span class="option-count">(5)</span></a></li><li data-dropdownvalue="BMW"><a>BMW <span class="option-count">(519)</span></a></li><li data-dropdownvalue="Buick"><a>Buick <span class="option-count">(308)</span></a></li><li data-dropdownvalue="Cadillac"><a>Cadillac <span class="option-count">(227)</span></a></li><li data-dropdownvalue="Chevrolet"><a>Chevrolet <span class="option-count">(924)</span></a></li><li data-dropdownvalue="Chrysler"><a>Chrysler <span class="option-count">(202)</span></a></li><li data-dropdownvalue="Dodge"><a>Dodge <span class="option-count">(316)</span></a></li><li data-dropdownvalue="Dodge or Ram"><a>Dodge or Ram <span class="option-count">(930)</span></a></li><li data-dropdownvalue="Edsel"><a>Edsel <span class="option-count">(1)</span></a></li><li data-dropdownvalue="Ferrari"><a>Ferrari <span class="option-count">(2)</span></a></li><li data-dropdownvalue="Fiat"><a>Fiat <span class="option-count">(13)</span></a></li><li data-dropdownvalue="Ford"><a>Ford <span class="option-count">(1518)</span></a></li><li data-dropdownvalue="Genesis"><a>Genesis <span class="option-count">(40)</span></a></li><li data-dropdownvalue="GMC"><a>GMC <span class="option-count">(511)</span></a></li><li data-dropdownvalue="Honda"><a>Honda <span class="option-count">(1012)</span></a></li><li data-dropdownvalue="Hummer"><a>Hummer <span class="option-count">(2)</span></a></li><li data-dropdownvalue="Hyundai"><a>Hyundai <span class="option-count">(1620)</span></a></li><li data-dropdownvalue="Infiniti"><a>Infiniti <span class="option-count">(119)</span></a></li><li data-dropdownvalue="Jaguar"><a>Jaguar <span class="option-count">(44)</span></a></li><li data-dropdownvalue="Jeep"><a>Jeep <span class="option-count">(717)</span></a></li><li data-dropdownvalue="Kia"><a>Kia <span class="option-count">(643)</span></a></li><li data-dropdownvalue="Lamborghini"><a>Lamborghini <span class="option-count">(3)</span></a></li><li data-dropdownvalue="Lancia"><a>Lancia <span class="option-count">(1)</span></a></li><li data-dropdownvalue="Land Rover"><a>Land Rover <span class="option-count">(166)</span></a></li><li data-dropdownvalue="Lexus"><a>Lexus <span class="option-count">(107)</span></a></li><li data-dropdownvalue="Lincoln"><a>Lincoln <span class="option-count">(35)</span></a></li><li data-dropdownvalue="Maserati"><a>Maserati <span class="option-count">(33)</span></a></li><li data-dropdownvalue="Mazda"><a>Mazda <span class="option-count">(599)</span></a></li><li data-dropdownvalue="Mercedes-AMG"><a>Mercedes-AMG <span class="option-count">(9)</span></a></li><li data-dropdownvalue="Mercedes-Benz"><a>Mercedes-Benz <span class="option-count">(512)</span></a></li><li data-dropdownvalue="Mercury"><a>Mercury <span class="option-count">(2)</span></a></li><li data-dropdownvalue="MG"><a>MG <span class="option-count">(2)</span></a></li><li data-dropdownvalue="MINI"><a>MINI <span class="option-count">(146)</span></a></li><li data-dropdownvalue="Mitsubishi"><a>Mitsubishi <span class="option-count">(301)</span></a></li><li data-dropdownvalue="Nissan"><a>Nissan <span class="option-count">(1381)</span></a></li><li data-dropdownvalue="Oldsmobile"><a>Oldsmobile <span class="option-count">(3)</span></a></li><li data-dropdownvalue="Plymouth"><a>Plymouth <span class="option-count">(1)</span></a></li><li data-dropdownvalue="Polestar"><a>Polestar <span class="option-count">(1)</span></a></li><li data-dropdownvalue="Pontiac"><a>Pontiac <span class="option-count">(11)</span></a></li><li data-dropdownvalue="Porsche"><a>Porsche <span class="option-count">(81)</span></a></li><li data-dropdownvalue="Ram"><a>Ram <span class="option-count">(617)</span></a></li><li data-dropdownvalue="Rolls-Royce"><a>Rolls-Royce <span class="option-count">(1)</span></a></li><li data-dropdownvalue="Saturn"><a>Saturn <span class="option-count">(1)</span></a></li><li data-dropdownvalue="Scion"><a>Scion <span class="option-count">(5)</span></a></li><li data-dropdownvalue="smart"><a>smart <span class="option-count">(2)</span></a></li><li data-dropdownvalue="Subaru"><a>Subaru <span class="option-count">(277)</span></a></li><li data-dropdownvalue="Suzuki"><a>Suzuki <span class="option-count">(4)</span></a></li><li data-dropdownvalue="Tesla"><a>Tesla <span class="option-count">(50)</span></a></li><li data-dropdownvalue="Toyota"><a>Toyota <span class="option-count">(842)</span></a></li><li data-dropdownvalue="Volkswagen"><a>Volkswagen <span class="option-count">(851)</span></a></li><li data-dropdownvalue="Volvo"><a>Volvo <span class="option-count">(46)</span></a></li></ul>'

# print(extract_car_companies(companyhtml))