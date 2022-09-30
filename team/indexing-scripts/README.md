## Instructions

### Set Up Folder Structure
This script assumes that the folder structure is as follows, with subfolders for `raw` and `processed` in the parent folder that contains this script:

Parent Folder
* scrape_formatter.py
* raw (folder)
    * scrape-output1.csv
    * scrape-output2.csv
* processed (folder)

### Install Dependencies

#### Python
Ensure you have a local version of Python installed, which will allow you to more easily install packages. If you have [Brew](https://treehouse.github.io/installation-guides/mac/homebrew) installed, you can run the following:
```
brew install python@3.9
```

#### Packages
`pip` is the package manager for Python. The packages you'll need to run this script are as follows.
```
pip3.9 install csv
pip3.9 install pandas
pip3.9 install os
```

### Running the Script
1. Ensure your crawl outputs are all in the "raw" folder you've created.
2. Open Terminal on Mac
3. `cd` into the folder that contains your script
4. Run this command: `python3.9 scrape_formatter.py`
5. The script will run and skip over any files that cause issues. Once it's done, you'll be able to see the processed txt files in the `processed` folder.
6. `cd` into the `processed` folder, and run `cat *.txt >> aggregated`
7. Then run `gsplit -b 3500K aggregated aggregated- --additional-suffix=".txt"`
8. The split will create a handful of files (aggregated-aa.txt, aggregated-ab.txt, etc), upload these to the Bulk URL Uploader.
