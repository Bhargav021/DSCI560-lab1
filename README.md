# Web Scraping Approach

## web_scraper.py

- **Downloads ChromeDriver automatically**: Uses Chrome for Testing API to fetch the correct ChromeDriver version matching the installed Chrome browser
- **Caches driver locally**: Stores downloaded ChromeDriver in `~/.cache/chromedriver` to avoid repeated downloads
- **Uses Selenium with headless Chrome**: Runs Chrome in headless mode (no GUI) to render JavaScript-heavy pages
- **Waits for page load**: Implements WebDriverWait to ensure the page is fully loaded before capturing content
- **Allows JavaScript execution**: Includes a 3-second delay for JavaScript to render dynamic content like market cards
- **Saves raw HTML**: Writes the complete rendered page source to `data/raw_data/web_data.html`
- **Handles Windows platform**: Specifically targets win64 ChromeDriver builds for Windows compatibility

## data_filter.py

- **Parses HTML with BeautifulSoup**: Uses BeautifulSoup4 to parse the saved HTML file efficiently
- **Extracts market data**: Finds all `MarketCard-container` elements and extracts symbol, stock position, and percentage change
- **Extracts news data**: Finds all `LatestNews-item` elements and extracts timestamp, title, and link
- **Normalizes URLs**: Converts relative URLs to absolute URLs by prepending `https://www.cnbc.com`
- **Writes to CSV files**: Uses Python's csv.DictWriter to create structured CSV files with headers
- **Includes fallback logic**: Implements heuristic-based fallbacks if primary CSS selectors don't find elements
- **Deduplicates news items**: Removes duplicate news entries based on link URLs
- **Provides progress feedback**: Prints console messages showing filtering progress and row counts
- **Creates output directories**: Automatically creates `data/processed_data` if it doesn't exist
- **Generates two CSVs**: Produces `market_data.csv` (5 rows) and `news_data.csv` (30 rows)
