from bs4 import BeautifulSoup
import pandas as pd
import requests

url = "https://www.carousell.com.my/categories/computers-tech-602/?addRecent=true&canChangeKeyword=true&includeSuggestions=true&search=macbook%20&searchId=ZhwBQl&t-search_query_source=direct_search"


def get_data(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
    except Exception as e:
        print(f"Error: {e}")
        return None


def parse(soup):
    productslist = []

    results = soup.find_all('div', {'class': 'D__o'})  # changes everyday

    for item in results:
        # Use CSS selectors to find elements by class

        price_element = item.select_one('.D_ow')

        if price_element:
            price_selling = price_element.text
        else:
            price_selling = "Price not found"

        print(f'Price: {price_selling}')

        products = {
            'price_selling': price_selling,
        }

        print(products)
        productslist.append(products)

    return productslist


soup = get_data(url)
if soup:
    productslist = parse(soup)
    df = pd.DataFrame(productslist)
    df.to_excel('scraped_data_macbook.xlsx', index=False)

else:
    print("No data to parse.")

print("**scraping complete**")
