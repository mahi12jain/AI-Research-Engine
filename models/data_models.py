# models/data_models.py
"""Data models for the AI Research Tool"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional, Any

@dataclass
class APIKeys:
    """API keys configuration"""
    google: str
    google_search: Optional[str] = None
    news: Optional[str] = None
    twitter: Optional[str] = None
    market: Optional[str] = None
    deepseek: Optional[str] = None  # Keep for backward compatibility

@dataclass
class ResearchResult:
    """Results from AI research analysis"""
    topic: str
    timestamp: datetime
    summary: str
    market_analysis: str
    technical_details: str
    business_opportunities: str
    key_players: List[str]
    trends: List[str]
    latest_news: List[Dict[str, Any]]
    confidence_score: float
    sources: List[str]  # URLs or references to data sources