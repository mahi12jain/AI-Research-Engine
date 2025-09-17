# services/data_collector.py
"""Multi-source data collection system"""

import asyncio
import logging
from typing import Dict, Any
from models.data_models import APIKeys
from apis.google_api import GoogleSearchAPI
from apis.news_api import NewsAPI
from apis.arxiv_api import ArxivAPI
from apis.patent_api import PatentAPI
from apis.twitter_api import TwitterAPI
from apis.market_api import MarketDataAPI

logger = logging.getLogger(__name__)

class DataCollector:
    """Multi-source data collection system"""
    
    def __init__(self, api_keys: APIKeys):
        self.api_keys = api_keys
        self.sources = {}
        self._setup_apis()
    
    def _setup_apis(self):
        """Setup API clients for different data sources"""
        # Google Search API
        if self.api_keys.google:
            self.sources['web_search'] = GoogleSearchAPI(self.api_keys.google)
        
        # News API
        if self.api_keys.news:
            self.sources['news'] = NewsAPI(self.api_keys.news)
        
        # ArXiv for academic papers (no key required)
        self.sources['academic'] = ArxivAPI()
        
        # Patent data (no key required)
        self.sources['patents'] = PatentAPI()
        
        # Twitter/X API
        if self.api_keys.twitter:
            self.sources['social'] = TwitterAPI(self.api_keys.twitter)
        
        # Market data APIs
        if self.api_keys.market:
            self.sources['market'] = MarketDataAPI(self.api_keys.market)
    
    async def collect_all_data(self, topic: str) -> Dict[str, Any]:
        """Collect data from all available sources"""
        tasks = []
        
        for source_name, api in self.sources.items():
            task = self._collect_from_source(source_name, api, topic)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine results
        combined_data = {
            'web_results': [],
            'news_results': [],
            'academic_results': [],
            'patent_results': [],
            'social_results': [],
            'market_results': []
        }
        
        for i, (source_name, _) in enumerate(self.sources.items()):
            if not isinstance(results[i], Exception):
                combined_data[f"{source_name}_results"] = results[i]
        
        return combined_data
    
    async def _collect_from_source(self, source_name: str, api, topic: str):
        """Collect data from a specific source"""
        try:
            return await api.search(topic)
        except Exception as e:
            logger.error(f"Error collecting from {source_name}: {e}")
            return []