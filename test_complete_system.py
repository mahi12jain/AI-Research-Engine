# test_complete_system.py
"""Complete system test for AI Research Tool"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.data_models import APIKeys
from core.research_engine import AIResearchEngine
from services.gemini_client import GeminiClient
from services.news_service import NewsService
from services.market_service import MarketService

# Test API Keys (from your apikeys.txt)
TEST_API_KEYS = {
    "gemini": "AIzaSyDJjvgXwLj4KgJF-xIX6c9qmFknGjkdxo8",
    "news": "4e2dde8f88cc459d89adacd07fe47cf2",
    "market": "d34gcf1r01qqt8sovug0d34gcf1r01qqt8sovugg"
}

async def test_gemini_client():
    """Test Gemini client functionality"""
    print("\n Testing Gemini Client...")
    
    client = GeminiClient(TEST_API_KEYS["gemini"])
    
    # Test connection
    connection_result = await client.test_connection()
    if connection_result["success"]:
        print(" Gemini API connection: SUCCESS")
        print(f"   Response: {connection_result['response']}")
    else:
        print(" Gemini API connection: FAILED")
        print(f"   Error: {connection_result['error']}")
        return False
    
    # Test response generation
    test_prompt = "Explain artificial intelligence in 2 sentences."
    response = await client.generate_response(test_prompt, max_tokens=100)
    
    if response and not response.startswith("Error"):
        print(" Gemini response generation: SUCCESS")
        print(f"   Response: {response[:100]}...")
    else:
        print(" Gemini response generation: FAILED")
        print(f"   Error: {response}")
        return False
    
    return True

async def test_news_service():
    """Test News service functionality"""
    print("\n Testing News Service...")
    
    service = NewsService(TEST_API_KEYS["news"])
    
    # Test connection
    connection_ok = await service.test_connection()
    if connection_ok:
        print(" News API connection: SUCCESS")
    else:
        print(" News API connection: FAILED")
        return False
    
    # Test news fetching
    news_articles = await service.get_news("artificial intelligence", limit=3)
    if news_articles:
        print(f" News fetching: SUCCESS ({len(news_articles)} articles)")
        for i, article in enumerate(news_articles[:2], 1):
            print(f"   {i}. {article['title'][:60]}...")
    else:
        print(" News fetching: FAILED")
        return False
    
    return True

async def test_market_service():
    """Test Market service functionality"""
    print("\n Testing Market Service...")
    
    service = MarketService(TEST_API_KEYS["market"])
    
    # Test market data fetching
    market_data = await service.get_market_data("artificial intelligence")
    if market_data and market_data.get("market_analysis"):
        print(" Market data fetching: SUCCESS")
        print(f"   Analysis: {market_data['market_analysis'][:100]}...")
    else:
        print(" Market data fetching: FAILED")
        return False
    
    return True

async def test_research_engine():
    """Test complete research engine"""
    print("\n Testing Research Engine...")
    
    api_keys = APIKeys(
        google=TEST_API_KEYS["gemini"],
        news=TEST_API_KEYS["news"],
        market=TEST_API_KEYS["market"]
    )
    
    engine = AIResearchEngine(api_keys)
    
    # Test service status
    service_results = await engine.test_all_services()
    print("\nService Status:")
    for service, result in service_results.items():
        status = result["status"]
        if status == "success":
            print(f"    {service}: {status}")
        elif status == "not_configured":
            print(f"    {service}: {status}")
        else:
            print(f"    {service}: {status}")
    
    # Test complete research
    print("\n Testing Complete Research...")
    result = await engine.research_topic("Python Programming")
    
    if result and result.summary:
        print(" Complete research: SUCCESS")
        print(f"   Topic: {result.topic}")
        print(f"   Summary length: {len(result.summary)} characters")
        print(f"   Market analysis length: {len(result.market_analysis)} characters")
        print(f"   Technical details length: {len(result.technical_details)} characters")
        print(f"   Business opportunities length: {len(result.business_opportunities)} characters")
        print(f"   Key players: {len(result.key_players)}")
        print(f"   Trends: {len(result.trends)}")
        print(f"   News articles: {len(result.latest_news)}")
        print(f"   Confidence score: {result.confidence_score:.1f}%")
        
        # Show sample content
        print("\n Sample Summary:")
        print(f"   {result.summary[:200]}...")
        
        if result.key_players:
            print("\n Key Players:")
            for player in result.key_players[:3]:
                print(f"    {player}")
        
        if result.trends:
            print("\n Trends:")
            for trend in result.trends[:3]:
                print(f"    {trend}")
        
        return True
    else:
        print(" Complete research: FAILED")
        return False

async def main():
    """Run all tests"""
    print(" Starting AI Research Tool System Tests")
    print("=" * 50)
    
    tests = [
        ("Gemini Client", test_gemini_client),
        ("News Service", test_news_service),
        ("Market Service", test_market_service),
        ("Research Engine", test_research_engine)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f" {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print(" TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = " PASSED" if result else " FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print(" ALL TESTS PASSED! Your AI Research Tool is working perfectly!")
    else:
        print(" Some tests failed. Check the errors above.")

if __name__ == "__main__":
    asyncio.run(main())
