import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv

# URL for the file directory
url = ''

# Send a GET request to fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the file names, links, and modification dates
files = []
base_url = ''  # Base URL for file links
for row in soup.find_all('tr'):
    cols = row.find_all('td')
    if len(cols) > 1:
        link_tag = row.find('a')
        file_name = link_tag.text.strip()  # File name from link text
        file_link = base_url + link_tag.get('href')  # Full link to the file
        last_modified = cols[2].text.strip()  # Date column
        try:
            date_obj = datetime.strptime(last_modified, '%Y-%m-%d %H:%M')
            files.append((file_name, file_link, date_obj))
        except ValueError:
            continue

# Sort files by date
sorted_files = sorted(files, key=lambda x: x[2], reverse=True)

# Write sorted files with links to a CSV file
with open('sorted_files_with_links.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['File Name', 'File Link', 'Last Modified'])
    for file_name, file_link, last_modified in sorted_files:
        writer.writerow([file_name, file_link, last_modified])

print("Files with links have been successfully written to 'sorted_files_with_links.csv'")
