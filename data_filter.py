"""
parse data/raw_data/web_data.html and produce two CSVs in data/processed_data:
market_data.csv with columns: marketCard_symbol, marketCard_stockPosition, marketCard-changePct
news_data.csv with columns: LatestNews-timestamp, title, link
"""

from pathlib import Path
from bs4 import BeautifulSoup
import csv
import re


def safetext(el):
    # extract text from element safely
    if el:
        return el.get_text(separator=' ', strip=True)
    return ''


def extractmarket(s):
    # extract market data from MarketCard elements
    print("Filtering market data fields...")
    mrows = []
    
    # find all MarketCard containers
    cards = s.find_all('a', class_=lambda x: x and 'MarketCard-container' in x)
    
    for card in cards:
        # extract symbol
        syelem = card.find('span', class_='MarketCard-symbol')
        sym = safetext(syelem)
        
        # extract stock position (price)
        poselem = card.find('span', class_='MarketCard-stockPosition')
        pos = safetext(poselem)
        
        # extract change percentage
        pctelem = card.find('span', class_='MarketCard-changesPct')
        cngpct = safetext(pctelem)
        
        # only add if we have at least a symbol
        if sym:
            mrows.append({
                'marketCard_symbol': sym,
                'marketCard_stockPosition': pos,
                'marketCard-changePct': cngpct
            })
    
    # if no data found, return empty row - fallback
    if not mrows:
        mrows = [{'marketCard_symbol': '', 'marketCard_stockPosition': '', 'marketCard-changePct': ''}]
    
    return mrows


def extractlatestnews(s):
    # find Latest News section and extract timestamp, title, link for each news item
    print("Filtering news data fields...")
    news = []
    
    # find all LatestNews-item elements
    newsitems = s.find_all('li', class_=lambda x: x and 'LatestNews-item' in x)
    
    for item in newsitems:
        # extract timestamp
        t = item.find('time', class_='LatestNews-timestamp')
        timestamp = safetext(t)
        
        # extract headline link
        headelem = item.find('a', class_='LatestNews-headline')
        if headelem:
            title = safetext(headelem)
            href = headelem.get('href', '')
            
            # make sure the link is absolute
            if href and not href.startswith('http'):
                href = 'https://www.cnbc.com' + href
            
            if title and href:
                news.append({
                    'LatestNews-timestamp': timestamp,
                    'title': title,
                    'link': href
                })
    
    return news


def writecsv(path, fieldnames, rows):
    # write data to CSV file
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def main():
    # set up paths
    base = Path(__file__).resolve().parents[1]
    rawfile = base / 'data' / 'raw_data' / 'web_data.html'
    procdir = base / 'data' / 'processed_data'
    procdir.mkdir(parents=True, exist_ok=True)
    marketcsv = procdir / 'market_data.csv'
    newscsv = procdir / 'news_data.csv'
    
    # read HTML file
    html = rawfile.read_text(encoding='utf-8')
    s = BeautifulSoup(html, 'html.parser')
    
    # extract data
    print("\nStarting data extraction...")
    marketrows = extractmarket(s)
    print(f"Storing market data ({len(marketrows)} rows)...")
    
    news = extractlatestnews(s)
    print(f"Storing news data ({len(news)} rows)...")
    
    # write CSVs
    writecsv(marketcsv, ['marketCard_symbol', 'marketCard_stockPosition', 'marketCard-changePct'], marketrows)
    print(f"Market CSV created: {marketcsv}")
    
    writecsv(newscsv, ['LatestNews-timestamp', 'title', 'link'], news)
    print(f"News CSV created: {newscsv}")
    
    print("\nData filtering complete!")


if __name__ == '__main__':
    main()
