# services/prompt_engine.py
"""Advanced prompt engineering for research tasks"""

from typing import Dict, Any

class PromptEngine:
    """Advanced prompt engineering for research tasks"""
    
    @staticmethod
    def create_research_prompt(topic: str, data: Dict[str, Any]) -> str:
        """Create optimized research prompt for DeepSeek with enhanced structure"""
        return f"""
COMPREHENSIVE RESEARCH ANALYSIS 

RESEARCH TOPIC: {topic}

DATA CONTEXT:
- Web Sources: {len(data.get('web_results', []))} articles
- News Articles: {len(data.get('news_results', []))} recent stories  
- Market Data: {len(data.get('market_results', []))} data points
- Social Insights: {len(data.get('social_results', []))} posts
- Academic Sources: {len(data.get('academic_results', []))} papers

AVAILABLE INFORMATION SUMMARY:
{PromptEngine._create_data_context(data)}

REQUIRED ANALYSIS STRUCTURE:

1. EXECUTIVE SUMMARY (250 words)
   Provide a comprehensive yet concise summary that covers:
   - What is {topic}? (Clear definition and context)
   - Current market position and adoption level
   - Why it matters now (significance and impact)
   - Key statistics and growth metrics
   - Primary use cases and target markets

2. MARKET ANALYSIS (300 words)
   Deliver detailed market intelligence including:
   - Market size (current and projected) with specific figures
   - Growth rate and key drivers
   - Competitive landscape and market leaders
   - Market share distribution
   - Geographic presence and regional variations
   - Revenue models and pricing strategies
   - Recent funding/investment activity
   - Market trends and consumer adoption patterns

3. TECHNICAL DETAILS (300 words)
   Provide in-depth technical analysis covering:
   - Core technology architecture and components
   - How it works (technical mechanisms explained simply)
   - Latest features, updates, and capabilities
   - Performance benchmarks and specifications
   - Technical requirements and implementation complexity
   - Integration capabilities and compatibility
   - Security, scalability, and reliability aspects
   - Innovation roadmap and future developments

4. BUSINESS OPPORTUNITIES & PROJECT SUGGESTIONS (350 words)
   Identify specific opportunities including:
   
   STARTUP OPPORTUNITIES:
   - 3 specific business ideas with market potential
   - Required resources and estimated investment
   - Target customer segments and revenue models
   
   PROJECT SUGGESTIONS:
   - 5 concrete project ideas for different business sizes
   - Implementation timeline and resource requirements
   - Expected ROI and success metrics
   
   INVESTMENT OPPORTUNITIES:
   - Key companies to watch or invest in
   - Emerging sectors with high growth potential
   - Partnership and collaboration opportunities
   
   BUSINESS APPLICATIONS:
   - Industry-specific use cases
   - Process improvement opportunities
   - Cost reduction and efficiency gains

5. FUTURE OUTLOOK & TRENDS (200 words)
   Analyze future trajectory including:
   - 3-5 year market predictions with reasoning
   - Emerging trends and disruptive factors
   - Potential challenges and risk factors
   - Innovation pipeline and breakthrough possibilities
   - Regulatory landscape and policy impacts

6. KEY ACTIONABLE INSIGHTS
   Summarize with specific recommendations:
   - Top 5 companies/players to monitor
   - Top 5 trends that will shape the market
   - Top 3 immediate business opportunities
   - Top 3 challenges to watch for
   - Top 3 investment recommendations

ANALYSIS GUIDELINES:
- Use specific data points, percentages, and metrics
- Include recent developments from the past 6-12 months
- Balance optimism with realistic assessment of challenges
- Provide actionable insights that readers can implement
- Focus on practical applications over theoretical concepts
- Ensure accuracy by stating confidence levels when uncertain

Please conduct a thorough analysis that transforms the available data into strategic insights for business decision-making."""
    
    @staticmethod
    def _create_data_context(data: Dict[str, Any]) -> str:
        """Create enhanced data context for better prompt understanding"""
        context_parts = []
        
        # Web results context
        if data.get('web_results'):
            top_sources = []
            for item in data['web_results'][:5]:
                title = item.get('title', 'Unknown')[:60]
                source = item.get('source', 'Web')
                top_sources.append(f"• {title}... ({source})")
            context_parts.append(f"KEY WEB SOURCES:\n" + "\n".join(top_sources))
        
        # News context
        if data.get('news_results'):
            recent_news = []
            for item in data['news_results'][:3]:
                title = item.get('title', 'Unknown')[:50]
                date = item.get('publishedAt', 'Recent')[:10]
                recent_news.append(f"• {title}... ({date})")
            context_parts.append(f"RECENT NEWS:\n" + "\n".join(recent_news))
        
        # Market data context
        if data.get('market_results'):
            context_parts.append(f"MARKET DATA: {len(data['market_results'])} financial indicators available")
        
        # Social media context
        if data.get('social_results'):
            context_parts.append(f"SOCIAL INSIGHTS: {len(data['social_results'])} social media mentions analyzed")
        
        # Academic context
        if data.get('academic_results'):
            context_parts.append(f"ACADEMIC RESEARCH: {len(data['academic_results'])} scholarly articles referenced")
        
        return "\n\n".join(context_parts) if context_parts else "Limited data available - providing analysis based on general knowledge"

    @staticmethod
    def create_focused_summary_prompt(topic: str, raw_analysis: str) -> str:
        """Create a focused prompt for generating concise summaries"""
        return f"""
SUMMARY OPTIMIZATION REQUEST

TOPIC: {topic}
RAW ANALYSIS: {raw_analysis[:1000]}...

Create an optimized executive summary that:
1. Captures the essence in exactly 150-200 words
2. Uses bullet points for key statistics
3. Includes 3-5 most important insights
4. Focuses on practical implications
5. Uses accessible language for all audiences

Format: Professional, scannable, action-oriented."""



# AVAILABLE DATA:
# - Web Search Results: {len(data.get('web_results', []))} sources
# - News Articles: {len(data.get('news_results', []))} articles
# - Academic Papers: {len(data.get('academic_results', []))} papers
# - Patent Information: {len(data.get('patent_results', []))} patents
# - Social Media Insights: {len(data.get('social_results', []))} posts
# - Market Data: {len(data.get('market_results', []))} data points

# RAW DATA SUMMARY:
# {PromptEngine._summarize_data(data)}

# ANALYSIS REQUIREMENTS:

# 1. EXECUTIVE SUMMARY (200 words)
#    - Core definition and current state
#    - Key significance and impact
#    - Primary use cases and applications

# 2. TECHNICAL ANALYSIS (300 words)
#    - How it works (technical details)
#    - Latest features and capabilities
#    - Architecture and implementation
#    - Performance characteristics

# 3. MARKET ANALYSIS (250 words)
#    - Market size and growth projections
#    - Key players and competitive landscape
#    - Revenue models and pricing
#    - Geographic distribution

# 4. BUSINESS OPPORTUNITIES (200 words)
#    - Emerging opportunities
#    - Investment trends and funding
#    - Startup ecosystem
#    - Future market potential

# 5. LATEST DEVELOPMENTS (150 words)
#    - Recent news and announcements
#    - Product launches and updates
#    - Industry partnerships
#    - Regulatory changes

# 6. FUTURE OUTLOOK (150 words)
#    - Predicted trends and evolution
#    - Challenges and risks
#    - Innovation pipeline
#    - Long-term implications

# 7. KEY INSIGHTS
#    - Top 5 companies/players
#    - Top 5 trends to watch
#    - Top 3 investment opportunities
#    - Top 3 challenges

# Please provide a comprehensive, data-driven analysis that synthesizes all available information into actionable insights. Focus on accuracy, specific examples, and practical implications.
# """
    
#     @staticmethod
#     def _summarize_data(data: Dict[str, Any]) -> str:
#         """Summarize collected data for prompt context"""
#         summary = ""
        
#         # Web results
#         if data.get('web_results'):
#             web_titles = [item.get('title', '') for item in data['web_results'][:5]]
#             summary += f"Web Sources: {', '.join(web_titles)}\n"
        
#         # News results
#         if data.get('news_results'):
#             news_titles = [item.get('title', '') for item in data['news_results'][:3]]
#             summary += f"Recent News: {', '.join(news_titles)}\n"
        
#         # Academic results
#         if data.get('academic_results'):
#             summary += f"Academic Research: {len(data['academic_results'])} papers found\n"
        
#         return summary