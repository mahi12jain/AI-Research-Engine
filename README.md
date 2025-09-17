# AI Research Tool - Powered by Google Gemini

A comprehensive AI-powered research tool that provides detailed analysis on any topic using Google Gemini AI, news data, and market intelligence.

##  Features

- **AI-Powered Analysis**: Uses Google Gemini 1.5 Pro for comprehensive research
- **News Integration**: Fetches latest news articles related to your research topic
- **Business Analysis**: Provides market analysis and business opportunities
- **Structured Reports**: Generates organized reports with multiple sections
- **Export Options**: Export research as text or JSON
- **Real-time Data**: Combines AI analysis with live news and market data

##  Sections Generated

1. **Executive Summary** - Comprehensive overview of the topic
2. **Market Analysis** - Market size, growth, competitors, trends
3. **Technical Details** - Technical aspects and implementation details
4. **Business Opportunities** - Investment prospects and strategic recommendations
5. **Key Players** - Major companies and organizations in the field
6. **Latest News** - Recent news articles and updates

##  Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key
- News API key (optional)
- Market data API key (optional)

### Quick Start

1. **Clone or download the project**
   `ash
   cd ai_research_tool
   `

2. **Install dependencies**
   `ash
   python run_ai_research.py
   `
   Or manually:
   `ash
   pip install -r requirements.txt
   `

3. **Configure API Keys**
   - Your Gemini API key is already configured in the code
   - Optional: Add News API and Market API keys for enhanced features

4. **Run the application**
   `ash
   streamlit run main.py
   `

5. **Open your browser**
   - Go to http://localhost:8501
   - Start researching any topic!

##  API Configuration

### Required: Gemini API Key
Your Gemini API key is already configured in main.py:
`python
STATIC_API_KEYS = {
    "gemini": "AIzaSyDJjvgXwLj4KgJF-xIX6c9qmFknGjkdxo8"
}
`

### Optional: News API
To get latest news articles, add your News API key:
`python
STATIC_API_KEYS = {
    "news": "your_news_api_key_here"
}
`

### Optional: Market Data API
For enhanced business analysis, add your market data API key:
`python
STATIC_API_KEYS = {
    "market": "your_market_api_key_here"
}
`

##  Testing

Run the comprehensive test suite:
`ash
python test_complete_system.py
`

This will test:
- Gemini API connection and response generation
- News service functionality
- Market service functionality
- Complete research engine integration

##  Usage Examples

### Research Topics
- "Artificial Intelligence"
- "Python Programming Language"
- "Blockchain Technology"
- "Machine Learning"
- "Robotics Industry"
- "React.js Framework"

### Quick Topics
The app includes quick topic buttons for:
- Python Latest Features
- AI Market Analysis
- Robotics Industry
- React.js Trends
- Blockchain Applications
- Machine Learning

##  How It Works

1. **Input**: Enter your research topic
2. **AI Analysis**: Gemini AI generates comprehensive analysis
3. **Data Collection**: Fetches latest news and market data
4. **Processing**: Parses and structures the information
5. **Output**: Displays organized research report with multiple sections
6. **Export**: Download results as text or JSON

##  Project Structure

`
ai_research_tool/
 main.py                 # Main Streamlit application
 run_ai_research.py      # Easy launcher script
 test_complete_system.py # Comprehensive test suite
 requirements.txt        # Python dependencies
 core/
    research_engine.py  # Main research coordination
 services/
    gemini_client.py    # Google Gemini AI client
    news_service.py     # News API integration
    market_service.py   # Market data service
 models/
    data_models.py      # Data structures
 utils/
    response_parser.py  # AI response parsing
 config/
     settings.py         # Configuration settings
`

##  Troubleshooting

### Common Issues

1. **"No API key configured"**
   - Check that your Gemini API key is properly set in main.py

2. **"API connection failed"**
   - Verify your API key is valid and has quota
   - Check your internet connection

3. **Empty sections in results**
   - This usually means the AI response wasn't parsed correctly
   - Try a different research topic
   - Check the API tester in the sidebar

4. **News not loading**
   - News API key might be invalid or expired
   - Check your News API quota

### Debug Mode
Use the API tester in the sidebar to diagnose issues:
1. Click " Test Gemini API" in the sidebar
2. Review the test results
3. Check for any error messages

##  Performance

- **Response Time**: Typically 10-30 seconds for complete research
- **Token Usage**: ~2000-4000 tokens per research request
- **Rate Limits**: Respects Gemini API rate limits
- **Caching**: No caching implemented (each request is fresh)

##  Security

- API keys are stored in the code (consider using environment variables for production)
- All API calls use HTTPS
- No user data is stored or logged

##  License

This project is for educational and research purposes.

##  Contributing

Feel free to submit issues, feature requests, or pull requests to improve the tool.

##  Support

If you encounter any issues:
1. Check the troubleshooting section
2. Run the test suite to identify problems
3. Verify your API keys and quotas
4. Check the debug information in the app

---

**Happy Researching! **
