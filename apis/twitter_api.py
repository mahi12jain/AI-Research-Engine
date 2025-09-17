# apis/twitter_api.py
"""Twitter/X API integration"""

import aiohttp
import logging
from typing import List, Dict
from config.settings import TWITTER_API_URL, DEFAULT_SOCIAL_RESULTS

logger = logging.getLogger(__name__)

class TwitterAPI:
    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token
        self.base_url = TWITTER_API_URL
        self.headers = {"Authorization": f"Bearer {bearer_token}"}
    
    async def search(self, query: str) -> List[Dict]:
        """Search Twitter for recent tweets"""
        try:
            params = {
                'query': query,
                'max_results': DEFAULT_SOCIAL_RESULTS,
                'tweet.fields': 'created_at,public_metrics,author_id'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/tweets/search/recent",
                    headers=self.headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [
                            {
                                'text': tweet.get('text', ''),
                                'created_at': tweet.get('created_at', ''),
                                'metrics': tweet.get('public_metrics', {}),
                                'source': 'Twitter'
                            }
                            for tweet in data.get('data', [])
                        ]
            return []
        except Exception as e:
            logger.error(f"Twitter API error: {e}")
            return []