# config/settings.py
"""Configuration settings for AI Research Tool"""

# API Endpoints
DEEPSEEK_API_URL = "https://api.deepseek.com/v1"
GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"
NEWS_API_URL = "https://newsapi.org/v2"
ARXIV_API_URL = "http://export.arxiv.org/api/query"
PATENT_API_URL = "https://api.patentsview.org/patents/query"
TWITTER_API_URL = "https://api.twitter.com/2"

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"
GEMINI_MODEL = "gemini-1.5-pro-latest"  # or "gemini-1.5-flash-latest" for faster responses
GEMINI_MAX_TOKENS = 8192
GEMINI_TEMPERATURE = 0.7

# Default Parameters
DEFAULT_MAX_RESULTS = 10
DEFAULT_NEWS_RESULTS = 20
DEFAULT_ACADEMIC_RESULTS = 10
DEFAULT_PATENT_RESULTS = 10
DEFAULT_SOCIAL_RESULTS = 50

# DeepSeek Parameters
DEEPSEEK_MODEL = "deepseek-chat"
DEEPSEEK_MAX_TOKENS = 3000
DEEPSEEK_TEMPERATURE = 0.3

# Logging Configuration
LOGGING_LEVEL = "INFO"
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Streamlit Configuration
PAGE_TITLE = "AI Research Engine"
PAGE_ICON = "🔬"
LAYOUT = "wide"