# services/news_service.py
"""News service for fetching latest news articles"""

import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class NewsService:
    """Service for fetching news articles from News API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
    
    async def get_news(self, topic: str, limit: int = 10, days_back: int = 7) -> List[Dict]:
        """Get news articles related to a topic"""
        if not self.api_key:
            logger.warning("News API key not configured")
            return []
        
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Format dates for API
            from_date = start_date.strftime('%Y-%m-%d')
            to_date = end_date.strftime('%Y-%m-%d')
            
            # API parameters
            params = {
                'q': topic,
                'from': from_date,
                'to': to_date,
                'sortBy': 'relevancy',
                'pageSize': min(limit, 100),  # API limit is 100
                'language': 'en'
            }
            
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/everything"
                
                async with session.get(
                    url,
                    headers=self.headers,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        articles = data.get('articles', [])
                        
                        # Process and clean articles
                        processed_articles = []
                        for article in articles[:limit]:
                            processed_article = {
                                'title': article.get('title', 'No title'),
                                'description': article.get('description', 'No description'),
                                'url': article.get('url', ''),
                                'source': article.get('source', {}).get('name', 'Unknown'),
                                'publishedAt': article.get('publishedAt', ''),
                                'content': article.get('content', '')
                            }
                            processed_articles.append(processed_article)
                        
                        logger.info(f"Fetched {len(processed_articles)} news articles for topic: {topic}")
                        return processed_articles
                    
                    else:
                        error_text = await response.text()
                        logger.error(f"News API error {response.status}: {error_text}")
                        return []
                        
        except asyncio.TimeoutError:
            logger.error("News API timeout")
            return []
        except Exception as e:
            logger.error(f"News API exception: {e}")
            return []
    
    async def get_top_headlines(self, category: str = "technology", limit: int = 10) -> List[Dict]:
        """Get top headlines from a specific category"""
        if not self.api_key:
            logger.warning("News API key not configured")
            return []
        
        try:
            params = {
                'category': category,
                'country': 'us',
                'pageSize': min(limit, 100),
                'language': 'en'
            }
            
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/top-headlines"
                
                async with session.get(
                    url,
                    headers=self.headers,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        articles = data.get('articles', [])
                        
                        # Process articles
                        processed_articles = []
                        for article in articles[:limit]:
                            processed_article = {
                                'title': article.get('title', 'No title'),
                                'description': article.get('description', 'No description'),
                                'url': article.get('url', ''),
                                'source': article.get('source', {}).get('name', 'Unknown'),
                                'publishedAt': article.get('publishedAt', ''),
                                'content': article.get('content', '')
                            }
                            processed_articles.append(processed_article)
                        
                        logger.info(f"Fetched {len(processed_articles)} top headlines")
                        return processed_articles
                    
                    else:
                        error_text = await response.text()
                        logger.error(f"News API error {response.status}: {error_text}")
                        return []
                        
        except Exception as e:
            logger.error(f"News API exception: {e}")
            return []
    
    async def test_connection(self) -> bool:
        """Test News API connection"""
        try:
            # Try to get top headlines as a test
            articles = await self.get_top_headlines(limit=1)
            return len(articles) > 0
        except Exception as e:
            logger.error(f"News API test failed: {e}")
            return False
    
    def format_news_for_display(self, articles: List[Dict]) -> str:
        """Format news articles for display"""
        if not articles:
            return "No news articles found."
        
        formatted = []
        for i, article in enumerate(articles, 1):
            formatted.append(f"{i}. {article['title']}")
            if article['description']:
                formatted.append(f"   {article['description']}")
            formatted.append(f"   Source: {article['source']}")
            formatted.append(f"   Published: {article['publishedAt']}")
            if article['url']:
                formatted.append(f"   URL: {article['url']}")
            formatted.append("")
        
        return "\n".join(formatted)
    
    async def search_news_by_keywords(self, keywords: List[str], limit: int = 10) -> List[Dict]:
        """Search news by multiple keywords"""
        if not self.api_key:
            return []
        
        try:
            # Combine keywords with OR operator
            query = " OR ".join(keywords)
            return await self.get_news(query, limit)
        except Exception as e:
            logger.error(f"Keyword search failed: {e}")
            return []
    
    def get_news_summary(self, articles: List[Dict]) -> str:
        """Generate a summary of news articles"""
        if not articles:
            return "No recent news available."
        
        # Extract key themes from titles
        titles = [article['title'] for article in articles if article.get('title')]
        
        if not titles:
            return "No news titles available for summary."
        
        # Simple summary based on common words
        all_words = []
        for title in titles:
            words = title.lower().split()
            all_words.extend(words)
        
        # Count word frequency (simple approach)
        word_count = {}
        for word in all_words:
            if len(word) > 3:  # Skip short words
                word_count[word] = word_count.get(word, 0) + 1
        
        # Get most common words
        common_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:5]
        
        summary = f"Recent news covers {len(articles)} articles. Key themes include: "
        summary += ", ".join([word for word, count in common_words])
        
        return summary
