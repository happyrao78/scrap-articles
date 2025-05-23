"""Text preprocessing functionality."""

import re
from typing import Set
import logging

logger = logging.getLogger(__name__)

# Common English stopwords
STOPWORDS: Set[str] = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
    'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
    'to', 'was', 'will', 'with', 'this', 'but', 'they', 'have', 'had',
    'what', 'said', 'each', 'which', 'their', 'time', 'if', 'up', 'out',
    'many', 'then', 'them', 'these', 'so', 'some', 'her', 'would',
    'make', 'like', 'into', 'him', 'has', 'two', 'more', 'go', 'no',
    'way', 'could', 'my', 'than', 'first', 'been', 'call', 'who',
    'oil', 'its', 'now', 'find', 'long', 'down', 'day', 'did', 'get',
    'come', 'made', 'may', 'part'
}

def preprocess_text(text: str, remove_stopwords: bool = False) -> str:
    """
    Preprocess text by cleaning and normalizing it.
    
    Args:
        text: Raw text to preprocess
        remove_stopwords: Whether to remove stopwords
    
    Returns:
        Preprocessed text string
    """
    if not text:
        return ""
    
    try:
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove extra punctuation (keeping basic punctuation)
        text = re.sub(r'[^\w\s.,!?;:\-\'"()]', '', text)
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove stopwords if requested
        if remove_stopwords:
            words = text.split()
            text = ' '.join([word for word in words if word.lower() not in STOPWORDS])
        
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        logger.debug(f"Preprocessed text length: {len(text)} characters")
        return text
        
    except Exception as e:
        logger.error(f"Error preprocessing text: {str(e)}")
        return text  # Return original text if preprocessing fails

def clean_html(text: str) -> str:
    """
    Remove HTML tags from text.
    
    Args:
        text: Text containing HTML tags
    
    Returns:
        Text with HTML tags removed
    """
    return re.sub(r'<[^>]+>', '', text)

def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text.
    
    Args:
        text: Text with irregular whitespace
    
    Returns:
        Text with normalized whitespace
    """
    return re.sub(r'\s+', ' ', text).strip()

def remove_special_characters(text: str, keep_basic_punctuation: bool = True) -> str:
    """
    Remove special characters from text.
    
    Args:
        text: Text containing special characters
        keep_basic_punctuation: Whether to keep basic punctuation
    
    Returns:
        Text with special characters removed
    """
    if keep_basic_punctuation:
        return re.sub(r'[^\w\s.,!?;:\-\'"()]', '', text)
    else:
        return re.sub(r'[^\w\s]', '', text)