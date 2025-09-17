# app.py
"""Streamlit interface for AI Research Tool - Powered by Gemini AI"""

import streamlit as st
import asyncio
import logging
import json
from datetime import datetime

from models.data_models import APIKeys
from core.research_engine import AIResearchEngine
from config.settings import PAGE_TITLE, PAGE_ICON, LAYOUT

# Configure logging
logging.basicConfig(level=logging.INFO)

# Static API Keys Configuration
# Updated to use your Gemini API key
STATIC_API_KEYS = {
    "deepseek": "",  # Deprecated - keeping for compatibility
    "google_search": "AIzaSyBAycnQVkKTlgcFunxg-vjYl-hc6Cd0Ua4",
    "gemini": "AIzaSyDJjvgXwLj4KgJF-xIX6c9qmFknGjkdxo8",  # Your Gemini API key
    "news": "4e2dde8f88cc459d89adacd07fe47cf2", 
    "twitter": "COznXqtITOCdEbMeDyPcCZUFnt3PTZiyvxC4gHgtxhUMbOt1hU",
    "market": "4e2dde8f88cc459d89adacd07fe47cf2"
}

# Gemini API test function
async def test_gemini_comprehensive():
    """Comprehensive Gemini API test"""
    
    # Import and use Gemini client
    from services.gemini_client import GeminiClient
    
    api_key = STATIC_API_KEYS.get("gemini")
    client = GeminiClient(api_key)
    
    st.write("### 🧪 Gemini AI API Test Results")
    
    # Test 1: Basic Connection
    st.write("**Test 1: Connection Test**")
    with st.spinner("Testing Gemini API connection..."):
        connection_result = await client.test_connection()
    
    if connection_result["success"]:
        st.success("✅ API Key and Connection: WORKING")
        st.json(connection_result)
    else:
        st.error("❌ API Connection: FAILED")
        st.json(connection_result)
        return
    
    # Test 2: Structured Analysis
    st.write("**Test 2: Research Analysis Test**")
    research_prompt = """Analyze "Artificial Intelligence" with these sections:

1. EXECUTIVE SUMMARY
2. MARKET ANALYSIS  
3. TECHNICAL DETAILS
4. BUSINESS OPPORTUNITIES

Please use exactly these headers."""
    
    with st.spinner("Testing Gemini research generation..."):
        research_response = await client.generate_response(research_prompt, max_tokens=1500)
    
    if research_response and not research_response.startswith("Error"):
        st.success("✅ Research Generation: WORKING")
        st.text_area("Full Response:", research_response, height=300)
        
        # Check sections
        sections = {
            "EXECUTIVE SUMMARY": "EXECUTIVE SUMMARY" in research_response.upper(),
            "MARKET ANALYSIS": "MARKET ANALYSIS" in research_response.upper(),
            "TECHNICAL DETAILS": "TECHNICAL DETAILS" in research_response.upper(),
            "BUSINESS OPPORTUNITIES": "BUSINESS OPPORTUNITIES" in research_response.upper()
        }
        
        st.write("**Section Detection:**")
        all_found = True
        for section, found in sections.items():
            if found:
                st.success(f"✅ {section}")
            else:
                st.error(f"❌ {section}")
                all_found = False
        
        if all_found:
            st.success("🎉 ALL TESTS PASSED! Your Gemini API is working properly.")
        else:
            st.warning("⚠️ Some sections missing. Check response parsing.")
    else:
        st.error("❌ Research Generation: FAILED")
        st.write("Error:", research_response)

def add_api_tester():
    """Add Gemini API tester to sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧪 Gemini AI API Tester")
    
    if st.sidebar.button("🚀 Test Gemini API"):
        st.markdown("---")
        asyncio.run(test_gemini_comprehensive())

def main():
    """Main Streamlit application"""
    
    # Page configuration
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=LAYOUT
    )
    
    # Title and description
    st.title(f"{PAGE_ICON} AI Research Engine - Powered by Google Gemini 🤖")
    st.markdown("### Comprehensive research on any topic using advanced AI")
    
    # Initialize API keys from static configuration
    api_keys = APIKeys(
        google=STATIC_API_KEYS.get("gemini"),           # Primary google key
        google_search=STATIC_API_KEYS.get("google_search"),    # Same key for search
        deepseek=STATIC_API_KEYS.get("deepseek"),       # Keep for compatibility
        news=STATIC_API_KEYS.get("news"),
        twitter=STATIC_API_KEYS.get("twitter"),
        market=STATIC_API_KEYS.get("market")
    )
    
    # Check if required API key is configured
    gemini_key = STATIC_API_KEYS.get("gemini")
    if not gemini_key:
        st.error("⚠️ Gemini API key not configured. Please update STATIC_API_KEYS in the code.")
        st.info("Configure your Gemini API key in the STATIC_API_KEYS dictionary at the top of app.py")
        return
    
    # Initialize research engine (will use Gemini instead of DeepSeek)
    research_engine = AIResearchEngine(api_keys)
    
    # Show configured services status
    with st.sidebar:
        st.title("🔧 Service Status")
        
        services = [
            ("Gemini AI", bool(gemini_key)),  # Updated to show Gemini
            ("Google Search", api_keys.google_search and api_keys.google_search != "your_google_search_api_key_here"),
            ("News API", api_keys.news and api_keys.news != "your_news_api_key_here"),
            ("Twitter API", api_keys.twitter and api_keys.twitter != "your_twitter_bearer_token_here"),
            ("Market Data", api_keys.market and api_keys.market != "your_market_data_api_key_here")
        ]
        
        for service, is_configured in services:
            if is_configured:
                st.success(f"✅ {service}")
            else:
                st.warning(f"⚠️ {service} (Optional)")
        
        # Show model info
        st.markdown("---")
        st.markdown("### 🤖 AI Model Info")
        st.info("**Model**: Gemini 1.5 Pro\n**Provider**: Google AI")
    
    # Add API tester to sidebar
    add_api_tester()
    
    # Main interface
    st.markdown("---")
    
    # Search interface
    col1, col2 = st.columns([4, 1])
    
    with col1:
        topic = st.text_input(
            "🎯 Enter research topic:",
            placeholder="e.g., Python, Robotics Market, AI Trends, React.js",
            help="Enter any topic you want to research"
        )
    
    with col2:
        st.write("")  # Space for alignment
        research_button = st.button("🚀 Start Research", type="primary")
    
    # Quick topic buttons
    st.markdown("#### 🔥 Quick Topics:")
    quick_topics = [
        "Python Latest Features",
        "AI Market Analysis", 
        "Robotics Industry",
        "React.js Trends",
        "Blockchain Applications",
        "Machine Learning"
    ]
    
    cols = st.columns(len(quick_topics))
    for i, quick_topic in enumerate(quick_topics):
        with cols[i]:
            if st.button(quick_topic, key=f"quick_{i}"):
                topic = quick_topic
                research_button = True
    
    # Research execution
    if research_button and topic:
        st.markdown("---")
        
        # Show processing status
        with st.container():
            start_time = datetime.now()
            
            # Create progress containers
            progress_container = st.container()
            results_container = st.container()
            
            with progress_container:
                st.info("🔍 Starting comprehensive research with Gemini AI...")
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate progress updates
                status_text.text("📊 Collecting data from multiple sources...")
                progress_bar.progress(25)
                
                try:
                    # Run research
                    result = asyncio.run(research_engine.research_topic(topic))
                    
                    progress_bar.progress(75)
                    status_text.text("🤖 Gemini AI analysis complete...")
                    progress_bar.progress(100)
                    
                    end_time = datetime.now()
                    research_time = (end_time - start_time).total_seconds()
                    
                    # Clear progress indicators
                    progress_container.empty()
                    
                    # Display results
                    with results_container:
                        st.success(f"✅ Research completed in {research_time:.2f} seconds!")
                        
                        # Debug information (helpful for troubleshooting)
                        with st.expander("🔧 Debug Information"):
                            st.write("**Result Object Debug:**")
                            debug_info = {
                                "has_summary": bool(result.summary),
                                "has_market_analysis": bool(result.market_analysis),
                                "has_technical_details": bool(result.technical_details),
                                "has_business_opportunities": bool(result.business_opportunities),
                                "summary_length": len(result.summary) if result.summary else 0,
                                "market_analysis_length": len(result.market_analysis) if result.market_analysis else 0,
                                "technical_details_length": len(result.technical_details) if result.technical_details else 0,
                                "business_opportunities_length": len(result.business_opportunities) if result.business_opportunities else 0,
                                "ai_provider": "Google Gemini 1.5 Pro"
                            }
                            st.json(debug_info)
                        
                        # Display results using the helper function
                        display_research_results(result)
                        
                except Exception as e:
                    st.error(f"❌ Research failed: {str(e)}")
                    st.info("Please check your Gemini API key configuration and internet connection.")
                    
                    # Show troubleshooting tips
                    with st.expander("🛠️ Troubleshooting Tips"):
                        st.markdown("""
                        **Common Issues:**
                        1. **API Key**: Make sure your Gemini API key is valid and has quota
                        2. **Network**: Check your internet connection
                        3. **Rate Limits**: Gemini might have rate limiting
                        4. **Content Policy**: Request might be blocked by safety filters
                        
                        **Solutions:**
                        - Test the API using the sidebar tester
                        - Check Google AI Studio for API key status
                        - Try a simpler/different research topic
                        """)

def display_research_results(result):
    """Display research results in organized format"""
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Confidence Score", f"{result.confidence_score:.1f}%")
    with col2:
        st.metric("News Articles", len(result.latest_news))
    with col3:
        st.metric("Key Players", len(result.key_players))
    with col4:
        st.metric("Data Sources", len(result.sources))
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Summary", 
        "📈 Market Analysis", 
        "🔧 Technical Details", 
        "💼 Business Opportunities", 
        "📰 Latest News"
    ])
    
    # Summary tab
    with tab1:
        st.markdown("### Executive Summary")
        if result.summary and result.summary.strip():
            st.write(result.summary)
        else:
            st.warning("⚠️ Summary not generated")
            st.info("Possible issues: Gemini API not responding, check API key, or content was filtered")
        
        # Key players
        if result.key_players:
            st.markdown("### 🏢 Key Players")
            cols = st.columns(min(len(result.key_players), 5))
            for i, player in enumerate(result.key_players):
                with cols[i]:
                    st.info(player)
    
    # Market Analysis tab
    with tab2:
        st.markdown("### Market Analysis")
        if result.market_analysis and result.market_analysis.strip():
            st.write(result.market_analysis)
        else:
            st.warning("⚠️ Market analysis not available")
            st.info("This usually means Gemini API didn't generate this section properly or content was filtered")
        
        # Trends
        if result.trends:
            st.markdown("### 📊 Key Trends")
            for i, trend in enumerate(result.trends, 1):
                st.write(f"**{i}.** {trend}")
    
    # Technical Details tab
    with tab3:
        st.markdown("### Technical Analysis")
        if result.technical_details and result.technical_details.strip():
            st.write(result.technical_details)
        else:
            st.warning("⚠️ Technical details not available")
            st.info("AI analysis didn't complete successfully or response parsing failed")
    
    # Business Opportunities tab
    with tab4:
        st.markdown("### Business Opportunities")
        if result.business_opportunities and result.business_opportunities.strip():
            st.write(result.business_opportunities)
        else:
            st.warning("⚠️ Business opportunities analysis not available")
            st.info("Incomplete AI analysis or Gemini API processing issues")
    
    # Latest News tab
    with tab5:
        st.markdown("### Latest News & Updates")
        if result.latest_news:
            for i, news in enumerate(result.latest_news[:5], 1):
                with st.container():
                    st.markdown(f"**{i}. {news.get('title', 'No title')}**")
                    
                    # News metadata
                    col1, col2 = st.columns(2)
                    with col1:
                        st.caption(f"📰 Source: {news.get('source', 'Unknown')}")
                    with col2:
                        st.caption(f"📅 {news.get('publishedAt', 'Unknown date')}")
                    
                    # Description
                    if news.get('description'):
                        st.write(news['description'])
                    
                    # Read more link
                    if news.get('url'):
                        st.markdown(f"[📖 Read more]({news['url']})")
                    
                    if i < len(result.latest_news):
                        st.divider()
        else:
            st.info("No recent news found. Configure News API key for latest updates.")
    
    # Data sources footer
    if result.sources:
        st.markdown("---")
        st.markdown("### 📚 Data Sources")
        for source in result.sources:
            st.caption(f"• {source}")
    
    # Export options
    st.markdown("---")
    st.markdown("### 📤 Export Research")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📄 Export as Text"):
            text_content = create_text_export(result)
            st.download_button(
                "Download Text Report",
                text_content,
                file_name=f"research_{result.topic}_{result.timestamp.strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    with col2:
        if st.button("📊 Export as JSON"):
            json_content = {
                'topic': result.topic,
                'timestamp': result.timestamp.isoformat(),
                'summary': result.summary,
                'market_analysis': result.market_analysis,
                'technical_details': result.technical_details,
                'business_opportunities': result.business_opportunities,
                'key_players': result.key_players,
                'trends': result.trends,
                'confidence_score': result.confidence_score,
                'ai_provider': 'Google Gemini 1.5 Pro'
            }
            st.download_button(
                "Download JSON Report",
                json.dumps(json_content, indent=2),
                file_name=f"research_{result.topic}_{result.timestamp.strftime('%Y%m%d')}.json",
                mime="application/json"
            )

def create_text_export(result):
    """Create text export of research results"""
    text_content = f"""
AI RESEARCH REPORT - POWERED BY GEMINI AI
=========================================

Topic: {result.topic}
Generated: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
Confidence Score: {result.confidence_score:.1f}%
AI Provider: Google Gemini 1.5 Pro

EXECUTIVE SUMMARY
================
{result.summary}

MARKET ANALYSIS
==============
{result.market_analysis}

TECHNICAL DETAILS
================
{result.technical_details}

BUSINESS OPPORTUNITIES
=====================
{result.business_opportunities}

KEY PLAYERS
===========
{', '.join(result.key_players)}

KEY TRENDS
==========
{chr(10).join([f"• {trend}" for trend in result.trends])}

DATA SOURCES
============
{chr(10).join([f"• {source}" for source in result.sources])}

---
Generated by AI Research Engine powered by Google Gemini
"""
    return text_content

if __name__ == "__main__":
    main()