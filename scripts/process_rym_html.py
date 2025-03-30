#!/usr/bin/env python3
"""
Script to process manually saved HTML files from RateYourMusic and extract film data.
Run this after using open_rym_browser.py to save HTML files.
"""

import json
import logging
import argparse
import glob
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RYMHTMLProcessor:
    """Processor for RateYourMusic film ratings HTML files."""
    
    def __init__(self, input_dir="app/database/rym_manual", output_file=None):
        self.input_dir = Path(input_dir)
        if not output_file:
            output_file = f"app/database/rym_films_{datetime.now().strftime('%Y%m%d')}.json"
        self.output_file = output_file
        self.films = []
    
    def process_all_html_files(self):
        """Process all HTML files in the input directory."""
        html_files = list(self.input_dir.glob("*.html"))
        if not html_files:
            logger.warning(f"No HTML files found in {self.input_dir}")
            return
        
        html_files.sort()  # Process in filename order
        
        logger.info(f"Found {len(html_files)} HTML files to process")
        for html_file in html_files:
            logger.info(f"Processing {html_file}")
            self.process_html_file(html_file)
        
        logger.info(f"Processed {len(html_files)} files, extracted {len(self.films)} films")
        self.save_to_json()
    
    def process_html_file(self, filepath):
        """Process a single HTML file and extract film data."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()
            
            films_data = self.parse_films_page(html)
            if films_data.get("count", 0) > 0:
                # Check for duplicates and add only new films
                existing_identifiers = {film["identifier"] for film in self.films}
                new_films = []
                for film in films_data.get("results", []):
                    if film["identifier"] not in existing_identifiers:
                        new_films.append(film)
                        existing_identifiers.add(film["identifier"])
                
                self.films.extend(new_films)
                logger.info(f"Extracted {len(new_films)} new films from {filepath.name}")
            else:
                logger.warning(f"No films found in {filepath.name}")
        except Exception as e:
            logger.error(f"Error processing {filepath}: {str(e)}")
    
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
            
            logger.info(f"Found {len(film_elements)} film elements in the HTML")
            
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
                    "url": "https://rateyourmusic.com/charts/top/film/all-time/separate:live,archival,soundtrack/",
                    "scraped_at": datetime.now().isoformat(),
                    "total_films": len(self.films),
                    "films": self.films
                }, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(self.films)} films to {self.output_file}")
            print(f"Successfully saved {len(self.films)} films to {self.output_file}")
        except Exception as e:
            logger.error(f"Error saving to JSON: {str(e)}")

def main():
    """Main function to process HTML files."""
    parser = argparse.ArgumentParser(description='Process RateYourMusic HTML files to extract film data.')
    parser.add_argument('--input-dir', type=str, default="app/database/rym_manual", 
                       help='Directory containing HTML files (default: app/database/rym_manual)')
    parser.add_argument('--output', type=str, default=None,
                       help='Output JSON file (default: app/database/rym_films_YYYYMMDD.json)')
    args = parser.parse_args()
    
    processor = RYMHTMLProcessor(input_dir=args.input_dir, output_file=args.output)
    
    try:
        print(f"Processing HTML files from {args.input_dir}...")
        processor.process_all_html_files()
    except Exception as e:
        logger.exception(f"Error processing HTML files: {str(e)}")

if __name__ == "__main__":
    main() 