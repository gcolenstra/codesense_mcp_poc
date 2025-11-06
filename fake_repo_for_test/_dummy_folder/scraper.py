"""
Web Scraper Module
Needs better error handling and modernization
"""

import requests
from bs4 import BeautifulSoup
import time
import re

BASE_URL = "https://example.com"

def fetch_page(url):
    """Fetch a web page - no error handling!"""
    response = requests.get(url)
    return response.text

def parse_products(html):
    """Parse product list from HTML"""
    soup = BeautifulSoup(html, 'html.parser')
    products = []
    
    # Find all product divs
    product_divs = soup.find_all('div', class_='product')
    
    for div in product_divs:
        # Extract data without error handling
        name = div.find('h2').text
        price_text = div.find('span', class_='price').text
        price = float(price_text.replace('$', '').replace(',', ''))
        
        products.append({
            'name': name,
            'price': price
        })
    
    return products

def scrape_category(category):
    """Scrape all products from a category"""
    page = 1
    all_products = []
    
    while True:
        url = BASE_URL + "/category/" + category + "?page=" + str(page)
        html = fetch_page(url)
        products = parse_products(html)
        
        if len(products) == 0:
            break
        
        all_products.extend(products)
        page = page + 1
        time.sleep(1)  # Be nice to the server
    
    return all_products

def extract_email(text):
    """Extract email from text - simple regex"""
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if match:
        return match.group(0)
    return None

def scrape_contact_page():
    """Scrape contact information"""
    url = BASE_URL + "/contact"
    html = fetch_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find contact info
    email = extract_email(html)
    phone = soup.find('span', class_='phone').text
    address = soup.find('div', class_='address').text
    
    return {
        'email': email,
        'phone': phone,
        'address': address
    }

def download_images(product_urls):
    """Download product images - no error handling"""
    for url in product_urls:
        html = fetch_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        
        img = soup.find('img', class_='main-image')
        img_url = img['src']
        
        # Download image
        img_data = requests.get(img_url).content
        
        # Save with product name from URL
        filename = url.split('/')[-1] + '.jpg'
        with open('images/' + filename, 'wb') as f:
            f.write(img_data)

def search_products(keyword):
    """Search for products"""
    url = BASE_URL + "/search?q=" + keyword
    html = fetch_page(url)
    products = parse_products(html)
    return products

def get_product_reviews(product_id):
    """Get reviews for a product"""
    url = BASE_URL + "/product/" + str(product_id) + "/reviews"
    html = fetch_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    
    reviews = []
    review_divs = soup.find_all('div', class_='review')
    
    for div in review_divs:
        rating = len(div.find_all('span', class_='star-filled'))
        text = div.find('p', class_='review-text').text
        author = div.find('span', class_='author').text
        
        reviews.append({
            'rating': rating,
            'text': text,
            'author': author
        })
    
    return reviews

if __name__ == "__main__":
    products = scrape_category("electronics")
    print("Found %d products" % len(products))