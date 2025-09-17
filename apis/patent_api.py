# apis/patent_api.py
"""Patent API integration"""

import aiohttp
import logging
from typing import List, Dict
from config.settings import PATENT_API_URL, DEFAULT_PATENT_RESULTS

logger = logging.getLogger(__name__)

class PatentAPI:
    def __init__(self):
        self.base_url = PATENT_API_URL
    
    async def search(self, query: str) -> List[Dict]:
        """Search for patents"""
        try:
            data = {
                "q": {"_text_any": {"patent_title": query}},
                "f": ["patent_number", "patent_title", "patent_date", "assignee_organization"],
                "s": [{"patent_date": "desc"}],
                "o": {"per_page": DEFAULT_PATENT_RESULTS}
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        return [
                            {
                                'title': patent.get('patent_title', ''),
                                'number': patent.get('patent_number', ''),
                                'date': patent.get('patent_date', ''),
                                'assignee': patent.get('assignee_organization', ''),
                                'source': 'USPTO'
                            }
                            for patent in result.get('patents', [])
                        ]
            return []
        except Exception as e:
            logger.error(f"Patent API error: {e}")
            return []