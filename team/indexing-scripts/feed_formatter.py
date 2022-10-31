import requests
from bs4 import BeautifulSoup
import pandas as pd
import feedparser

## Instructions
## 1. Create "feeds.txt" file in the "indexing-scripts" folder. Ensure it has all RSS feeds you want to process, with each feed on a new line. 
## 2. Ensure all feeds in the file are valid. The script will error if there are spaces in the url, so find-replace " " with "%20".
## 3. Open Terminal, and cd into the /indexing-scripts folder
## 4. Run `python3.9 feed_formatter.py`
## 5. At the end, it will output a file called "rss-feeds.txt" in the "processed" folder. Use Super Admin to bulk upload these URLs.


with open("feeds.txt") as file:
    feeds = [line.rstrip() for line in file]


output = []

for f in feeds:
    d = feedparser.parse(f)

    if len(d.entries) > 0:
        resp = requests.get(f)
        soup = BeautifulSoup(resp.text, 'xml')

        if "www.oge.gov" in f:
            for link in soup.find_all('file'):
                output.append(link.text)
            print("processed: " + f)

        else:
            for link in soup.find_all('link'):
                output.append(link.text)
            print("processed: " + f)
    else:
        print("Invalid Feed: " + f)

with open("processed/rss-feeds.txt", 'w') as fp:
    for item in output:
        fp.write("%s\n" % item)
    print('Done')
