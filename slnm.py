from cgitb import text
from profile import password, email
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup, SoupStrainer
import re
import csv

search_term = 'minilogue XD'

option = Options()
option.add_argument('--disable-notifications')
driver = webdriver.Chrome(options=option)

driver.get("https://www.facebook.com/")

driver.implicitly_wait(5)
accept_cookies = driver.find_element(
    By.XPATH, "//*[@title='Allow essential and optional cookies']")
accept_cookies.click()

email_input = driver.find_element(By.ID, 'email')
password_input = driver.find_element(By.ID, 'pass')

email_input.send_keys(email)
password_input.send_keys(password)

driver.find_element(By.NAME, 'login').click()
driver.implicitly_wait(5)

driver.get(
    'https://www.facebook.com/marketplace/category/search/?query=minilogue%20xd')

driver.implicitly_wait(5)

item_block = SoupStrainer(
    "div", attrs={"aria-label": "Collection of Marketplace items"})

soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=item_block)

# get exact matches
titles = soup.find_all('span', text=re.compile(search_term, re.IGNORECASE))

results = []

for t in titles:
    i = {}
    parent = t.find_parent("a")
    i['link'] = 'https://www.facebook.com'+parent['href']
    i['price'] = int(parent.find(string=re.compile('^£\d+'))[1:])

    results.append(i)


# driver.quit()
