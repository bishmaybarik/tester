import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin, urlparse, parse_qs
import time
from unidecode import unidecode  # Import unidecode for transliteration

# Base URL for constructing full URLs
base_url = "put/your/base/url/here"

# List of state URLs (should be provided externally)
state_urls = [
    # Add state URLs dynamically
]

# Function to fetch and parse a webpage into a BeautifulSoup object
def get_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        time.sleep(1)  # Add a delay to prevent server overload
        return BeautifulSoup(response.text, 'html.parser')  # Use response.text for proper decoding
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to extract links and names from a table
def extract_links(soup):
    if soup is None:
        return []
    table = soup.find('table', id='t1')
    if not table:
        return []
    rows = table.find_all('tr')[4:]
    links = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 2:
            link_tag = cells[1].find('a')
            if link_tag:
                name = unidecode(link_tag.text.strip())
                href = link_tag['href']
                full_url = urljoin(base_url, href)
                links.append((name, full_url))
    return links

# Function to scrape table data from a page
def scrape_table_data(soup, state, state_id, fy, district, block):
    if soup is None:
        return []
    table = soup.find('table', id='t1')
    if not table:
        return []
    rows = table.find_all('tr')[4:]
    data = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 14:
            panchayat = unidecode(cells[1].text.strip())
            monthly_data = [cell.text.strip() for cell in cells[2:14]]
            data.append({
                'State': state,
                'State ID': state_id,
                'FY': fy,
                'District': district,
                'Block': block,
                'Panchayat': panchayat,
                'April': monthly_data[0],
                'May': monthly_data[1],
                'June': monthly_data[2],
                'July': monthly_data[3],
                'August': monthly_data[4],
                'September': monthly_data[5],
                'October': monthly_data[6],
                'November': monthly_data[7],
                'December': monthly_data[8],
                'January': monthly_data[9],
                'February': monthly_data[10],
                'March': monthly_data[11]
            })
    return data

# Main function to orchestrate the scraping
def main():
    all_data = []
    for state_url in state_urls:
        parsed_url = urlparse(state_url)
        query_params = parse_qs(parsed_url.query)
        state = query_params.get('state_name', ['Unknown'])[0]
        state_id = query_params.get('state_code', ['Unknown'])[0]
        fy = query_params.get('fin_year', ['Unknown'])[0]
        
        print(f"Processing state: {state}")
        state_soup = get_soup(state_url)
        if not state_soup:
            print(f"Failed to fetch state page for {state}. Skipping.")
            continue
        
        district_links = extract_links(state_soup)
        print(f"Found {len(district_links)} districts in {state}.")
        
        for district_name, district_url in district_links:
            print(f"Processing district: {district_name} in {state}")
            district_soup = get_soup(district_url)
            if not district_soup:
                print(f"Skipping {district_name} due to fetch error.")
                continue
            
            block_links = extract_links(district_soup)
            print(f"Found {len(block_links)} blocks in {district_name}.")
            
            for block_name, block_url in block_links:
                print(f"Processing block: {block_name} in {district_name}, {state}")
                block_soup = get_soup(block_url)
                if not block_soup:
                    print(f"Skipping {block_name} due to fetch error.")
                    continue
                
                panchayat_data = scrape_table_data(block_soup, state, state_id, fy, district_name, block_name)
                all_data.extend(panchayat_data)
                print(f"Collected data for {len(panchayat_data)} panchayats in {block_name}.")
    
    if all_data:
        df = pd.DataFrame(all_data)
        output_file = "put/yourr/output/path/here.csv"
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Data saved to {output_file} with {len(df)} rows.")
    else:
        print("No data collected.")

if __name__ == "__main__":
    main()
