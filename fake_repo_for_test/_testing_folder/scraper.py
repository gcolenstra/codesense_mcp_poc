"""
Web Scraper Module
Modernized for Python 3.9+ with improved error handling and documentation.
"""

from typing import Optional, List, Dict, Any
import requests
from bs4 import BeautifulSoup
import time
import re
from pathlib import Path

BASE_URL = "https://example.com"


def fetch_page(url: str) -> str:
    """
    Fetch a web page with error handling.
    
    Args:
        url: The URL to fetch
        
    Returns:
        str: The HTML content of the page
        
    Raises:
        requests.RequestException: If the request fails
        requests.HTTPError: If the response status is not OK
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to fetch {url}: {e}") from e


def parse_products(html: str) -> List[Dict[str, Any]]:
    """
    Parse product list from HTML with error handling.
    
    Args:
        html: The HTML content to parse
        
    Returns:
        List[Dict[str, Any]]: List of product dictionaries with 'name' and 'price' keys
    """
    soup = BeautifulSoup(html, 'html.parser')
    products = []
    
    # Find all product divs
    product_divs = soup.find_all('div', class_='product')
    
    for div in product_divs:
        try:
            # Extract data with error handling
            name_elem = div.find('h2')
            price_elem = div.find('span', class_='price')
            
            if not name_elem or not price_elem:
                continue
                
            name = name_elem.text.strip()
            price_text = price_elem.text.strip()
            price = float(price_text.replace('$', '').replace(',', ''))
            
            products.append({
                'name': name,
                'price': price
            })
        except (AttributeError, ValueError) as e:
            # Skip products with parsing errors
            continue
    
    return products


def scrape_category(category: str) -> List[Dict[str, Any]]:
    """
    Scrape all products from a category with pagination.
    
    Args:
        category: The category name to scrape
        
    Returns:
        List[Dict[str, Any]]: List of all products in the category
    """
    page = 1
    all_products = []
    
    while True:
        url = f"{BASE_URL}/category/{category}?page={page}"
        try:
            html = fetch_page(url)
            products = parse_products(html)
            
            if not products:
                break
            
            all_products.extend(products)
            page += 1
            time.sleep(1)  # Be nice to the server
        except requests.RequestException:
            # Stop pagination on error
            break
    
    return all_products


def extract_email(text: str) -> Optional[str]:
    """
    Extract email address from text using regex.
    
    Args:
        text: The text to search for an email address
        
    Returns:
        Optional[str]: The extracted email address, or None if not found
    """
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if match:
        return match.group(0)
    return None


def scrape_contact_page() -> Dict[str, Optional[str]]:
    """
    Scrape contact information from the contact page.
    
    Returns:
        Dict[str, Optional[str]]: Dictionary containing 'email', 'phone', and 'address'
    """
    url = f"{BASE_URL}/contact"
    try:
        html = fetch_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find contact info with error handling
        email = extract_email(html)
        
        phone_elem = soup.find('span', class_='phone')
        phone = phone_elem.text.strip() if phone_elem else None
        
        address_elem = soup.find('div', class_='address')
        address = address_elem.text.strip() if address_elem else None
        
        return {
            'email': email,
            'phone': phone,
            'address': address
        }
    except requests.RequestException:
        return {
            'email': None,
            'phone': None,
            'address': None
        }


def download_images(product_urls: List[str]) -> None:
    """
    Download product images from a list of product URLs.
    
    Args:
        product_urls: List of product page URLs to download images from
    """
    # Ensure images directory exists
    images_dir = Path('images')
    images_dir.mkdir(exist_ok=True)
    
    for url in product_urls:
        try:
            html = fetch_page(url)
            soup = BeautifulSoup(html, 'html.parser')
            
            img = soup.find('img', class_='main-image')
            if not img or 'src' not in img.attrs:
                continue
                
            img_url = img['src']
            
            # Download image
            img_response = requests.get(img_url, timeout=30)
            img_response.raise_for_status()
            img_data = img_response.content
            
            # Save with product name from URL
            filename = url.split('/')[-1] + '.jpg'
            filepath = images_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(img_data)
        except (requests.RequestException, AttributeError, KeyError, OSError) as e:
            # Skip images that fail to download
            continue


def search_products(keyword: str) -> List[Dict[str, Any]]:
    """
    Search for products by keyword.
    
    Args:
        keyword: The search keyword
        
    Returns:
        List[Dict[str, Any]]: List of matching products
    """
    url = f"{BASE_URL}/search?q={keyword}"
    try:
        html = fetch_page(url)
        products = parse_products(html)
        return products
    except requests.RequestException:
        return []


def get_product_reviews(product_id: int) -> List[Dict[str, Any]]:
    """
    Get reviews for a specific product.
    
    Args:
        product_id: The product ID to fetch reviews for
        
    Returns:
        List[Dict[str, Any]]: List of review dictionaries with 'rating', 'text', and 'author' keys
    """
    url = f"{BASE_URL}/product/{product_id}/reviews"
    try:
        html = fetch_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        
        reviews = []
        review_divs = soup.find_all('div', class_='review')
        
        for div in review_divs:
            try:
                rating = len(div.find_all('span', class_='star-filled'))
                
                text_elem = div.find('p', class_='review-text')
                author_elem = div.find('span', class_='author')
                
                if not text_elem or not author_elem:
                    continue
                
                text = text_elem.text.strip()
                author = author_elem.text.strip()
                
                reviews.append({
                    'rating': rating,
                    'text': text,
                    'author': author
                })
            except AttributeError:
                # Skip reviews with parsing errors
                continue
        
        return reviews
    except requests.RequestException:
        return []


if __name__ == "__main__":
    products = scrape_category("electronics")
    print(f"Found {len(products)} products")