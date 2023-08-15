# import dependencies
# if you are running this for the first time, you may need to 'pip3 install package-name', ex 'pip3 install requests_html'
# check the console when you run it for any other dependencies you may need to install
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import csv
import json
import pandas as pd
from urllib.parse import urlparse
from urllib.parse import parse_qs

# place the input file (format = xlsx) in a folder named 'input-files' and name it 'typeahead_checker_input'
# the file should have one column labeled "urls"
df = pd.read_excel('input-files/typeahead_checker_input.xlsx')
typeahead_targets = pd.Series(df.urls.values).to_dict()

# prints the dictionary into the console
print(typeahead_targets)

# set up file
output = []
columns = ( 
    "url",
    "error_status",
    "remote_loader_present",
    "remote.loader_over_http"

)

# this step iterates through all URLs and outputs the findings to a CSV
with open('output-files/typeahead_checher_results.csv', "w") as csvfile:
    w = csv.DictWriter(csvfile, columns)
    w.writeheader()
    
    for id, url in typeahead_targets.items():
        if url.find("https://") == -1 and url.find("http://") == -1:
            url = "https://" + url
        d = {"url": url, "error_status": "OK"}
        
        session = HTMLSession()

        try: 
            # sets up the HTML session object
            r = session.get(url)
            r.html.render(timeout = 800)
            body = r.text
            soup = BeautifulSoup(body, "html.parser")
            
            # sets the booleans to false to start - only sets to true if evidence is found for it
            d["remote_loader_present"] = False
            d["remote.loader_over_http"] = False

            # looking for remote.loader.js
            if body.find("remote.loader") > -1:
                d["remote_loader_present"] = True

            # checks to see if site incorrectly has http in their search bar, which will lead to an error
            if body.find("http://search.usa.gov") > -1:
                d["remote.loader_over_http"] = True
            
            print("processed: " + str(url))
    
        except Exception as e:
            print("issue processing " + str(url) + " - " + str(e))
            d["error_status"] = "Issue processing site: " + str(e)
        
        session.close()
        
        output.append(d)
        w.writerow(d)
csvfile.close()
