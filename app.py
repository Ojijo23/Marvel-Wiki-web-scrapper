import requests
import csv
from bs4 import  BeautifulSoup


url = "https://en.wikipedia.org/wiki/Marvel_Comics"

response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
    print   ("Page fetched succesfully!")
else:
    print("Failed to fetch page. Status Code:", response.status_code)
    

soup =  BeautifulSoup(html_content, 'html.parser')

page_title = soup.title.text
print("Page  Title:", page_title)

# Extract the first paragraph of the page
intro_paragraph = soup.find('p').text
print("Introduction Paragraph:\n", intro_paragraph)

# Find all main section headings (<h2> tags)
headings = soup.find_all('h2')

print("Main section Headings: ")
for heading in headings:
    #extract and clean the text from each <h2> tag
    heading_text = heading.text.strip()
    print(heading_text)

# Locate the first table on the page
table = soup.find('table')

# Open csv file to write the extracted table data
with open('marvel_table_data.csv', mode='w',  newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Loop through each row in the table
    for row in table.find_all('tr'):
        #Get header cells (if they exist), else get regular cells
        headers = [header.text.strip() for header in row.find_all('th')] 
        cells = [cell.text.strip() for cell in row.find_all('td')]
        
        # If the row has headers, write them to the CSV  as the header row
        if headers:
            writer.writerow(headers)
        else:
            # Otherwise, write the cells to the CSV as a regular row
            writer.writerow(cells)
print(f"Table data saved to 'marvel_table_data.csv'")


# Find all tables on the page
tables = soup.find_all('table')

# Loop througth each table and save it as a separate file
for index, table in enumerate (tables, start=1):
    filename = f'marvel_table_{index}.csv' #Unique filename for each  table.
    
    with  open(filename, mode='w',  newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Loop through each row  in the current table
        for row in table.find_all('tr'):
            headers = [header.text.strip() for header in row.find_all('th')]
            cells = [cell.text.strip() for cell in row.find_all('td')]
            
            if headers:
                writer.writerow(headers)
            else:
                writer.writerow(cells)
                
print(f"Table {index} data saved to '{filename}'")


# List to store all links
links = []

# Find all <a> tags on the page
for link in soup.find_all('a', href=True):
    url = link['href']
    
    # Check if the link is absolute or relative
    if url.startswith('http'):
        links.append(url) # Absolute link
    else:
        # Prepend the base url to make it an absolute URL
        links.append("https://en.wikipedia.org" + url) 
        
# Print the links or save them to a file
print("Extracted Links:")
for link in links:
    print(link)
    
with  open('marvel_links.txt', mode='w', newline='', encoding='utf-8') as file:
    for link in links:
        file.write(link +"\n")
        
# List to store all image URLs
images = []

# Find all  <img> tags on the page
for img in soup.find_all('img', src=True):
    img_url = img ['src']
    
    # Check if the image URL is absolute or relative
    if img_url.startswith("http"):
        images.append(img_url) #absolute URL
    else:
        # Prepend the base URL for relative URLs
        images.append("https:" + img_url)

# Print th eimage URLs or save them to a file
print("Extracted Image Urls:")
for img_url in images:
    print(img_url)
    
# Optionally, save image URLs to a text file
with open("marvel_images.txt", "w", encoding="utf-8") as file:
    for img_url in images:
        file.write(img_url + "\n")        
