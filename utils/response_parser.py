# utils/response_parser.py
"""Parser for AI responses to extract structured data"""

import re
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class ResponseParser:
    """Parser for extracting structured data from AI responses"""
    
    def __init__(self):
        # Define section patterns for different AI response formats
        self.section_patterns = {
            'summary': [
                r'(?:1\.\s*)?EXECUTIVE SUMMARY[:\n]*(.*?)(?=\n(?:2\.|MARKET ANALYSIS|$))',
                r'(?:##\s*)?EXECUTIVE SUMMARY[:\n]*(.*?)(?=\n##|$)',
                r'SUMMARY[:\n]*(.*?)(?=\n(?:MARKET|ANALYSIS|$))'
            ],
            'market_analysis': [
                r'(?:2\.\s*)?MARKET ANALYSIS[:\n]*(.*?)(?=\n(?:3\.|TECHNICAL DETAILS|$))',
                r'(?:##\s*)?MARKET ANALYSIS[:\n]*(.*?)(?=\n##|$)',
                r'MARKET[:\n]*(.*?)(?=\n(?:TECHNICAL|DETAILS|$))'
            ],
            'technical_details': [
                r'(?:3\.\s*)?TECHNICAL DETAILS[:\n]*(.*?)(?=\n(?:4\.|BUSINESS OPPORTUNITIES|$))',
                r'(?:##\s*)?TECHNICAL DETAILS[:\n]*(.*?)(?=\n##|$)',
                r'TECHNICAL[:\n]*(.*?)(?=\n(?:BUSINESS|OPPORTUNITIES|$))'
            ],
            'business_opportunities': [
                r'(?:4\.\s*)?BUSINESS OPPORTUNITIES[:\n]*(.*?)(?=\n(?:5\.|KEY PLAYERS|$))',
                r'(?:##\s*)?BUSINESS OPPORTUNITIES[:\n]*(.*?)(?=\n##|$)',
                r'BUSINESS[:\n]*(.*?)(?=\n(?:KEY|PLAYERS|$))'
            ],
            'key_players': [
                r'(?:5\.\s*)?KEY PLAYERS[:\n]*(.*?)(?=\n(?:6\.|TRENDS|$))',
                r'(?:##\s*)?KEY PLAYERS[:\n]*(.*?)(?=\n##|$)',
                r'KEY PLAYERS[:\n]*(.*?)(?=\n(?:TRENDS|$))'
            ],
            'trends': [
                r'(?:6\.\s*)?TRENDS[:\n]*(.*?)(?=\n##|$)',
                r'(?:##\s*)?TRENDS[:\n]*(.*?)(?=\n##|$)',
                r'TRENDS[:\n]*(.*?)$'
            ]
        }
    
    def parse_research_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response into structured research data"""
        if not response or response.strip() == "":
            logger.warning("Empty response received")
            return self._get_empty_result()
        
        logger.info(f"Parsing response of length: {len(response)}")
        
        # Clean the response
        cleaned_response = self._clean_response(response)
        
        # Extract sections
        parsed_data = {}
        
        for section_name, patterns in self.section_patterns.items():
            content = self._extract_section(cleaned_response, patterns, section_name)
            parsed_data[section_name] = content
            
            if content:
                logger.info(f"Extracted {section_name}: {len(content)} characters")
            else:
                logger.warning(f"Failed to extract {section_name}")
        
        # Extract key players as list
        if parsed_data.get('key_players'):
            parsed_data['key_players'] = self._extract_list_items(parsed_data['key_players'])
        
        # Extract trends as list
        if parsed_data.get('trends'):
            parsed_data['trends'] = self._extract_list_items(parsed_data['trends'])
        
        return parsed_data
    
    def _clean_response(self, response: str) -> str:
        """Clean and normalize the response text"""
        # Remove extra whitespace
        cleaned = re.sub(r'\n\s*\n', '\n\n', response)
        # Remove leading/trailing whitespace
        cleaned = cleaned.strip()
        return cleaned
    
    def _extract_section(self, text: str, patterns: List[str], section_name: str) -> str:
        """Extract a specific section using multiple patterns"""
        for pattern in patterns:
            try:
                match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
                if match:
                    content = match.group(1).strip()
                    if content and len(content) > 10:  # Minimum content length
                        return content
            except Exception as e:
                logger.warning(f"Pattern failed for {section_name}: {e}")
                continue
        
        # Fallback: try to find section by header
        return self._extract_by_header(text, section_name)
    
    def _extract_by_header(self, text: str, section_name: str) -> str:
        """Fallback extraction by looking for section headers"""
        headers = {
            'summary': ['EXECUTIVE SUMMARY', 'SUMMARY'],
            'market_analysis': ['MARKET ANALYSIS', 'MARKET'],
            'technical_details': ['TECHNICAL DETAILS', 'TECHNICAL'],
            'business_opportunities': ['BUSINESS OPPORTUNITIES', 'BUSINESS'],
            'key_players': ['KEY PLAYERS', 'PLAYERS'],
            'trends': ['TRENDS']
        }
        
        section_headers = headers.get(section_name, [])
        
        for header in section_headers:
            # Look for the header
            header_pattern = rf'{header}[:\n]*(.*?)(?=\n(?:[A-Z\s]+:|$))'
            match = re.search(header_pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                content = match.group(1).strip()
                if content and len(content) > 10:
                    return content
        
        return ""
    
    def _extract_list_items(self, text: str) -> List[str]:
        """Extract list items from text"""
        items = []
        
        # Try different list patterns
        patterns = [
            r'[-]\s*(.+?)(?=\n[-]|\n\n|$)',
            r'\d+\.\s*(.+?)(?=\n\d+\.|\n\n|$)',
            r'^\s*[-]\s*(.+?)$',
            r'^\s*\d+\.\s*(.+?)$'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.MULTILINE)
            if matches:
                items.extend([match.strip() for match in matches if match.strip()])
                break
        
        # If no patterns worked, split by lines and clean
        if not items:
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if line and len(line) > 5:  # Minimum item length
                    # Remove common prefixes
                    line = re.sub(r'^[-\d\.\s]+', '', line)
                    if line:
                        items.append(line)
        
        # Remove duplicates and limit to reasonable number
        unique_items = list(dict.fromkeys(items))  # Preserve order, remove duplicates
        return unique_items[:10]  # Limit to 10 items
    
    def _get_empty_result(self) -> Dict[str, Any]:
        """Return empty result structure"""
        return {
            'summary': '',
            'market_analysis': '',
            'technical_details': '',
            'business_opportunities': '',
            'key_players': [],
            'trends': []
        }
    
    def validate_parsed_data(self, data: Dict[str, Any]) -> Dict[str, bool]:
        """Validate that all required sections were extracted"""
        validation = {}
        
        required_sections = ['summary', 'market_analysis', 'technical_details', 'business_opportunities']
        
        for section in required_sections:
            content = data.get(section, '')
            validation[section] = bool(content and len(content) > 50)
        
        # Check optional sections
        validation['key_players'] = bool(data.get('key_players'))
        validation['trends'] = bool(data.get('trends'))
        
        return validation
