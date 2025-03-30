#!/usr/bin/env python3
"""
Script to open a browser for RateYourMusic and manually save HTML for later processing.
This completely manual approach avoids triggering anti-bot measures.
"""

import time
import json
import logging
import argparse
import os
from pathlib import Path
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RYMBrowser:
    """Simple browser for RateYourMusic manual scraping."""
    
    BASE_URL = "https://rateyourmusic.com/charts/top/film/all-time/separate:live,archival,soundtrack/"
    
    def __init__(self):
        self.driver = None
        self.output_dir = Path("app/database/rym_manual")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def initialize(self):
        """Initialize a normal Chrome browser."""
        options = Options()
        
        # Create a temporary user data directory just for this session
        temp_profile_dir = self.output_dir / "chrome_profile"
        temp_profile_dir.mkdir(exist_ok=True)
        options.add_argument(f"user-data-dir={temp_profile_dir}")
        logger.info(f"Using temporary Chrome profile at {temp_profile_dir}")
        
        # Don't use automation flags
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Create and configure the WebDriver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        
        logger.info("Browser initialized")
    
    def close(self):
        """Close the browser."""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("Browser closed")
    
    def open_page(self, page_num=1):
        """Open a specific page of RateYourMusic charts."""
        if not self.driver:
            self.initialize()
        
        # Construct URL for the current page
        url = self.BASE_URL
        if page_num > 1:
            url = f"{self.BASE_URL}{page_num}/"
        
        logger.info(f"Opening page {page_num}: {url}")
        self.driver.get(url)
    
    def save_current_page(self):
        """Save the current page source to a file."""
        page_source = self.driver.page_source
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_file = self.output_dir / f"rym_page_{timestamp}.html"
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(page_source)
        
        print(f"Saved current page to: {html_file}")
        return html_file

def main():
    """Main function to run the browser."""
    parser = argparse.ArgumentParser(description='Open browser for manual RateYourMusic scraping.')
    parser.add_argument('--page', type=int, default=1, help='Page number to open (default: 1)')
    args = parser.parse_args()
    
    browser = RYMBrowser()
    
    try:
        browser.initialize()
        browser.open_page(args.page)
        
        print("\n" + "="*80)
        print("MANUAL BROWSER MODE")
        print("="*80)
        print("Browser window opened to RateYourMusic charts page.")
        print("Instructions:")
        print("1. Complete any verification steps in the browser")
        print("2. Wait for the page to fully load with film entries")
        print("3. Type 'save' to save the current page HTML")
        print("4. Type 'open X' to open page number X")
        print("5. Type 'quit' to exit")
        print("="*80)
        
        while True:
            command = input("\nEnter command (save/open/quit): ").strip().lower()
            
            if command == 'quit':
                break
            elif command == 'save':
                html_file = browser.save_current_page()
                print(f"HTML saved to {html_file}")
            elif command.startswith('open '):
                try:
                    page_num = int(command.split(' ')[1])
                    browser.open_page(page_num)
                    print(f"Opened page {page_num}")
                except (ValueError, IndexError):
                    print("Invalid command. Use 'open X' where X is a page number.")
            else:
                print("Unknown command. Valid commands: save, open X, quit")
    
    except KeyboardInterrupt:
        print("\nBrowser session interrupted by user.")
    except Exception as e:
        logger.exception(f"Error: {str(e)}")
    finally:
        input("\nPress Enter to close the browser...")
        browser.close()

if __name__ == "__main__":
    main() 