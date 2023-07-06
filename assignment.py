import requests
from bs4 import BeautifulSoup
import csv

def scrape_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # To Extract product details
    product_url = url
    try:
        product_name = soup.find('span', {'id': 'productTitle'}).text.strip()
    except AttributeError:
        product_name = 'N/A'

    product_price_element = soup.find('span', {'id': 'priceblock_ourprice'})
    product_price = product_price_element.text.strip() if product_price_element else 'N/A'

    rating_element = soup.find('span', {'class': 'a-icon-alt'})
    rating = rating_element.text.strip() if rating_element else 'N/A'

    reviews_count_element = soup.find('span', {'id': 'acrCustomerReviewText'})
    reviews_count = reviews_count_element.text.strip() if reviews_count_element else 'N/A'

    # Extracting additional information
    description_element = soup.find('div', {'id': 'feature-bullets'})
    description = description_element.get_text(separator=' ').strip() if description_element else 'N/A'

    asin_element = soup.find('th', String='ASIN')
    asin = asin_element.find_next('td').text.strip() if asin_element else 'N/A'

    product_description_element = soup.find('div', {'id': 'productDescription'})
    product_description = product_description_element.get_text(separator=' ').strip() if product_description_element else 'N/A'

    manufacturer_element = soup.find('a', {'id': 'bylineInfo'})
    manufacturer = manufacturer_element.text.strip() if manufacturer_element else 'N/A'

    # Writing data to CSV
    product_data = [product_url, product_name, product_price, rating, reviews_count, description, asin, product_description, manufacturer]
    writer.writerow(product_data)



base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
page_count = 1

csv_file = open('product_data.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)
header = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'Description', 'ASIN', 'Product Description', 'Manufacturer']
writer.writerow(header)

while page_count <= 30:  # This number can be chaged as needed
    url = base_url + str(page_count)
    print("Scraping page", page_count)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_list = soup.find_all('div', {'data-component-type': 's-search-result'})

    for product in product_list:
        product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal'})['href']
        scrape_page(product_url)

    page_count += 1

csv_file.close()
