#!/usr/bin/env python3
"""
Standalone script to scrape RateYourMusic top films and save to a JSON file.
This script operates independently from the database.
"""

import asyncio
import aiohttp
import json
import logging
import os
import time
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, Any, List, Optional
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("rym_scrape.log")
    ]
)
logger = logging.getLogger(__name__)

class RYMScraper:
    """Scraper for RateYourMusic film ratings."""
    
    BASE_URL = "https://rateyourmusic.com/charts/top/film/all-time/separate:live,archival,soundtrack/"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    
    def __init__(self):
        self.session = None
        self.films = []
        self.output_file = f"rym_films_{datetime.now().strftime('%Y%m%d')}.json"
    
    async def initialize(self):
        """Initialize aiohttp session for making requests."""
        if self.session is None:
            self.session = aiohttp.ClientSession(headers={
                "User-Agent": self.USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml",
                "Accept-Language": "en-US,en;q=0.9"
            })
    
    async def close(self):
        """Close the aiohttp session."""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def scrape_top_films(self, max_pages: int = 5):
        """Scrape top films from RateYourMusic over multiple pages."""
        await self.initialize()
        
        for page in range(1, max_pages + 1):
            logger.info(f"Scraping page {page}/{max_pages}...")
            
            try:
                films_data = await self.fetch_page(page)
                if "error" in films_data:
                    logger.error(f"Error on page {page}: {films_data['error']}")
                    continue
                
                self.films.extend(films_data.get("results", []))
                logger.info(f"Retrieved {len(films_data.get('results', []))} films from page {page}")
                
                # Save after each page for resilience
                self.save_to_json()
                
                # Be polite with rate limiting
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"Error processing page {page}: {str(e)}")
        
        logger.info(f"Scraping complete. Total films collected: {len(self.films)}")
    
    async def fetch_page(self, page: int) -> Dict[str, Any]:
        """Fetch and parse a single page of film rankings."""
        try:
            # Construct the URL with proper pagination format
            url = self.BASE_URL
            if page > 1:
                url = f"{self.BASE_URL}{page}/"
            
            logger.info(f"Fetching URL: {url}")
            async with self.session.get(url) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch page {page}: HTTP {response.status}")
                    return {"error": f"HTTP Error: {response.status}"}
                
                html = await response.text()
                
                # Save raw HTML for debugging if needed
                if page == 1:  # Just save first page as sample
                    self.save_html(html, f"rym_page_{page}.html")
                
                # Parse the HTML
                results = self.parse_films_page(html)
                
                # If we couldn't find any films, save the HTML for debugging
                if not results.get("results"):
                    logger.warning(f"No films found on page {page}, saving HTML for debugging")
                    self.save_html(html, f"rym_page_{page}_no_results.html")
                
                return results
                
        except Exception as e:
            logger.error(f"Error fetching page {page}: {str(e)}")
            return {"error": str(e)}
    
    def parse_films_page(self, html: str) -> Dict[str, Any]:
        """Parse HTML from RateYourMusic to extract film data."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            films = []
            
            # Find film entries in the chart
            # Updated selector based on the HTML example
            film_elements = soup.select('.page_charts_section_charts_item.object_film')
            
            if not film_elements:
                # Fallback if the first selector doesn't find anything
                film_elements = soup.select('.page_charts_section_charts_item')
            
            if not film_elements:
                # Second fallback for earlier versions of the site
                film_elements = soup.select('.chart_item_release')
            
            logger.info(f"Found {len(film_elements)} film elements on the page")
            
            for element in film_elements:
                film_data = self.extract_film_data(element)
                if film_data:
                    films.append(film_data)
            
            return {
                "results": films,
                "count": len(films)
            }
        
        except Exception as e:
            logger.error(f"Error parsing HTML: {str(e)}")
            return {"error": str(e)}
    
    def extract_film_data(self, element) -> Optional[Dict[str, Any]]:
        """Extract data for a single film from its HTML element."""
        try:
            # Extract rank
            # Note: RYM doesn't show rank number directly in the HTML samples provided
            # We'll derive it from the list position or extract from ID if available
            element_id = element.get('id', '')
            rank = None
            if element_id and 'page_charts_section_charts_item_' in element_id:
                try:
                    rank = int(element_id.split('_')[-1])
                except ValueError:
                    pass
            
            # Extract title
            title_elem = element.select_one('.page_charts_section_charts_item_title .ui_name_locale_original')
            if not title_elem:
                # Try alternate selector
                title_elem = element.select_one('.page_charts_section_charts_item_link')
            
            if not title_elem:
                return None
            
            title = title_elem.text.strip()
            
            # Extract year/release date
            date_elem = element.select_one('.page_charts_section_charts_item_date span')
            if not date_elem:
                # Try alternate date location
                date_elem = element.select_one('.page_charts_section_charts_item_title_date_compact span')
            
            year = None
            if date_elem:
                date_text = date_elem.text.strip()
                # Extract year from date string (typically in format "DD Month YYYY")
                if date_text:
                    try:
                        # If it's a full date, extract the year portion
                        year_part = date_text.split()[-1]
                        year = int(year_part)
                    except (ValueError, IndexError):
                        # If can't parse, leave as None
                        pass
            
            # Extract rating
            rating_elem = element.select_one('.page_charts_section_charts_item_details_average_num')
            rating = None
            if rating_elem:
                try:
                    rating = float(rating_elem.text.strip())
                except ValueError:
                    pass
            
            # Extract vote count
            votes_elem = element.select_one('.page_charts_section_charts_item_details_ratings .abbr')
            votes = 0
            if votes_elem:
                votes_text = votes_elem.text.strip()
                try:
                    # Handle abbreviated vote counts like "12k"
                    if 'k' in votes_text.lower():
                        votes = int(float(votes_text.lower().replace('k', '')) * 1000)
                    else:
                        votes = int(votes_text.replace(',', ''))
                except ValueError:
                    pass
            
            # Extract genres
            genres = []
            primary_genres = element.select('.page_charts_section_charts_item_genres_primary .genre')
            secondary_genres = element.select('.page_charts_section_charts_item_genres_secondary .genre')
            
            for genre_elem in primary_genres:
                genres.append({
                    "name": genre_elem.text.strip(),
                    "type": "primary"
                })
            
            for genre_elem in secondary_genres:
                genres.append({
                    "name": genre_elem.text.strip(),
                    "type": "secondary"
                })
            
            # Extract URL
            url = None
            link_elem = element.select_one('.page_charts_section_charts_item_title a')
            if link_elem and 'href' in link_elem.attrs:
                url = f"https://rateyourmusic.com{link_elem['href']}"
            
            # Extract poster image
            poster_url = None
            img_elem = element.select_one('.page_charts_section_charts_item_image_link picture img')
            if img_elem and 'src' in img_elem.attrs:
                poster_url = img_elem['src']
                if poster_url.startswith('//'):
                    poster_url = f"https:{poster_url}"
            
            # Generate unique identifier
            identifier = f"{title} ({year})" if year else title
            
            return {
                "rank": rank,
                "title": title,
                "year": year,
                "rating": rating,
                "votes": votes,
                "genres": genres,
                "url": url,
                "poster_url": poster_url,
                "identifier": identifier,
                "scraped_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error extracting film data: {str(e)}")
            return None
    
    def save_to_json(self):
        """Save the collected film data to a JSON file."""
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "source": "RateYourMusic",
                    "url": self.BASE_URL,
                    "scraped_at": datetime.now().isoformat(),
                    "total_films": len(self.films),
                    "films": self.films
                }, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(self.films)} films to {self.output_file}")
        except Exception as e:
            logger.error(f"Error saving to JSON: {str(e)}")
    
    def save_html(self, html: str, filename: str):
        """Save raw HTML to a file for debugging."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
            logger.info(f"Saved raw HTML to {filename}")
        except Exception as e:
            logger.error(f"Error saving HTML to file: {str(e)}")

async def main():
    """Main function to run the scraper."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Scrape RateYourMusic top films.')
    parser.add_argument('--pages', type=int, default=10, help='Number of pages to scrape (default: 10)')
    parser.add_argument('--delay', type=int, default=5, help='Delay in seconds between page requests (default: 5)')
    parser.add_argument('--output', type=str, help='Output filename (default: auto-generated with date)')
    args = parser.parse_args()
    
    scraper = RYMScraper()
    if args.output:
        scraper.output_file = args.output
    
    # Update the delay in the scrape_top_films method
    original_method = scraper.scrape_top_films
    
    async def scrape_with_custom_delay(max_pages=10):
        # Pass the delay to asyncio.sleep in the method
        original_sleep = asyncio.sleep
        
        async def custom_sleep(seconds):
            logger.info(f"Waiting {args.delay} seconds before next request...")
            return await original_sleep(args.delay)
        
        # Replace sleep temporarily
        asyncio.sleep = custom_sleep
        try:
            return await original_method(max_pages)
        finally:
            # Restore original sleep
            asyncio.sleep = original_sleep
    
    # Replace the method
    scraper.scrape_top_films = scrape_with_custom_delay
    
    try:
        logger.info(f"Starting RateYourMusic scraper for {args.pages} pages with {args.delay}s delay")
        await scraper.scrape_top_films(max_pages=args.pages)
        logger.info(f"Scraping complete. Data saved to {scraper.output_file}")
    except Exception as e:
        logger.exception(f"Error in main scraper process: {str(e)}")
    finally:
        await scraper.close()

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main()) 