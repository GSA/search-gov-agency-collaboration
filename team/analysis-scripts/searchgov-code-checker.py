# import dependencies
# if you are running this for the first time, you may need to 'pip3 install package-name', ex 'pip3 install requests_html'
# check the console when you run it for any other dependencies you may need to install
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import csv
import json
import pandas as pd
import pyarrow
from urllib.parse import urlparse
from urllib.parse import parse_qs

# place the input file (format = xlsx) in a folder named 'input-files' and name it 'market_share_input'
# the file should have one column labeled "site_handle" (can be empty) and one column labeled "urls"
df = pd.read_excel('input-files/market_share_input.xlsx')
marketshare_urls = pd.Series(df.urls.values,index=df.site_handle).to_dict()

# prints the dictionary into the console
print(marketshare_urls)

# set up file
output = []
columns = ( 
    "url",
    "error_status",
    "affiliate",
    "searchbox",
    "customer",
    "http",
    "extracted_affiliate",
    "affiliate_match"

)

# this step iterates through all URLs and outputs the findings to a CSV
with open('output-files/market-share-stats.csv', "w") as csvfile:
    w = csv.DictWriter(csvfile, columns)
    w.writeheader()
    
    for id, url in marketshare_urls.items():
        if url.find("https://") == -1 and url.find("http://") == -1:
            url = "https://" + url
        d = {"url": url, "affiliate": id, "error_status": "OK"}
        
        session = HTMLSession()

        try: 
            # sets up the HTML session object
            #TODO: handle JS based content
            r = session.get(url)
            r.html.render(timeout = 800)
            body = r.text
            soup = BeautifulSoup(body, "html.parser")
            
            # sets the booleans to false to start - only sets to true if evidence is found for it
            d["searchbox"] = False
            d["customer"] = False
            d["http"] = False
            d["affiliate_match"] = False

            # checks to see if any search function is present 
            if body.find("search") > -1:
                    d["searchbox"] = True

            # looking for standard search box string (affiliate=) or DMA (skin-search-input usagov-search-autocomplete)
            if body.find("\"affiliate\"") > -1 or body.find("\"aid\":") > -1 or body.find("skin-search-input usagov-search-autocomplete") > -1 or body.find("affiliate=") > -1:
                d["customer"] = True

            # checks to see if site incorrectly has http in their search bar, which will lead to an error
            if body.find("http://search.usa.gov") > -1:
                d["http"] = True

            # list to store any affiliate IDs found on the pages
            affiliates_found = []

            # extract affiliate value from page - standard implementation
            for item in soup.find_all('input', attrs={"name":"affiliate"}):
                affiliates_found.append(item["value"])
            
            # extract affiliate value from page - DMA implementation
            for script in soup(text=re.compile(r'skinvars')):
                vars = json.loads(script.split("= ")[1].replace(";", ""))
                affiliates_found.append(vars["aid"])
            
            # extract affiliate value from page - direct link implementation
            for link in soup.find_all('a', href=True):
                if link['href'].find("affiliate") > -1:
                    parsed_url = urlparse(link['href'])
                    affiliate = str(parse_qs(parsed_url.query)['affiliate'][0])
                    affiliates_found.append(affiliate)


            # prints affiliate names in a comma-separated list in the output file
            d["extracted_affiliate"] = ", ".join(affiliates_found)

            # check to see if affiliate IDs match
            if d["extracted_affiliate"].find(str(d["affiliate"])) > -1:
                d["affiliate_match"] = True
            
            print("processed: " + str(url))
    
        except Exception as e:
            print("issue processing " + str(url) + " - " + str(e))
            d["error_status"] = "Issue processing site: " + str(e)
        
        session.close()
        
        output.append(d)
        w.writerow(d)
csvfile.close()
