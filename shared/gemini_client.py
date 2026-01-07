"""
Unified Gemini Client for OpenAnalytics.

Provides:
- Structured output generation (JSON)
- Search grounding for mentions
- OpenAI-compatible message format
"""

import os
import json
import logging
import httpx
from typing import List, Dict, Any, Optional
from google import genai
from dotenv import load_dotenv

from .constants import GEMINI_MODEL

logger = logging.getLogger(__name__)


class GeminiClient:
    """Gemini client using the google-genai SDK."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini client.

        Args:
            api_key: Optional API key. If not provided, uses GEMINI_API_KEY env var.
        """
        load_dotenv('.env.local')

        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")

        self.client = genai.Client(api_key=self.api_key)
        self.serper_api_key = os.getenv('SERPER_API_KEY')

        logger.info("GeminiClient initialized with google-genai SDK")

    async def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        model: str = GEMINI_MODEL,
        json_output: bool = False,
        temperature: float = 0.3,
        max_tokens: int = 8192,
        use_search: bool = False,
    ) -> Dict[str, Any]:
        """Generate content with Gemini.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            model: Gemini model to use
            json_output: Request JSON output
            temperature: Generation temperature
            max_tokens: Maximum output tokens
            use_search: Enable web search grounding

        Returns:
            Dict with success, response, and metadata
        """
        try:
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"

            if json_output:
                full_prompt += "\n\nReturn your response as valid JSON."

            if use_search and self._needs_web_search(prompt):
                response = await self._generate_with_search(full_prompt, model)
            else:
                response = self.client.models.generate_content(
                    model=model,
                    contents=full_prompt
                )

            return {
                "success": True,
                "response": response.text,
                "model": model
            }

        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": ""
            }

    async def query_with_structured_output(
        self,
        prompt: str,
        system_prompt: str = "",
        model: str = GEMINI_MODEL,
        response_format: str = "json",
        **kwargs
    ) -> Dict[str, Any]:
        """Generate structured output (JSON) from prompt.

        Alias for generate() with json_output=True for compatibility.
        """
        return await self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            model=model,
            json_output=(response_format == "json"),
            **kwargs
        )

    async def complete(
        self,
        messages: List[Dict[str, str]],
        model: str = GEMINI_MODEL,
        **kwargs
    ) -> Any:
        """OpenAI-compatible completion interface.

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model to use

        Returns:
            OpenAI-compatible response object
        """
        try:
            prompt = self._convert_messages_to_prompt(messages)

            response = self.client.models.generate_content(
                model=model,
                contents=prompt
            )

            class MockChoice:
                def __init__(self, content):
                    self.message = MockMessage(content)

            class MockMessage:
                def __init__(self, content):
                    self.content = content

            class MockResponse:
                def __init__(self, content):
                    self.choices = [MockChoice(content)]

            return MockResponse(response.text)

        except Exception as e:
            logger.error(f"Gemini completion error: {e}")
            raise

    async def query_mentions_with_search_grounding(
        self,
        query: str,
        company_name: str
    ) -> Dict[str, Any]:
        """Query for company mentions with search grounding.

        Main method for AEO mentions check.
        """
        try:
            prompt = f"""I need information about "{query}".

Please search the web and provide information about the best companies, tools, or platforms related to this query. Focus on:
1. Which companies or platforms are mentioned as top options
2. What specific features and services they offer
3. Any rankings, reviews, or recommendations
4. Market leaders and popular choices

Please include specific company names and details about their capabilities."""

            response = await self._generate_with_search(prompt)

            return {
                "success": True,
                "response": response.text,
                "model": GEMINI_MODEL,
                "search_grounding": True
            }

        except Exception as e:
            logger.error(f"Gemini mentions query error: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": "",
                "search_grounding": False
            }

    async def _generate_with_search(
        self,
        prompt: str,
        model: str = GEMINI_MODEL
    ):
        """Generate with web search grounding."""
        try:
            if self.serper_api_key:
                return await self._generate_with_serper(prompt, model)
            else:
                logger.warning("No Serper API key, using regular Gemini")
                return self.client.models.generate_content(
                    model=model,
                    contents=prompt
                )
        except Exception as e:
            logger.warning(f"Search generation failed: {e}, using regular Gemini")
            return self.client.models.generate_content(
                model=model,
                contents=prompt
            )

    async def _generate_with_serper(self, prompt: str, model: str = GEMINI_MODEL):
        """Generate with Serper search fallback."""
        try:
            search_query = self._extract_search_terms(prompt)
            search_results = await self._serper_search(search_query)

            enhanced_prompt = f"{prompt}\n\nBased on these search results:\n{search_results}"

            return self.client.models.generate_content(
                model=model,
                contents=enhanced_prompt
            )

        except Exception as e:
            logger.warning(f"Serper fallback failed: {e}")
            return self.client.models.generate_content(
                model=model,
                contents=prompt
            )

    async def _serper_search(self, query: str) -> str:
        """Search using Serper API."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://google.serper.dev/search",
                    headers={
                        "X-API-KEY": self.serper_api_key,
                        "Content-Type": "application/json"
                    },
                    json={"q": query, "num": 5}
                )

                if response.status_code == 200:
                    data = response.json()
                    results = []
                    for item in data.get("organic", []):
                        results.append(f"- {item.get('title', '')}: {item.get('snippet', '')}")
                    return "\n".join(results)
                else:
                    logger.error(f"Serper API error: {response.status_code}")
                    return ""
        except Exception as e:
            logger.error(f"Serper search error: {e}")
            return ""

    def _convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert OpenAI-style messages to single prompt."""
        parts = []
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")

            if role == "system":
                parts.append(f"System: {content}")
            elif role == "user":
                parts.append(f"User: {content}")
            elif role == "assistant":
                parts.append(f"Assistant: {content}")

        return "\n\n".join(parts)

    def _needs_web_search(self, prompt: str) -> bool:
        """Determine if prompt needs web search."""
        search_indicators = [
            "search the web", "find information", "latest", "current",
            "best companies", "top companies", "alternatives to",
            "information about", "details about", "companies that",
            "tools for", "platforms for", "services for"
        ]

        prompt_lower = prompt.lower()
        return any(indicator in prompt_lower for indicator in search_indicators)

    def _extract_search_terms(self, prompt: str) -> str:
        """Extract relevant search terms from prompt."""
        import re

        quoted = re.findall(r'"([^"]*)"', prompt)
        if quoted:
            return quoted[0]

        info_match = re.search(r'information about (.+?)[\.\?]', prompt, re.IGNORECASE)
        if info_match:
            return info_match.group(1).strip()

        best_match = re.search(r'(?:best|top) (.+?) (?:for|in)', prompt, re.IGNORECASE)
        if best_match:
            return best_match.group(1).strip()

        sentences = prompt.split('.')
        if sentences:
            return sentences[0][:100]

        return prompt[:100]


# Singleton instance
_gemini_client = None


def get_gemini_client() -> GeminiClient:
    """Get singleton Gemini client instance."""
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    return _gemini_client
