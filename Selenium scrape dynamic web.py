#!/usr/bin/env python
# coding: utf-8

# In[3]:


from selenium import webdriver
from selenium.webdriver.common.by import By

# Configure the Selenium webdriver (ensure you have the appropriate driver executable in your PATH)
driver = webdriver.Chrome(executable_path='D:\My data\data\Misc. files\Chromedriver\chromedriver.exe')

url = 'https://batdongsan.com.vn/ban-can-ho-chung-cu-ha-noi?gcn=2.5-ty'

# Open the URL in the Selenium-controlled browser
driver.get(url)

# Find all the <div> elements with class "js__card js__card-full-web"
containers = driver.find_elements(By.CSS_SELECTOR, 'div.js__card.js__card-full-web')

# Iterate over the containers and extract the href links
for container in containers:
    # Find all the <a> elements within the container
    links = container.find_elements(By.TAG_NAME, 'a')

    # Extract the href links
    for link in links:
        href = link.get_attribute('href')
        if href:
            print("Link:", href)
            print("-------------------")

# Close the browser
driver.quit()


# In[15]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure the Selenium webdriver (ensure you have the appropriate driver executable in your PATH)
driver = webdriver.Chrome(executable_path='D:\My data\data\Misc. files\Chromedriver\chromedriver.exe')

base_url = 'https://batdongsan.com.vn/ban-can-ho-chung-cu-ha-noi'
query_params = '?gcn=2.5-ty'

# Open the URL in the Selenium-controlled browser
driver.get(base_url + query_params)

# Find the "Next" button
next_button = driver.find_element(By.CSS_SELECTOR, '.re__pagination-icon')

# Scrape the links from all pages
while True:
    # Find all the link containers
    containers = driver.find_elements(By.CSS_SELECTOR, 'div.js__card.js__card-full-web')

    # Extract the href links from the containers
    for container in containers:
        link = container.find_element(By.TAG_NAME, 'a')
        href = link.get_attribute('href')
        if href:
            print("Link:", href)
            print("-------------------")

    # Check if there is a "Next" button
    if 're__disabled' in next_button.get_attribute('class'):
        break

    # Click the "Next" button
    next_button.click()

    # Wait until the new page finishes loading
    WebDriverWait(driver, 10).until(EC.staleness_of(containers[0]))

# Close the browser
driver.quit()


# In[ ]:




