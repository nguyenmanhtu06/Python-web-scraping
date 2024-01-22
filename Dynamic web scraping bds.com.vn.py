#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from undetected_chromedriver import Chrome, ChromeOptions
from cfscrape import create_scraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

# Configure the undetected_chromedriver options
options = ChromeOptions()
options.add_argument('--no-sandbox')

# Set the path to the Chromedriver executable
chromedriver_path = 'D:\My data\data\Misc. files\Chromedriver\chromedriver.exe'

# Instantiate an undetected_chromedriver instance with the specified options and executable path
driver = Chrome(options=options, executable_path=chromedriver_path)

# Create a session with cfscrape
session = create_scraper()

base_url = 'https://batdongsan.com.vn/ban-can-ho-chung-cu-ha-noi'
query_params = '?gcn=2.5-ty'

# Open the URL in the Selenium-controlled browser
driver.get(base_url + query_params)

# Solve the Cloudfare challenge using cfscrape
session.cookies.update({c['name']: c['value'] for c in driver.get_cookies()})

# List to store the URLs
urls = []

while True:
    try:
        # Find all the link containers
        containers = driver.find_elements(By.CSS_SELECTOR, 'div.js__card.js__card-full-web')

        # Extract the href links from the containers
        for container in containers:
            link = container.find_element(By.TAG_NAME, 'a')
            href = link.get_attribute('href')
            if href:
                urls.append(href)
                print("Link:", href)
                print("-------------------")

        # Check if there is a "Next" button
        next_button = driver.find_element(By.CSS_SELECTOR, '.re__pagination-icon')
        if 're__disabled' in next_button.get_attribute('class'):
            break

        # Click the "Next" button
        next_button.click()

        # Solve the Cloudfare challenge for the next page
        session.cookies.update({c['name']: c['value'] for c in driver.get_cookies()})

    except StaleElementReferenceException:
        # Handle the StaleElementReferenceException by re-finding the elements
        pass

# Close the browser
driver.quit()

# Set up Selenium Chrome driver
driver = webdriver.Chrome()

# Create an empty dataframe to store the data
df = pd.DataFrame(columns=["District", "Project", "Ngày đăng", "Ngày hết hạn", "Mã tin", "Mức giá", "Đơn giá", "Diện tích"])

# Loop through the URLs
for url in urls:
    # Open the webpage
    driver.get(url)

    # Find the breadcrumb element
    breadcrumb_element = driver.find_element(By.CLASS_NAME, "re__breadcrumb")

    # Get the breadcrumb text
    breadcrumb_text = breadcrumb_element.text

    # Split the breadcrumb text to extract District and Project names
    breadcrumb_parts = breadcrumb_text.split("/")
    district = breadcrumb_parts[-2].strip()
    project = breadcrumb_parts[-1].strip()

    # Find the elements using XPath
    ngay_dang_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Ngày đăng')]/following-sibling::span")
    ngay_het_han_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Ngày hết hạn')]/following-sibling::span")
    ma_tin_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Mã tin')]/following-sibling::span")
    muc_gia_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Mức giá')]/following-sibling::span[@class='value']")
    don_gia_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Mức giá')]/following-sibling::span[@class='ext']")
    dien_tich_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Diện tích')]/following-sibling::span[@class='value']")

    # Get the text content of the elements
    ngay_dang = ngay_dang_element.text if ngay_dang_element else None
    ngay_het_han = ngay_het_han_element.text if ngay_het_han_element else None
    ma_tin = ma_tin_element.text if ma_tin_element else None
    muc_gia = muc_gia_element.text if muc_gia_element else None
    don_gia = don_gia_element.text if don_gia_element else None
    dien_tich = dien_tich_element.text if dien_tich_element else None

    # Append the extracted data to the dataframe
    df = df.append({
        "District": district,
        "Project": project,
        "Ngày đăng": ngay_dang,
        "Ngày hết hạn": ngay_het_han,
        "Mã tin": ma_tin,
        "Mức giá": muc_gia,
        "Đơn giá": don_gia,
        "Diện tích": dien_tich
    }, ignore_index=True)

# Close the browser
driver.quit()

# Print the dataframe
print(df)


# In[ ]:




