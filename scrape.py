from profile import password, email, search_term
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup, SoupStrainer
from os.path import exists
import re
import csv
from datetime import datetime


today = datetime.now().strftime("%d:%m:%Y")

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
    f'https://www.facebook.com/marketplace/category/search/?query={search_term}')

driver.implicitly_wait(5)

item_block = SoupStrainer(
    "div", attrs={"aria-label": "Collection of Marketplace items"})

soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=item_block)

# get exact matches
titles = soup.find_all('span', text=re.compile(search_term, re.IGNORECASE))

results = []

for t in titles:
    parent = t.find_parent("a")
    try:
        price = parent.find(string=re.compile('^£\d+$'))[1:]
        i = {}
        i['date'] = today
        i['price'] = int(price)
        i['link'] = 'https://www.facebook.com'+parent['href']
        results.append(i)
    except TypeError as e:
        print(e)

filename = f'{search_term}_data.csv'
is_new = not exists(filename)
with open(filename, 'a', newline='') as f:
    w = csv.DictWriter(f, ['date', 'price', 'link'])
    if is_new:
        w.writeheader()
    for r in results:
        w.writerow(r)

driver.quit()
