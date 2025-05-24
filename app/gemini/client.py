import os
import google.generativeai as genai
import logging
import time
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class GeminiClient:
    """Client for Google Gemini API integration."""
    
    def __init__(self):
        """Initialize Gemini client with API key."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.rate_limit_delay = 1  # Delay between requests in seconds
        self.last_request_time = 0
    
    def _apply_rate_limit(self):
        """Apply rate limiting between requests."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last_request
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def summarize_text(self, text: str, max_sentences: int = 3) -> str:
        """
        Summarize text using Gemini API.
        
        Args:
            text: Text to summarize
            max_sentences: Maximum number of sentences in summary
        
        Returns:
            Summarized text
        """
        if not text or len(text.strip()) == 0:
            return "No content to summarize."
        
        try:
            self._apply_rate_limit()
            
            # Create a prompt for summarization
            prompt = f"""
            Please provide a concise summary of the following text in {max_sentences} sentences or less. 
            Focus on the main points and key information:

            Text to summarize:
            {text}

            Summary:
            """
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                summary = response.text.strip()
                logger.info(f"Generated summary with {len(summary)} characters")
                return summary
            else:
                logger.warning("Empty response from Gemini API")
                return "Unable to generate summary."
                
        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            return f"Error generating summary: {str(e)}"
    
    def summarize_article(self, title: str, content: str, author: str = None) -> str:
        """
        Summarize an article with context.
        
        Args:
            title: Article title
            content: Article content
            author: Article author (optional)
        
        Returns:
            Summarized text
        """
        if not content or len(content.strip()) == 0:
            return "No content to summarize."
        
        try:
            self._apply_rate_limit()
            
            # Create a contextual prompt
            author_text = f" by {author}" if author else ""
            prompt = f"""
            Please provide a concise 3-sentence summary of this article:

            Title: {title}{author_text}
            Content: {content}

            Focus on the main message, key points, and important details. Make the summary informative and well-structured.

            Summary:
            """
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                summary = response.text.strip()
                logger.info(f"Generated article summary: {len(summary)} characters")
                return summary
            else:
                logger.warning("Empty response from Gemini API for article")
                return "Unable to generate article summary."
                
        except Exception as e:
            logger.error(f"Error summarizing article: {str(e)}")
            return f"Error generating article summary: {str(e)}"

# Global client instance
_gemini_client: Optional[GeminiClient] = None

def get_gemini_client() -> GeminiClient:
    """Get or create Gemini client singleton."""
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    return _gemini_client

def summarize_text(text: str) -> str:
    """
    Main function to summarize text using Gemini API.
    
    Args:
        text: Text to summarize
    
    Returns:
        Summarized text
    """
    client = get_gemini_client()
    return client.summarize_text(text)