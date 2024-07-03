from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def setup_driver():
    options = Options()
    # options.add_argument("--headless")  # Temporarily disable headless mode for debugging
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    service = Service('/opt/homebrew/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    return driver
