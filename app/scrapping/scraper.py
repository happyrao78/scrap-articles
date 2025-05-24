import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging
import time

logger = logging.getLogger(__name__)

class WebScraper:
    """Web scraper for extracting content from various sites."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_articles(self, url: str, limit: int = 5) -> List[Dict[str, str]]:
        """
        Scrape articles from a given URL.
        
        Args:
            url: URL to scrape from
            limit: Maximum number of articles to scrape
        
        Returns:
            List of dictionaries containing article data
        """
        try:
            if "quotes.toscrape.com" in url:
                return self._scrape_quotes_to_scrape(url, limit)
            elif "news.ycombinator.com" in url:
                return self._scrape_hacker_news(url, limit)
            else:
                return self._scrape_generic(url, limit)
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return []
    
    def _scrape_quotes_to_scrape(self, url: str, limit: int) -> List[Dict[str, str]]:
        """Scrape quotes from quotes.toscrape.com"""
        articles = []
        response = self.session.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        quotes = soup.find_all('div', class_='quote')[:limit]
        
        for quote in quotes:
            text = quote.find('span', class_='text').get_text()
            author = quote.find('small', class_='author').get_text()
            tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
            
            articles.append({
                'title': f"Quote by {author}",
                'author': author,
                'content': f"{text}\n\nTags: {', '.join(tags)}",
                'source_url': url
            })
            
        return articles
    
    def _scrape_hacker_news(self, url: str, limit: int) -> List[Dict[str, str]]:
        """Scrape articles from Hacker News"""
        articles = []
        response = self.session.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all('tr', class_='athing')[:limit]
        
        for row in rows:
            title_element = row.find('span', class_='titleline')
            if title_element:
                title_link = title_element.find('a')
                if title_link:
                    title = title_link.get_text().strip()
                    link = title_link.get('href', '')
                    
                    # Get additional info from next row
                    next_row = row.find_next_sibling('tr')
                    author = "Unknown"
                    if next_row:
                        author_element = next_row.find('a', class_='hnuser')
                        if author_element:
                            author = author_element.get_text()
                    
                    articles.append({
                        'title': title,
                        'author': author,
                        'content': f"Title: {title}\nLink: {link}",
                        'source_url': url
                    })
        
        return articles
    
    def _scrape_generic(self, url: str, limit: int) -> List[Dict[str, str]]:
        """Generic scraper for other websites"""
        articles = []
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find article-like content
            potential_articles = (
                soup.find_all('article') +
                soup.find_all('div', class_=lambda x: x and 'post' in x.lower()) +
                soup.find_all('div', class_=lambda x: x and 'article' in x.lower())
            )[:limit]
            
            for i, article in enumerate(potential_articles):
                title_element = (
                    article.find('h1') or 
                    article.find('h2') or 
                    article.find('h3') or
                    article.find('title')
                )
                
                title = title_element.get_text().strip() if title_element else f"Article {i+1}"
                
                # Extract text content
                for script in article(["script", "style"]):
                    script.extract()
                
                content = article.get_text().strip()[:2000]  # Limit content length
                
                articles.append({
                    'title': title,
                    'author': "Unknown",
                    'content': content,
                    'source_url': url
                })
                
        except Exception as e:
            logger.error(f"Error in generic scraping: {str(e)}")
            
        return articles

def scrape_articles(url: str, limit: int = 5) -> List[Dict[str, str]]:
    """
    Main function to scrape articles from a URL.
    
    Args:
        url: URL to scrape from
        limit: Maximum number of articles to scrape
    
    Returns:
        List of dictionaries containing article data
    """
    scraper = WebScraper()
    return scraper.scrape_articles(url, limit)