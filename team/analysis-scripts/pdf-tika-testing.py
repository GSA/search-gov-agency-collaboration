# Import Tika Parser (pip3 install tika)
# You will also need to have Java 8 installed
from tika import parser

# Set the URL you want to parse here. This is a sample from the Search.gov site.
pdf_url ="https://search.gov/files/2021-year-in-review.pdf"

# Parses the PDF into the parsed_pdf object
parsed_pdf = parser.from_file(pdf_url)

# Saves metadata and PDF content
metadata = parsed_pdf['metadata']
content = parsed_pdf['content']

# Printing metadata and content
print("Metadata: \n")
print(metadata)

print("\nContent: ")
print(content)
