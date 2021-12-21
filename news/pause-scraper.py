"""
This will do the scraping of the news with urllib3 and beautifulsoup
"""

"""
Stop trying to scrape google news for now.
"""


import urllib3
from bs4 import BeautifulSoup
http = urllib3.PoolManager()

# make request with urllib3
r = http.request_encode_body(
    "GET", "https://news.google.com/topstories?hl=zh-HK&gl=HK&ceid=HK:zh-Hant")
d = r.data

# parsing the html
parsed = BeautifulSoup(d, "html.parser")
links = parsed.find_all(class_="DY5T1d")

hrefs = []

for link in links:
    dotLink = link.get("href")
    fullLink = dotLink.replace(".", "https://news.google.com/")
    print(fullLink)
