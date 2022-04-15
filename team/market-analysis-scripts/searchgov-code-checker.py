from requests_html import HTMLSession
import csv
import pandas as pd

df = pd.read_excel('input-files/market_share_input.xlsx')
marketshare_urls = pd.Series(df.urls.values,index=df.site_handle).to_dict()

print(marketshare_urls)

# # test array
# # marketshare_urls = ["https://www.sandia.gov/"]

# set up file
output = []
columns = ( 
    "url",
    "connection_status",
    "affiliate",
    "searchbox",
    "customer",
    "http"
)

with open('output-files/market-share-stats.csv', "w") as csvfile:
    w = csv.DictWriter(csvfile, columns)
    w.writeheader()
    
    for id, url in marketshare_urls.items():
        if url.find("https://") == -1 and url.find("http://") == -1:
            url = "https://" + url
        d = {"url": url, "affiliate": id, "connection_status": "OK"}
        

        try: 
            # sets up the HTML session object
            #TODO: handle JS based content
            session = HTMLSession()
            r = session.get(url)
            r.html.render()
            body = r.text
            
            # sets the booleans to false to start - only sets to true if evidence is found for it
            has_searchbox = False
            is_customer = False
            is_http = False

            # search is present 
            if body.find("search") > -1:
                has_searchbox = True

            # looking for standard search box string (affiliate=) or DMA (skin-search-input usagov-search-autocomplete)
            if body.find("\"affiliate\"") > -1 or body.find("\"aid\":") > -1 or body.find("skin-search-input usagov-search-autocomplete") > -1:
                is_customer = True

            # incorrectly has http in their search bar, which will lead to an error
            if body.find("http://search.usa.gov") > -1:
                is_http = True

            d["searchbox"] = has_searchbox
            d["customer"] = is_customer
            d["http"] = is_http

            print("processed: " + url)
        except Exception as e:
            print("issue reaching " + url)
            print(e)
            d["connection_status"] = "Issue reaching site: " + str(e)
        
        output.append(d)
        w.writerow(d)
csvfile.close()