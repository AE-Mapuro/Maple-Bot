#%%
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# import numpy
# BeautifulSoup


#%%


#%%
# Can also use sys.argv to pass in character names
chr = "Doop70"
chr = "Asterisker12"
url = "https://maplestory.nexon.net/rankings/overall-ranking/monthly?rebootIndex=0&character_name=%s&search=true" % chr

# This should always be in the output .html
test_str_def = "Rankings"
# This indicates if the selenium test worked
test_str_chr = chr


#%%
# # %%time

chrome_options = Options()
chrome_options.add_argument("--headless")

# These options may or may not help speed this process up
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--ignore-certificate-errors")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-images")
# chrome_options.add_argument("--disable-css")

# Create a headless browser
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
# print(driver.page_source.encode("utf-8"))
soup = BeautifulSoup(driver.page_source.encode("utf-8"), 'html.parser')
driver.quit()

#%%
# Old way of doing this

import warnings
# This is used to suppress the requests warning (See: https://github.com/urllib3/urllib3/issues/3020)
warnings.filterwarnings("ignore", message=".*NotOpenSSLWarning: urllib3 v2.0 only supports OpenSSL 1.1.1+.*")

import requests

# This didnt work because the site also had to load some Javascript
result = requests.get(url)
src = result.content
soup_ = BeautifulSoup(src, 'html.parser')

#%%
# print(soup)
if test_str_def not in soup.get_text():
    print("HTML test failed")
if test_str_chr not in soup.get_text():
    print("Selenium test failed")


# %%
# soup.find_all("div", {"class", "c-rank-list__item-job-image"})


#%%
# # %%time

# Find all table rows
# There should only be two: the table column names and the character data
table_rows = soup.find_all(class_="c-rank-list__table-row")
if len(table_rows) != 2:
    print("Something happend")

# Get the table header
table_headers = [cell.get_text() for cell in table_rows[0].find_all(class_="c-rank-list__table-cell-text")]

table_cells = table_rows[1].find_all(class_="c-rank-list__table-cell-text")

# First, let's check that we have the same number of headers as cells
if len(table_headers) != len(table_cells):
    print("Something happend")

# Next, let's loop through the headers and print corresponding output from the cells based on each header
for header, cell in zip(table_headers, table_cells):
    
    if header == "Rank":
        value = cell.get_text()
    elif header == "Character":
        value = cell.find("img")["src"]
    elif header == "Character Name":
        value = cell.get_text()
    elif header == "World":
        value = cell.find("a")["class"][1]
    elif header == "Job":
        value = cell.find("img")["title"]
    elif header == "Exp Gained":
        value = cell.get_text()
    else: 
        value = 'Invalid header'

    print("%s: %s" % (header, value))




# %%
