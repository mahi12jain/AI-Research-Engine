# services/gemini_client.py - GEMINI VERSION
"""Google Gemini AI client for research analysis (REST-based)"""

import aiohttp
import asyncio
import logging
from config.settings import GEMINI_API_URL, GEMINI_MODEL, GEMINI_MAX_TOKENS, GEMINI_TEMPERATURE

logger = logging.getLogger(__name__)

class GeminiClient:
	"""Google Gemini API client for research analysis"""
	
	def __init__(self, api_key: str):
		self.api_key = api_key
		self.base_url = GEMINI_API_URL
		# Gemini uses API key as query parameter, not in headers
		self.headers = {
			"Content-Type": "application/json"
		}
	
	async def test_connection(self) -> dict:
		"""Test Gemini API connection and key validity"""
		try:
			async with aiohttp.ClientSession() as session:
				# Gemini API endpoint format
				url = f"{self.base_url}/{GEMINI_MODEL}:generateContent?key={self.api_key}"
				
				test_data = {
					"contents": [
						{
							"parts": [
								{
									"text": "Say 'API Test Successful' if you can read this."
								}
							]
						}
					],
					"generationConfig": {
						"maxOutputTokens": 50,
						"temperature": 0.1
					}
				}
				
				async with session.post(
					url,
					headers=self.headers,
					json=test_data,
					timeout=30
				) as response:
					
					response_text = await response.text()
					
					if response.status == 200:
						result = await response.json()
						# Extract content from Gemini response format
						content = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
						return {
							"success": True,
							"status_code": response.status,
							"response": content,
							"model": GEMINI_MODEL,
							"usage": result.get("usageMetadata", {})
						}
					else:
						return {
							"success": False,
							"status_code": response.status,
							"error": response_text,
							"headers": dict(response.headers)
						}
						
		except asyncio.TimeoutError:
			return {
				"success": False,
				"error": "Request timeout - API might be slow or unresponsive"
			}
		except Exception as e:
			return {
				"success": False,
				"error": f"Connection error: {str(e)}"
			}
	
	async def generate_response(self, prompt: str, max_tokens: int = GEMINI_MAX_TOKENS) -> str:
		"""Generate response using Google Gemini (REST)"""
		try:
			async with aiohttp.ClientSession() as session:
				# Gemini API endpoint format
				url = f"{self.base_url}/{GEMINI_MODEL}:generateContent?key={self.api_key}"
				
				# Combine system prompt with user prompt for Gemini
				full_prompt = f"{self._get_system_prompt()}\n\nUser Query: {prompt}"
				
				data = {
					"contents": [
						{
							"parts": [
								{
									"text": full_prompt
								}
							]
						}
					],
					"generationConfig": {
						"maxOutputTokens": max_tokens,
						"temperature": GEMINI_TEMPERATURE,
						"topK": 40,
						"topP": 0.95
					},
					"safetySettings": [
						{
							"category": "HARM_CATEGORY_HARASSMENT",
							"threshold": "BLOCK_MEDIUM_AND_ABOVE"
						},
						{
							"category": "HARM_CATEGORY_HATE_SPEECH",
							"threshold": "BLOCK_MEDIUM_AND_ABOVE"
						},
						{
							"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
							"threshold": "BLOCK_MEDIUM_AND_ABOVE"
						},
						{
							"category": "HARM_CATEGORY_DANGEROUS_CONTENT",
							"threshold": "BLOCK_MEDIUM_AND_ABOVE"
						}
					]
				}
				
				# Add timeout
				timeout = aiohttp.ClientTimeout(total=120)  # 2 minutes timeout
				
				async with session.post(
					url,
					headers=self.headers,
					json=data,
					timeout=timeout
				) as response:
					
					if response.status == 200:
						result = await response.json()
						
						# Check if response was blocked by safety filters
						if "candidates" not in result or not result["candidates"]:
							return "Error: Response was blocked by safety filters. Please try rephrasing your query."
						
						# Extract content from Gemini response format
						content = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
						
						# Log successful response
						logger.info(f"Gemini response length: {len(content)} characters")
						
						return content
					else:
						error_text = await response.text()
						logger.error(f"Gemini API error {response.status}: {error_text}")
						return f"API Error {response.status}: {error_text}"
						
		except asyncio.TimeoutError:
			logger.error("Gemini API timeout")
			return "Error: Request timeout. The API is taking too long to respond."
		except Exception as e:
			logger.error(f"Gemini API exception: {e}")
			return f"Error: {str(e)}"
	
	def _get_system_prompt(self) -> str:
		"""Enhanced system prompt optimized for accurate AI research analysis"""
		return """You are an elite AI Research Analyst. Provide structured research analysis in the following format:

1. EXECUTIVE SUMMARY
[Provide 200-300 word comprehensive overview]

2. MARKET ANALYSIS  
[Provide detailed market intelligence including size, growth, competitors]

3. TECHNICAL DETAILS
[Explain technical aspects, architecture, implementation]

4. BUSINESS OPPORTUNITIES
[List specific business opportunities and project suggestions]

5. KEY PLAYERS
[List major companies/organizations]

6. TRENDS
[List 3-5 key trends]

IMPORTANT: Always use the exact section headers above. Structure your response clearly with these sections."""
