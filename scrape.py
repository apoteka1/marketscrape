from os import link
from profile import password, email, search_term
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup, SoupStrainer
from os.path import exists
import re
import csv
from datetime import datetime

### selenium ###

# block popups, use chrome
option = Options()
option.add_argument('--disable-notifications')
driver = webdriver.Chrome(options=option)

driver.get("https://www.facebook.com/")

driver.implicitly_wait(5)

# allow cookies
accept_cookies = driver.find_element(
    By.XPATH, "//*[@title='Allow essential and optional cookies']")
accept_cookies.click()

# log in
email_input = driver.find_element(By.ID, 'email')
password_input = driver.find_element(By.ID, 'pass')
email_input.send_keys(email)
password_input.send_keys(password)
driver.find_element(By.NAME, 'login').click()

driver.implicitly_wait(5)

# search for thing
driver.get(
    f'https://www.facebook.com/marketplace/category/search/?query={search_term}')

driver.implicitly_wait(5)

### Beautiful Soup ###

# get items list block
item_block = SoupStrainer(
    "div", attrs={"aria-label": "Collection of Marketplace items"})

# make list into soup
soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=item_block)

# get search_term matches, case insensitive (facebook is too relaxed)
titles = soup.find_all(text=re.compile(search_term, re.IGNORECASE))

results = []
today = datetime.now().strftime("%d:%m:%Y")
# loop thru matches
for t in titles:

    # full item block
    parent = t.find_parent("a")
    try:
        # gets price from block => turns in to number
        price = parent.find(string=re.compile('^£\d+$'))[1:]

        # gets important part of href
        # removes unique session number / data, so pandas can weed out duplicates using the href
        item_url_snippet = '/'.join(parent['href'].split('/')[:4])

        # adds dict of data
        i = {}
        i['date'] = today
        i['price'] = int(price)
        i['link_url'] = 'https://www.facebook.com'+item_url_snippet
        results.append(i)

        # prints if weird prices e.g. commas, letters etc
    except TypeError as e:
        print('invalid price format')

### saving data ###

filename = f'{search_term}_data.csv'
is_new = not exists(filename)

with open(filename, 'a', newline='') as f:
    w = csv.DictWriter(f, ['date', 'price', 'link_url'])
    if is_new:
        w.writeheader()
    for r in results:
        w.writerow(r)

driver.quit()
