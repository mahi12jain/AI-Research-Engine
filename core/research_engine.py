# core/research_engine.py - UPDATED FOR GEMINI
"""Main research engine coordinating all AI and data services"""

import logging
from datetime import datetime
from typing import Optional

from models.data_models import APIKeys, ResearchResult
from services.gemini_client import GeminiClient  # Updated import
from services.news_service import NewsService
from services.market_service import MarketService
from utils.response_parser import ResponseParser

logger = logging.getLogger(__name__)

class AIResearchEngine:
    """Main research engine that coordinates all services"""
    
    def __init__(self, api_keys: APIKeys):
        self.api_keys = api_keys
        
        # Initialize Gemini client with the google API key
        self.gemini_client = GeminiClient(api_keys.google)
        
        # Initialize other services
        self.news_service = NewsService(api_keys.news) if api_keys.news else None
        self.market_service = MarketService(api_keys.market) if api_keys.market else None
        
        # Response parser
        self.response_parser = ResponseParser()
    
    async def research_topic(self, topic: str) -> ResearchResult:
        """Conduct comprehensive research on a topic"""
        logger.info(f"Starting research on topic: {topic}")
        
        try:
            # Generate AI analysis using Gemini
            ai_analysis = await self._generate_ai_analysis(topic)
            
            # Parse the AI response into structured data
            parsed_data = self.response_parser.parse_research_response(ai_analysis)
            
            # Gather additional data from external sources
            latest_news = await self._fetch_latest_news(topic) if self.news_service else []
            market_data = await self._fetch_market_data(topic) if self.market_service else {}
            
            # Create comprehensive result
            result = ResearchResult(
                topic=topic,
                timestamp=datetime.now(),
                summary=parsed_data.get("summary", ""),
                market_analysis=parsed_data.get("market_analysis", ""),
                technical_details=parsed_data.get("technical_details", ""),
                business_opportunities=parsed_data.get("business_opportunities", ""),
                key_players=parsed_data.get("key_players", []),
                trends=parsed_data.get("trends", []),
                latest_news=latest_news,
                confidence_score=self._calculate_confidence_score(parsed_data, latest_news),
                sources=self._compile_sources()
            )
            
            logger.info(f"Research completed successfully for topic: {topic}")
            return result
            
        except Exception as e:
            logger.error(f"Research failed for topic {topic}: {e}")
            # Return a result with error information
            return ResearchResult(
                topic=topic,
                timestamp=datetime.now(),
                summary=f"Research failed: {str(e)}",
                market_analysis="Analysis unavailable due to error",
                technical_details="Technical analysis unavailable",
                business_opportunities="Business analysis unavailable",
                key_players=[],
                trends=[],
                latest_news=[],
                confidence_score=0.0,
                sources=["Error occurred during research"]
            )
    
    async def _generate_ai_analysis(self, topic: str) -> str:
        """Generate AI analysis using Gemini"""
        prompt = f"""
        Provide a comprehensive research analysis for the topic: "{topic}"

        Please structure your response with exactly these sections:

        1. EXECUTIVE SUMMARY
        [Provide a 200-300 word comprehensive overview of the topic, its current state, significance, and key aspects]

        2. MARKET ANALYSIS
        [Provide detailed market intelligence including market size, growth rates, major competitors, market trends, and future outlook]

        3. TECHNICAL DETAILS
        [Explain technical aspects, architecture, implementation details, key technologies, and technical challenges or innovations]

        4. BUSINESS OPPORTUNITIES
        [List specific business opportunities, potential applications, investment prospects, and strategic recommendations]

        5. KEY PLAYERS
        [List 5-10 major companies, organizations, or individuals who are key players in this field]

        6. TRENDS
        [List 5-7 key current and emerging trends related to this topic]

        Please use exactly these section headers and provide detailed, accurate information for each section.
        """
        
        try:
            response = await self.gemini_client.generate_response(prompt, max_tokens=4000)
            logger.info(f"Gemini AI analysis completed, response length: {len(response)}")
            return response
        except Exception as e:
            logger.error(f"Gemini AI analysis failed: {e}")
            return f"AI Analysis Error: {str(e)}"
    
    async def _fetch_latest_news(self, topic: str) -> list:
        """Fetch latest news related to the topic"""
        if not self.news_service:
            return []
        
        try:
            news_data = await self.news_service.get_news(topic, limit=10)
            logger.info(f"Fetched {len(news_data)} news articles")
            return news_data
        except Exception as e:
            logger.error(f"News fetching failed: {e}")
            return []
    
    async def _fetch_market_data(self, topic: str) -> dict:
        """Fetch market data related to the topic"""
        if not self.market_service:
            return {}
        
        try:
            market_data = await self.market_service.get_market_data(topic)
            logger.info("Market data fetched successfully")
            return market_data
        except Exception as e:
            logger.error(f"Market data fetching failed: {e}")
            return {}
    
    def _calculate_confidence_score(self, parsed_data: dict, news_data: list) -> float:
        """Calculate confidence score based on available data"""
        score = 0.0
        
        # Base score for AI analysis sections
        sections = ["summary", "market_analysis", "technical_details", "business_opportunities"]
        for section in sections:
            if parsed_data.get(section) and len(parsed_data[section]) > 50:
                score += 20.0
        
        # Bonus for having key players and trends
        if parsed_data.get("key_players"):
            score += 10.0
        if parsed_data.get("trends"):
            score += 10.0
        
        # Bonus for external data sources
        if news_data:
            score = min(score + 5.0, 100.0)
        
        return min(score, 100.0)
    
    def _compile_sources(self) -> list:
        """Compile list of data sources used"""
        sources = ["Google Gemini 1.5 Pro AI Analysis"]
        
        if self.news_service:
            sources.append("News API")
        if self.market_service:
            sources.append("Market Data API")
        
        return sources
    
    async def test_all_services(self) -> dict:
        """Test all configured services"""
        results = {}
        
        # Test Gemini AI
        try:
            gemini_test = await self.gemini_client.test_connection()
            results["gemini"] = {
                "status": "success" if gemini_test["success"] else "failed",
                "details": gemini_test
            }
        except Exception as e:
            results["gemini"] = {
                "status": "error",
                "details": str(e)
            }
        
        # Test News Service
        if self.news_service:
            try:
                news_test = await self.news_service.test_connection()
                results["news"] = {
                    "status": "success" if news_test else "failed",
                    "details": "News API test completed"
                }
            except Exception as e:
                results["news"] = {
                    "status": "error",
                    "details": str(e)
                }
        else:
            results["news"] = {
                "status": "not_configured",
                "details": "News API key not provided"
            }
        
        # Test Market Service
        if self.market_service:
            try:
                market_test = await self.market_service.test_connection()
                results["market"] = {
                    "status": "success" if market_test else "failed",
                    "details": "Market API test completed"
                }
            except Exception as e:
                results["market"] = {
                    "status": "error",
                    "details": str(e)
                }
        else:
            results["market"] = {
                "status": "not_configured",
                "details": "Market API key not provided"
            }
        
        return results
