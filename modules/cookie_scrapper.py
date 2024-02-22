from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import streamlit as st

COOKIE_URL = st.secrets["cookie_url"]

def get_cookie():
    # Configure Selenium to run Chrome in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without a UI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Setup WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(COOKIE_URL)

        # Wait for a specific element to ensure the page has loaded
        wait = WebDriverWait(driver, 60)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'onboarding_overviewPipelineProcesses')))

        cookies = driver.get_cookies()
        return cookies

    finally:
        # Ensure the driver quits regardless of success/failure
        driver.quit()