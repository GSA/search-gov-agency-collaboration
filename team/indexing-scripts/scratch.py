import csv
import pandas as pd
import os

filepath = '/Users/jamesmkreft/Documents/GitHub/search-gov-agency-collaboration/team/indexing-scripts/raw/all-links.csv'


# read the file into a Pandas DataFrame
df = pd.read_csv(filepath)

# isolate rows that have 200 status
good_urls = df.loc[df['status'].eq("200 no error")]

# dedup lines
deduped = good_urls.drop_duplicates(subset=["url"], keep="first", inplace=False, ignore_index=False)

# write text file with only URLs from those rows. additional options added to remove extra leading/trailing quotes
deduped['url'].to_csv('processed/' + filename.replace(".csv", "") + ".txt", index=False, header=False, quoting=csv.QUOTE_NONE, quotechar="",  escapechar="\\")

# print message
print(filename + " is finished processing.")

