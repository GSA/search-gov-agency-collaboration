from requests_html import HTMLSession
import requests
import csv
import pandas as pd

## update to location of domain input file
df = pd.read_excel('input-files/domains_input.xlsx')

## file needs to list domains in a column labeled "Domain" for this to work
domains = df["Domain"].to_list()
print(domains)

# # test array
# domains = ["https://buildbackbetter.gov/"]

# set up file
columns = ( 
    "domain",
    "connection_status",
    "redirects"
)

with open('output-files/domain-stats.csv', "w") as csvfile:
    w = csv.DictWriter(csvfile, columns)
    w.writeheader()
    
    for domain in domains:
        if domain.find("https://") == -1 and domain.find("http://") == -1:
            domain = "https://" + domain      

        d = {"domain": domain}  

        try: 
            redirects = []
            r = requests.get(domain, timeout=10)
            if len(r.history) < 1:
                d["connection_status"]= str(r.status_code)
            else:
                d["connection_status"]= 301
                h = r.history
                print(h)
                for resp in h:
                    redirects.append(resp.url)
                redirects.append(r.url)
                d["redirects"]= redirects
            
            print("processed: " + domain)
        except Exception as e:
            print("issue reaching " + domain)
            print(e)
            d["connection_status"] = "Issue reaching site: " + str(e)
        w.writerow(d)
csvfile.close()