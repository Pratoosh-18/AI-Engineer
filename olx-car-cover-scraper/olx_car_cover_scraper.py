#!/usr/bin/env python3
"""
OLX Car Cover Search Scraper
----------------------------
This script scrapes car cover listings from OLX India and saves the results to a file.
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import random
import argparse
from datetime import datetime


class OlxScraper:
    def __init__(self, base_url="https://www.olx.in"):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        
    def get_search_results(self, query, max_pages=3):
        """Fetches search results for the given query"""
        all_listings = []
        
        for page in range(1, max_pages + 1):
            url = f"{self.base_url}/items/q-{query}"
            if page > 1:
                url += f"?page={page}"
                
            print(f"Scraping page {page} - URL: {url}")
            
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                listings = self._extract_listings(soup)
                
                if not listings:
                    print(f"No more listings found on page {page}. Stopping.")
                    break
                    
                all_listings.extend(listings)
                
                # Add a random delay between requests to be respectful to the server
                time.sleep(random.uniform(1.5, 3.5))
                
            except Exception as e:
                print(f"Error scraping page {page}: {str(e)}")
                break
                
        return all_listings
    
    def _extract_listings(self, soup):
        """Extracts listing information from the page"""
        listings = []
        
        # OLX listings are typically in a container with product cards
        # Adjust these selectors based on the actual structure of the page
        cards = soup.select("li[data-aut-id='itemBox']")
        
        if not cards:
            # Try alternative selectors if the main one doesn't work
            cards = soup.select(".EIR5N")
        
        for card in cards:
            try:
                # Extract key information
                title_elem = card.select_one("[data-aut-id='itemTitle']")
                price_elem = card.select_one("[data-aut-id='itemPrice']")
                location_elem = card.select_one("[data-aut-id='item-location']")
                date_elem = card.select_one("[data-aut-id='item-date']")
                
                # Get link to listing detail page
                link_elem = card.select_one("a")
                link = link_elem.get('href') if link_elem else None
                
                # Fix relative URLs
                if link and not link.startswith(('http://', 'https://')):
                    link = self.base_url + link if not link.startswith('/') else self.base_url + link
                
                # Get image URL if available
                img_elem = card.select_one("img")
                img_url = img_elem.get('src') if img_elem else None
                
                listing = {
                    "title": title_elem.text.strip() if title_elem else "N/A",
                    "price": price_elem.text.strip() if price_elem else "N/A",
                    "location": location_elem.text.strip() if location_elem else "N/A",
                    "date_posted": date_elem.text.strip() if date_elem else "N/A",
                    "link": link if link else "N/A",
                    "image_url": img_url if img_url else "N/A"
                }
                
                listings.append(listing)
                
            except Exception as e:
                print(f"Error extracting listing info: {str(e)}")
                continue
                
        return listings
    
    def save_to_json(self, listings, filename):
        """Save listings to a JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "search_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_results": len(listings),
                "listings": listings
            }, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(listings)} listings to {filename}")
    
    def save_to_csv(self, listings, filename):
        """Save listings to a CSV file"""
        if not listings:
            print("No listings to save")
            return
            
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = listings[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(listings)
        print(f"Saved {len(listings)} listings to {filename}")


def main():
    parser = argparse.ArgumentParser(description='Scrape car cover listings from OLX India')
    parser.add_argument('--query', default='car-cover', help='Search query (default: car-cover)')
    parser.add_argument('--pages', type=int, default=3, help='Maximum number of pages to scrape (default: 3)')
    parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Output file format (default: json)')
    args = parser.parse_args()
    
    # Replace spaces with hyphens in the query for the URL
    query = args.query.replace(' ', '-')
    
    scraper = OlxScraper()
    listings = scraper.get_search_results(query, max_pages=args.pages)
    
    if not listings:
        print("No listings found.")
        return
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"olx_{query}_{timestamp}.{args.format}"
    
    if args.format == 'json':
        scraper.save_to_json(listings, filename)
    else:
        scraper.save_to_csv(listings, filename)


if __name__ == "__main__":
    main()