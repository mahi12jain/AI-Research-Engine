# apis/news_api.py
"""News API integration"""

import aiohttp
import logging
from typing import List, Dict
from config.settings import NEWS_API_URL, DEFAULT_NEWS_RESULTS

logger = logging.getLogger(__name__)

class NewsAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = NEWS_API_URL
    
    async def search(self, query: str) -> List[Dict]:
        """Search for news articles"""
        try:
            params = {
                'apiKey': self.api_key,
                'q': query,
                'sortBy': 'publishedAt',
                'pageSize': DEFAULT_NEWS_RESULTS,
                'language': 'en'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/everything", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [
                            {
                                'title': article.get('title', ''),
                                'description': article.get('description', ''),
                                'url': article.get('url', ''),
                                'publishedAt': article.get('publishedAt', ''),
                                'source': article.get('source', {}).get('name', 'Unknown'),
                                'category': 'news'
                            }
                            for article in data.get('articles', [])
                        ]
            return []
        except Exception as e:
            logger.error(f"News API error: {e}")
            return []   