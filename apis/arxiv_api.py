# apis/arxiv_api.py
"""ArXiv API integration for academic papers"""

import aiohttp
import logging
from typing import List, Dict
from config.settings import ARXIV_API_URL, DEFAULT_ACADEMIC_RESULTS

logger = logging.getLogger(__name__)

class ArxivAPI:
    def __init__(self):
        self.base_url = ARXIV_API_URL
    
    async def search(self, query: str, max_results: int = DEFAULT_ACADEMIC_RESULTS) -> List[Dict]:
        """Search ArXiv for academic papers"""
        try:
            params = {
                'search_query': f'all:{query}',
                'start': 0,
                'max_results': max_results,
                'sortBy': 'submittedDate',
                'sortOrder': 'descending'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        content = await response.text()
                        # Parse XML response (simplified)
                        papers = self._parse_arxiv_xml(content)
                        return papers
            return []
        except Exception as e:
            logger.error(f"ArXiv API error: {e}")
            return []
    
    def _parse_arxiv_xml(self, xml_content: str) -> List[Dict]:
        """Parse ArXiv XML response (simplified version)"""
        papers = []
        # Simple parsing - in production use xml.etree.ElementTree
        try:
            # This is a simplified version
            # For full implementation, use proper XML parsing
            lines = xml_content.split('\n')
            current_paper = {}
            
            for line in lines:
                if '<title>' in line and '</title>' in line:
                    title = line.split('<title>')[1].split('</title>')[0].strip()
                    current_paper['title'] = title
                    current_paper['source'] = 'ArXiv'
                
                if current_paper and len(current_paper) >= 2:
                    papers.append(current_paper)
                    current_paper = {}
                    if len(papers) >= 5:  # Limit results
                        break
        except Exception as e:
            logger.error(f"ArXiv XML parsing error: {e}")
        
        return papers