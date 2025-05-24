import re
import logging
from typing import List

logger = logging.getLogger(__name__)

def postprocess_summary(summary: str, max_sentences: int = 5) -> str:
    """
    Post-process Gemini API summary output.
    
    Args:
        summary: Raw summary from Gemini API
        max_sentences: Maximum number of sentences to keep
    
    Returns:
        Clean, processed summary
    """
    if not summary:
        return ""
    
    try:
        # Remove extra whitespace and newlines
        summary = re.sub(r'\s+', ' ', summary).strip()
        
        # Remove markdown formatting that might come from Gemini
        summary = re.sub(r'\*\*(.*?)\*\*', r'\1', summary)  # Bold
        summary = re.sub(r'\*(.*?)\*', r'\1', summary)      # Italic
        summary = re.sub(r'`(.*?)`', r'\1', summary)        # Code
        
        # Remove bullet points and list formatting
        summary = re.sub(r'^[-•*]\s+', '', summary, flags=re.MULTILINE)
        summary = re.sub(r'^\d+\.\s+', '', summary, flags=re.MULTILINE)
        
        # Split into sentences
        sentences = split_sentences(summary)
        
        # Limit to max_sentences
        if len(sentences) > max_sentences:
            sentences = sentences[:max_sentences]
        
        # Join sentences back together
        processed_summary = ' '.join(sentences).strip()
        
        # Ensure proper sentence ending
        if processed_summary and not processed_summary.endswith('.'):
            processed_summary += '.'
        
        logger.debug(f"Post-processed summary: {len(processed_summary)} characters")
        return processed_summary
        
    except Exception as e:
        logger.error(f"Error post-processing summary: {str(e)}")
        return summary  # Return original if post-processing fails

def split_sentences(text: str) -> List[str]:
    """
    Split text into sentences.
    
    Args:
        text: Text to split
    
    Returns:
        List of sentences
    """
    # Simple sentence splitting based on periods, exclamation marks, and question marks
    # followed by whitespace and capital letters
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    
    # Clean up sentences
    cleaned_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and len(sentence) > 5:  # Filter out very short fragments
            cleaned_sentences.append(sentence)
    
    return cleaned_sentences

def clean_formatting(text: str) -> str:
    """
    Remove various formatting artifacts.
    
    Args:
        text: Text with formatting
    
    Returns:
        Clean text without formatting
    """
    # Remove markdown
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'`(.*?)`', r'\1', text)
    
    # Remove HTML entities
    text = re.sub(r'&[a-zA-Z]+;', '', text)
    
    # Remove extra punctuation
    text = re.sub(r'[.]{2,}', '.', text)
    text = re.sub(r'[!]{2,}', '!', text)
    text = re.sub(r'[?]{2,}', '?', text)
    
    return text.strip()

def ensure_sentence_completion(text: str) -> str:
    """
    Ensure text ends with proper punctuation.
    
    Args:
        text: Input text
    
    Returns:
        Text with proper ending punctuation
    """
    if not text:
        return text
    
    text = text.strip()
    if text and not text.endswith(('.', '!', '?')):
        text += '.'
    
    return text

def limit_length(text: str, max_chars: int = 500) -> str:
    """
    Limit text length while preserving sentence boundaries.
    
    Args:
        text: Input text
        max_chars: Maximum character length
    
    Returns:
        Truncated text
    """
    if len(text) <= max_chars:
        return text
    
    # Find the last complete sentence within the limit
    truncated = text[:max_chars]
    last_sentence_end = max(
        truncated.rfind('.'),
        truncated.rfind('!'),
        truncated.rfind('?')
    )
    
    if last_sentence_end > max_chars * 0.7:  # If we found a sentence end reasonably close
        return text[:last_sentence_end + 1]
    else:
        return truncated + '...'