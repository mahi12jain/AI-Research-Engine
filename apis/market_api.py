# apis/market_api.py
"""Market Data API integration"""

import aiohttp
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class MarketDataAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        # You can use Alpha Vantage, Yahoo Finance, etc.
        self.base_url = "https://www.alphavantage.co/query"
    
    async def search(self, query: str) -> List[Dict]:
        """Get market data related to query"""
        try:
            # Example: Search for company stock data
            params = {
                'function': 'SYMBOL_SEARCH',
                'keywords': query,
                'apikey': self.api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        matches = data.get('bestMatches', [])
                        return [
                            {
                                'symbol': match.get('1. symbol', ''),
                                'name': match.get('2. name', ''),
                                'type': match.get('3. type', ''),
                                'region': match.get('4. region', ''),
                                'currency': match.get('8. currency', ''),
                                'source': 'Market Data'
                            }
                            for match in matches
                        ]
            return []
        except Exception as e:
            logger.error(f"Market Data API error: {e}")
            return []