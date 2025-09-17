# apis/google_api.py
"""Google Search API integration"""

import aiohttp
import logging
from typing import List, Dict
from config.settings import GOOGLE_SEARCH_URL, DEFAULT_MAX_RESULTS

logger = logging.getLogger(__name__)

class GoogleSearchAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.search_engine_id = "YOUR_SEARCH_ENGINE_ID"  # Get from Google Custom Search
        self.base_url = GOOGLE_SEARCH_URL
    
    async def search(self, query: str, num_results: int = DEFAULT_MAX_RESULTS) -> List[Dict]:
        """Search Google for web results"""
        try:
            params = {
                'key': self.api_key,
                'cx': self.search_engine_id,
                'q': query,
                'num': num_results
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [
                            {
                                'title': item.get('title', ''),
                                'link': item.get('link', ''),
                                'snippet': item.get('snippet', ''),
                                'source': 'Google Search'
                            }
                            for item in data.get('items', [])
                        ]
            return []
        except Exception as e:
            logger.error(f"Google Search error: {e}")
            return []