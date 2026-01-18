"""
Web scraper for CNBC world page
Fetches the page using Selenium to capture JavaScript-rendered content
and saves it as data/raw_data/web_data.html
"""

from pathlib import Path
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://www.cnbc.com/world/?region=world"


def pgscrape():
    """Scrape CNBC world page using Selenium"""
    # chrome options for Ubuntu
    op = Options()
    # runs without GUI
    op.add_argument('--headless=new')  
    # required for VM env
    op.add_argument('--no-sandbox')  
    # prevents shared memory issues
    op.add_argument('--disable-dev-shm-usage')  
    # consistent viewport size
    op.add_argument('--window-size=1920,1080')  
    
    print("Setting up ChromeDriver...")
    ser = Service(ChromeDriverManager().install())
    
    print("Starting Chrome WebDriver...")
    dv = webdriver.Chrome(service=ser, options=op)
    
    print(f"Loading page: {URL}")
    dv.get(URL)
    
    # waiting for page to load
    wait = WebDriverWait(dv, 15)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "a")))
    time.sleep(3)
    
    # getting page source
    htmlCont = dv.page_source
    
    # quit browser
    dv.quit()
    
    return htmlCont


def savehtml(htmlCont):
    #Save HTML content to file
    outDir = Path(__file__).parent.parent / 'data' / 'raw_data'
    outDir.mkdir(parents=True, exist_ok=True)
    outFile = outDir / 'web_data.html'
    
    outFile.write_text(htmlCont, encoding='utf-8')
    print(f"Saved to: {outFile}")


def main():
    html = pgscrape()
    savehtml(html)
    print("Task 2.3 - Scraping completed successfully!")


if __name__ == '__main__':
    main()

    

