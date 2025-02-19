import requests
from bs4 import BeautifulSoup
import time 
import json
import re

#Retry mechanism and data scraping function
def fetch_data_with_retries(url, retries=3, delay=2): 
    """
    Fetches data from a specified URL with retries in case of failure

    """
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1} failed: {e}")
            if attempt < retries - 1: 
                time.sleep(delay * {attempt + 1})  # Wait for a delay before retrying

            else:
                raise


#Funtion to extract data using BeaytifulSoup4 and regular expressions
def extract_data_from_html(html_content):
    """
    Extracts relevant links containing 'python' from HTML content.
    """
    if not html_content:
        raise ValueError("HTML content is invalid or empty") 
   
    soup = BeautifulSoup(html_content, 'html.parser')
    titles = []

    # Regular expression to find all links with 'python' in their text
    for link in soup.find_all('a', href=True):
        title = link.get_text(strip=True)  # Get text and remove extra spaces
        if re.search(r'python', title, re.IGNORECASE):  # Corrected regex
            titles.append(title)

    print("Extracted Titles:", titles)  # Debugging step
    return titles


#function to save data to json file
def save_data_to_json(data, filename="Scraped_data.json"):
    """
    Saves the extrated data to json file
    """
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error svaing data to the file: {e}")
#Url to Scrape
url = 'https://docs.python.org/3/'

#Fetch and extract data
html_content = fetch_data_with_retries(url)
extracted_data = extract_data_from_html(html_content)
save_data_to_json(extracted_data)