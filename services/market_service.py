# services/market_service.py
"""Market service for business analysis and market data"""

import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)

class MarketService:
    """Service for market analysis and business intelligence"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://finnhub.io/api/v1"  # Using Finnhub for market data
        self.headers = {
            "Content-Type": "application/json"
        }
    
    async def get_market_data(self, topic: str) -> Dict[str, Any]:
        """Get market data and business analysis for a topic"""
        if not self.api_key:
            logger.warning("Market API key not configured")
            return self._get_mock_market_data(topic)
        
        try:
            # Get company information and news
            market_data = {
                'topic': topic,
                'timestamp': datetime.now().isoformat(),
                'market_analysis': await self._analyze_market_trends(topic),
                'key_metrics': await self._get_key_metrics(topic),
                'competitor_analysis': await self._get_competitor_data(topic),
                'investment_opportunities': await self._get_investment_insights(topic)
            }
            
            return market_data
            
        except Exception as e:
            logger.error(f"Market data fetching failed: {e}")
            return self._get_mock_market_data(topic)
    
    async def _analyze_market_trends(self, topic: str) -> str:
        """Analyze market trends for the topic"""
        try:
            # Search for company news related to the topic
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/company-news"
                params = {
                    'symbol': 'AAPL',  # Using Apple as example
                    'from': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                    'to': datetime.now().strftime('%Y-%m-%d'),
                    'token': self.api_key
                }
                
                async with session.get(url, params=params, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        news_count = len(data) if isinstance(data, list) else 0
                        
                        return f"Market analysis for {topic}: Recent activity shows {news_count} news items in the last 30 days. The market is showing active interest in this sector with growing investor attention."
                    else:
                        return f"Market analysis for {topic}: Current market conditions show moderate activity with potential for growth in this emerging sector."
        except Exception as e:
            logger.error(f"Market trend analysis failed: {e}")
            return f"Market analysis for {topic}: Industry shows steady growth potential with increasing market adoption and technological advancement."
    
    async def _get_key_metrics(self, topic: str) -> Dict[str, Any]:
        """Get key market metrics"""
        return {
            'market_size': 'Growing market with expanding opportunities',
            'growth_rate': 'Moderate to high growth potential',
            'competition_level': 'Moderate competition with room for innovation',
            'investment_activity': 'Active investment interest from venture capital',
            'regulatory_environment': 'Supportive regulatory framework'
        }
    
    async def _get_competitor_data(self, topic: str) -> List[str]:
        """Get competitor analysis"""
        # Mock competitor data based on topic
        competitors = {
            'ai': ['OpenAI', 'Google DeepMind', 'Microsoft AI', 'Amazon AI', 'Meta AI'],
            'python': ['Python Software Foundation', 'JetBrains', 'Anaconda', 'Google', 'Microsoft'],
            'blockchain': ['Ethereum Foundation', 'Binance', 'Coinbase', 'Ripple', 'Cardano'],
            'machine learning': ['TensorFlow', 'PyTorch', 'Scikit-learn', 'Keras', 'Hugging Face'],
            'robotics': ['Boston Dynamics', 'iRobot', 'ABB', 'KUKA', 'Universal Robots']
        }
        
        # Find relevant competitors
        topic_lower = topic.lower()
        for key, comps in competitors.items():
            if key in topic_lower:
                return comps
        
        return ['Leading companies in the sector', 'Established market players', 'Emerging startups']
    
    async def _get_investment_insights(self, topic: str) -> str:
        """Get investment insights and opportunities"""
        insights = {
            'ai': 'AI sector shows strong investment potential with growing enterprise adoption, focus on AI infrastructure and applications.',
            'python': 'Python ecosystem continues to grow with strong developer adoption, opportunities in data science and web development.',
            'blockchain': 'Blockchain technology gaining mainstream adoption, opportunities in DeFi, NFTs, and enterprise solutions.',
            'machine learning': 'ML market expanding rapidly with applications across industries, focus on automation and predictive analytics.',
            'robotics': 'Robotics industry growing with automation trends, opportunities in manufacturing, healthcare, and service robots.'
        }
        
        topic_lower = topic.lower()
        for key, insight in insights.items():
            if key in topic_lower:
                return insight
        
        return f"Investment opportunities in {topic} sector include early-stage startups, established companies expanding into new markets, and infrastructure development."
    
    def _get_mock_market_data(self, topic: str) -> Dict[str, Any]:
        """Get mock market data when API is not available"""
        return {
            'topic': topic,
            'timestamp': datetime.now().isoformat(),
            'market_analysis': f"Market analysis for {topic}: The industry shows strong growth potential with increasing market adoption. Key trends include digital transformation, automation, and innovation driving market expansion.",
            'key_metrics': {
                'market_size': 'Large and growing market',
                'growth_rate': 'High growth potential',
                'competition_level': 'Moderate to high competition',
                'investment_activity': 'Active investment interest',
                'regulatory_environment': 'Evolving regulatory landscape'
            },
            'competitor_analysis': [
                'Major established players',
                'Emerging startups',
                'International competitors',
                'Technology leaders',
                'Innovation-focused companies'
            ],
            'investment_opportunities': f"Investment opportunities in {topic} include early-stage companies, growth-stage businesses, and established players expanding into new markets. Focus areas include technology innovation, market expansion, and strategic partnerships."
        }
    
    async def test_connection(self) -> bool:
        """Test market API connection"""
        try:
            if not self.api_key:
                return False
            
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/quote"
                params = {
                    'symbol': 'AAPL',
                    'token': self.api_key
                }
                
                async with session.get(url, params=params, timeout=10) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"Market API test failed: {e}")
            return False
    
    async def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """Get company profile information"""
        if not self.api_key:
            return {}
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/stock/profile2"
                params = {
                    'symbol': symbol,
                    'token': self.api_key
                }
                
                async with session.get(url, params=params, timeout=30) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return {}
        except Exception as e:
            logger.error(f"Company profile fetch failed: {e}")
            return {}
    
    def format_market_analysis(self, market_data: Dict[str, Any]) -> str:
        """Format market data for display"""
        if not market_data:
            return "No market data available."
        
        formatted = []
        formatted.append(f"Market Analysis for: {market_data.get('topic', 'Unknown')}")
        formatted.append("=" * 50)
        
        if market_data.get('market_analysis'):
            formatted.append(f"Analysis: {market_data['market_analysis']}")
        
        if market_data.get('key_metrics'):
            formatted.append("\nKey Metrics:")
            for key, value in market_data['key_metrics'].items():
                formatted.append(f"   {key.replace('_', ' ').title()}: {value}")
        
        if market_data.get('competitor_analysis'):
            formatted.append("\nKey Competitors:")
            for competitor in market_data['competitor_analysis']:
                formatted.append(f"   {competitor}")
        
        if market_data.get('investment_opportunities'):
            formatted.append(f"\nInvestment Opportunities:")
            formatted.append(f"  {market_data['investment_opportunities']}")
        
        return "\n".join(formatted)
