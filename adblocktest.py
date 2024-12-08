from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
# Path to the chromedriver executable
chromedriver_path = r"C:\\Users\\togoo\\Desktop\\Self Improvement\\Coding Projects\\CarSearchCA\\chromedriver-win64\\chromedriver.exe"

# Path to the ad-blocking .crx file
adblocker_crx_path = r"C:\\Users\\togoo\\Desktop\\Self Improvement\\Coding Projects\\CarSearchCA\\CarSearchCA\\CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_61_2_0.crx"

# Configure Chrome options
chrome_options = Options()
chrome_options.add_extension(adblocker_crx_path)

# Initialize the WebDriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Test by navigating to a website with ads
driver.get("https://www.autotrader.ca/cars/tesla/model%203/?rcp=15&rcs=0&srt=35&pRng=15000%2C35000&prx=-1&loc=Kanata%2C%20ON&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch")

# Perform other actions as needed...
time.sleep(15)
# Close the browser
driver.quit()