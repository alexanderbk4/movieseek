#!/usr/bin/env python3
"""
Script to scrape RateYourMusic top films using Selenium with manual verification.
This version requires human interaction for CAPTCHA solving and verification.
"""

import time
import json
import logging
import argparse
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("rym_selenium_scrape.log")
    ]
)
logger = logging.getLogger(__name__)

class RYMSeleniumScraper:
    """Scraper for RateYourMusic film ratings using Selenium with manual verification."""
    
    BASE_URL = "https://rateyourmusic.com/charts/top/film/all-time/separate:live,archival,soundtrack/"
    
    def __init__(self, manual_mode=True):
        self.driver = None
        self.films = []
        # Always run in visible mode for manual verification
        self.headless = False
        self.manual_mode = manual_mode
        self.output_file = f"app/database/rym_films_{datetime.now().strftime('%Y%m%d')}.json"
        self.debug_dir = Path("app/database/rym_debug")
        self.debug_dir.mkdir(parents=True, exist_ok=True)
    
    def initialize(self):
        """Initialize the Selenium WebDriver."""
        options = Options()
        # Never run headless in manual mode
        if self.headless and not self.manual_mode:
            options.add_argument("--headless=new")
        
        # Add common user agent from a real browser
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        
        # Keep extensions enabled in manual mode to allow for any verification plugins
        if not self.manual_mode:
            options.add_argument("--disable-extensions")
        
        # Add additional options to make the browser more stealthy
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--lang=en-US,en;q=0.9")
        options.add_argument("--start-maximized")
        
        # Set window size for easy viewing in manual mode
        window_width = 1200
        window_height = 900
        
        # Disable automation flags
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        })
        
        # Create and configure the WebDriver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        # Set window size to appear more like a real browser and make it easier to interact with
        self.driver.set_window_size(window_width, window_height)
        
        # Additional WebDriver settings to evade detection
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        logger.info("Selenium WebDriver initialized in manual verification mode")
    
    def close(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("WebDriver closed")
    
    def wait_for_user_verification(self, page_num):
        """Wait for user to complete verification and signal readiness to continue."""
        if not self.manual_mode:
            return True
        
        print("\n" + "="*80)
        print(f"MANUAL VERIFICATION REQUIRED FOR PAGE {page_num}")
        print("="*80)
        print("Please complete any CAPTCHA or verification steps in the browser window.")
        print("The page should be fully loaded with film entries visible.")
        print("\nPress Enter when you're ready for the script to continue scraping...", end="")
        input()
        print("Continuing with scraping...")
        return True
    
    def scrape_top_films(self, max_pages: int = 5):
        """Scrape top films from RateYourMusic over multiple pages with manual verification."""
        if not self.driver:
            self.initialize()
        
        for page in range(1, max_pages + 1):
            logger.info(f"Scraping page {page}/{max_pages}...")
            
            try:
                # Construct URL for the current page
                url = self.BASE_URL
                if page > 1:
                    url = f"{self.BASE_URL}{page}/"
                
                logger.info(f"Navigating to: {url}")
                self.driver.get(url)
                
                # Take a screenshot right away
                self.save_screenshot(f"rym_selenium_page_{page}_initial.png")
                
                # In manual mode, wait for user to verify and press Enter
                if self.manual_mode:
                    self.wait_for_user_verification(page)
                else:
                    # Only wait and check for consent in automatic mode
                    # Wait longer initially - site might have cookie consent or other dialogs
                    time.sleep(random.uniform(5, 8))
                    
                    # Check for cookie consent dialog and try to accept it
                    try:
                        cookie_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Agree') or contains(text(), 'Cookie')]")
                        if cookie_buttons:
                            logger.info("Found cookie consent button, attempting to click")
                            cookie_buttons[0].click()
                            time.sleep(2)
                    except Exception as e:
                        logger.warning(f"Error handling cookie consent: {str(e)}")
                    
                    # Wait for the content to load in automatic mode
                    try:
                        WebDriverWait(self.driver, 15).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".page_charts_section_charts_item"))
                        )
                    except TimeoutException:
                        logger.warning(f"Timeout waiting for content on page {page}")
                        # Save the page source for debugging
                        self.save_html(self.driver.page_source, f"rym_selenium_page_{page}_timeout.html")
                        self.save_screenshot(f"rym_selenium_page_{page}_timeout.png")
                        continue
                
                # Get the page source and parse with BeautifulSoup
                html = self.driver.page_source
                
                # Save the first page source as a sample
                if page == 1:
                    self.save_html(html, f"rym_selenium_page_{page}.html")
                
                # Parse the HTML
                films_data = self.parse_films_page(html)
                
                if films_data.get("count", 0) == 0:
                    logger.warning(f"No films found on page {page}")
                    self.save_html(html, f"rym_selenium_page_{page}_no_results.html")
                    self.save_screenshot(f"rym_selenium_page_{page}_no_results.png")
                    
                    if self.manual_mode:
                        print("No films were found on this page. Please check the browser window.")
                        print("Press Enter to continue to the next page, or Ctrl+C to exit...")
                        input()
                    
                    continue
                
                self.films.extend(films_data.get("results", []))
                logger.info(f"Retrieved {films_data.get('count', 0)} films from page {page}")
                
                # Save data after each page for resilience
                self.save_to_json()
                
                if self.manual_mode:
                    print(f"Successfully scraped {films_data.get('count', 0)} films from page {page}.")
                    print(f"Total films collected so far: {len(self.films)}")
                    print(f"Proceed to page {page+1}? (Press Enter to continue, or Ctrl+C to exit)...")
                    input()
                else:
                    # Add a random delay between page requests to mimic human behavior
                    sleep_time = random.uniform(3, 6)
                    logger.info(f"Waiting {sleep_time:.2f} seconds before next request...")
                    time.sleep(sleep_time)
                
            except Exception as e:
                logger.error(f"Error processing page {page}: {str(e)}")
                # Save a screenshot to diagnose the issue
                self.save_screenshot(f"rym_selenium_page_{page}_error.png")
                
                if self.manual_mode:
                    print(f"Error processing page {page}: {str(e)}")
                    print("Press Enter to try the next page, or Ctrl+C to exit...")
                    input()
        
        logger.info(f"Scraping complete. Total films collected: {len(self.films)}")
        if self.manual_mode:
            print(f"\nScraping complete! Total films collected: {len(self.films)}")
            print(f"Data saved to: {self.output_file}")
    
    def parse_films_page(self, html: str) -> Dict[str, Any]:
        """Parse HTML from RateYourMusic to extract film data."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            films = []
            
            # Find film entries in the chart
            film_elements = soup.select('.page_charts_section_charts_item.object_film')
            
            if not film_elements:
                # Fallback if the first selector doesn't find anything
                film_elements = soup.select('.page_charts_section_charts_item')
            
            if not film_elements:
                # Second fallback
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
            return {"error": str(e), "results": [], "count": 0}
    
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
                # One more fallback
                title_elem = element.select_one('a.page_charts_section_charts_item_link.film')
            
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
            filepath = self.debug_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            logger.info(f"Saved raw HTML to {filepath}")
        except Exception as e:
            logger.error(f"Error saving HTML to file: {str(e)}")
    
    def save_screenshot(self, filename: str):
        """Save a screenshot for debugging."""
        try:
            if self.driver:
                filepath = self.debug_dir / filename
                self.driver.save_screenshot(str(filepath))
                logger.info(f"Saved screenshot to {filepath}")
        except Exception as e:
            logger.error(f"Error saving screenshot: {str(e)}")

def main():
    """Main function to run the scraper."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Scrape RateYourMusic top films using Selenium with manual verification.')
    parser.add_argument('--pages', type=int, default=5, help='Number of pages to scrape (default: 5)')
    parser.add_argument('--output', type=str, help='Output filename (default: auto-generated with date)')
    parser.add_argument('--auto', action='store_true', help='Run in automatic mode without manual verification (not recommended)')
    args = parser.parse_args()
    
    # Create the scraper
    scraper = RYMSeleniumScraper(manual_mode=not args.auto)
    
    # Set custom output file if provided
    if args.output:
        scraper.output_file = args.output
    
    try:
        logger.info(f"Starting RateYourMusic scraper for {args.pages} pages")
        if not args.auto:
            print("\n" + "="*80)
            print("MANUAL VERIFICATION MODE ENABLED")
            print("="*80)
            print("This scraper will open a browser window for each page.")
            print("You will need to:")
            print("1. Complete any CAPTCHA or 'I am human' verification")
            print("2. Wait for the page to fully load with film entries visible")
            print("3. Press Enter in this terminal window to scrape the data")
            print("4. Repeat for each page")
            print("\nPress Enter to begin scraping...", end="")
            input()
        else:
            logger.warning("Automatic mode enabled - this may trigger anti-scraping measures")
        
        scraper.scrape_top_films(max_pages=args.pages)
        logger.info(f"Scraping complete. Data saved to {scraper.output_file}")
    except KeyboardInterrupt:
        print("\nScraping interrupted by user. Saving collected data...")
        if scraper.films:
            scraper.save_to_json()
            print(f"Data saved to: {scraper.output_file}")
        else:
            print("No data was collected before interruption.")
    except Exception as e:
        logger.exception(f"Error in main scraper process: {str(e)}")
    finally:
        scraper.close()

if __name__ == "__main__":
    # Run the main function
    main() 