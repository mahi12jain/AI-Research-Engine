# utils/helpers.py
"""Helper functions for data processing and analysis"""

import re
from typing import Dict, List

def extract_sections(response: str) -> Dict[str, str]:
    """Extract different sections from AI response"""
    sections = {}
    
    # Simple section extraction based on headers
    current_section = None
    current_content = []
    
    for line in response.split('\n'):
        line = line.strip()
        
        # Check for section headers
        if any(keyword in line.lower() for keyword in [
            'executive summary', 'technical analysis', 'market analysis',
            'business opportunities', 'latest developments', 'future outlook'
        ]):
            # Save previous section
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            
            # Start new section
            current_section = line.lower().replace(' ', '_').replace(':', '')
            current_content = []
        else:
            if line:  # Skip empty lines
                current_content.append(line)
    
    # Save last section
    if current_section:
        sections[current_section] = '\n'.join(current_content)
    
    return sections

def extract_key_players(sections: Dict[str, str]) -> List[str]:
    """Extract key players from analysis"""
    players = []
    market_text = sections.get('market_analysis', '')
    
    # Look for common company name patterns
    company_patterns = [
        r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b',  # Two-word company names
        r'\b([A-Z]{2,})\b',  # Acronyms (MSFT, GOOGL, etc.)
        r'\b(Apple|Google|Microsoft|Amazon|Meta|Tesla|Netflix|Adobe)\b'  # Known companies
    ]
    
    for pattern in company_patterns:
        matches = re.findall(pattern, market_text)
        players.extend(matches)
    
    # Remove duplicates and limit to 5
    return list(set(players))[:5]

def extract_trends(sections: Dict[str, str]) -> List[str]:
    """Extract trends from analysis"""
    trends = []
    
    # Look in future outlook and latest developments
    trend_sections = [
        sections.get('future_outlook', ''),
        sections.get('latest_developments', ''),
        sections.get('technical_analysis', '')
    ]
    
    for section_text in trend_sections:
        # Split by sentences and filter meaningful ones
        sentences = section_text.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            # Look for trend indicators
            if any(indicator in sentence.lower() for indicator in [
                'trend', 'growing', 'increasing', 'emerging', 'rising',
                'adoption', 'shift', 'evolution', 'advancement'
            ]):
                if len(sentence) > 20:  # Filter out short fragments
                    trends.append(sentence)
    
    return trends[:5]  # Limit to 5 trends

def clean_text(text: str) -> str:
    """Clean and format text"""
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    return text.strip()

def format_currency(amount: str) -> str:
    """Format currency amounts"""
    try:
        # Simple formatting for common currency patterns
        if 'billion' in amount.lower() or 'b' in amount.lower():
            return f"${amount}B"
        elif 'million' in amount.lower() or 'm' in amount.lower():
            return f"${amount}M"
        else:
            return amount
    except:
        return amount