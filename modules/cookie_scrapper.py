from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import streamlit as st

COOKIE_URL = st.secrets["cookie_url"]


def get_cookie():
    driver = webdriver.Chrome()
    driver.get(COOKIE_URL)

    wait = WebDriverWait(driver, 60)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'onboarding_overviewPipelineProcesses')))

    cookies = driver.get_cookies()

    return cookies
