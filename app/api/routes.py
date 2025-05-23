"""API routes for the FastAPI application."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging

from app.database import get_db, delete_articles_by_ids
from app.models import Article
from app.scrapping.scraper import scrape_articles
from app.processing.preprocessor import preprocess_text
from app.processing.postprocessor import postprocess_summary
from app.gemini.client import get_gemini_client
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic models for request/response
class ScrapeRequest(BaseModel):
    url: str
    limit: int = 5

class ScrapeResponse(BaseModel):
    message: str
    articles_processed: int
    article_ids: List[int]

class ArticleResponse(BaseModel):
    id: int
    title: str
    author: str
    content: str
    summary: str
    source_url: str
    created_at: str

@router.post("/scrape-and-summarize", response_model=ScrapeResponse)
async def scrape_and_summarize(request: ScrapeRequest, db: Session = Depends(get_db)):
    """
    Scrape articles from a URL and summarize them using Gemini API.
    
    Args:
        request: ScrapeRequest containing URL and limit
        db: Database session
    
    Returns:
        Response with processing results
    """
    try:
        logger.info(f"Starting scrape and summarize for URL: {request.url}")
        
        # Step 1: Scrape articles
        scraped_articles = scrape_articles(request.url, request.limit)
        
        if not scraped_articles:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No articles found at the provided URL"
            )
        
        # Get Gemini client
        gemini_client = get_gemini_client()
        processed_article_ids = []
        
        # Process each scraped article
        for article_data in scraped_articles:
            try:
                # Step 2: Preprocess content
                preprocessed_content = preprocess_text(article_data['content'])
                
                # Step 3: Summarize with Gemini
                summary = gemini_client.summarize_article(
                    title=article_data['title'],
                    content=preprocessed_content,
                    author=article_data.get('author')
                )
                
                # Step 4: Post-process summary
                final_summary = postprocess_summary(summary)
                
                # Step 5: Store in database
                article = Article(
                    title=article_data['title'],
                    author=article_data.get('author', 'Unknown'),
                    content=article_data['content'],
                    summary=final_summary,
                    source_url=article_data['source_url']
                )
                
                db.add(article)
                db.commit()
                db.refresh(article)
                
                processed_article_ids.append(article.id)
                logger.info(f"Processed and stored article: {article.id}")
                
            except Exception as e:
                logger.error(f"Error processing article '{article_data.get('title', 'Unknown')}': {str(e)}")
                continue
        
        return ScrapeResponse(
            message=f"Successfully processed {len(processed_article_ids)} articles",
            articles_processed=len(processed_article_ids),
            article_ids=processed_article_ids
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in scrape_and_summarize: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/get-summary/{article_id}", response_model=ArticleResponse)
async def get_summary_by_id(article_id: int, db: Session = Depends(get_db)):
    """
    Get article summary by ID.
    
    Args:
        article_id: ID of the article
        db: Database session
    
    Returns:
        Article with summary
    """
    try:
        article = db.query(Article).filter(Article.id == article_id).first()
        
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Article with ID {article_id} not found"
            )
        
        return ArticleResponse(
            id=article.id,
            title=article.title,
            author=article.author or "Unknown",
            content=article.content,
            summary=article.summary,
            source_url=article.source_url,
            created_at=article.created_at.isoformat() if article.created_at else ""
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting article {article_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/articles", response_model=List[ArticleResponse])
async def get_all_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all articles with pagination.
    
    Args:
        skip: Number of articles to skip
        limit: Maximum number of articles to return
        db: Database session
    
    Returns:
        List of articles
    """
    try:
        articles = db.query(Article).offset(skip).limit(limit).all()
        
        return [
            ArticleResponse(
                id=article.id,
                title=article.title,
                author=article.author or "Unknown",
                content=article.content,
                summary=article.summary,
                source_url=article.source_url,
                created_at=article.created_at.isoformat() if article.created_at else ""
            )
            for article in articles
        ]
        
    except Exception as e:
        logger.error(f"Error getting articles: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running"}

@router.delete("/articles/{article_id}")
async def delete_article(article_id: int, db: Session = Depends(get_db)):
    """
    Delete an article by ID.
    
    Args:
        article_id: ID of the article to delete
        db: Database session
    
    Returns:
        Success message
    """
    try:
        article = db.query(Article).filter(Article.id == article_id).first()
        
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Article with ID {article_id} not found"
            )
        
        db.delete(article)
        db.commit()
        
        return {"message": f"Article {article_id} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting article {article_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.delete("/api/v1/articles")
async def delete_articles(ids: list[int], db: Session = Depends(get_db)):
    """
    Delete multiple articles by their IDs.
    """
    if not ids:
        raise HTTPException(status_code=400, detail="No IDs provided.")

    success = delete_articles_by_ids(db, ids)
    if not success:
        raise HTTPException(status_code=404, detail="No articles found for the provided IDs.")

    return {"message": "Articles deleted successfully."}

# Database utility functions
def store_article(data: Dict[str, str], db: Session) -> Article:
    """
    Store article data in the database.
    
    Args:
        data: Article data dictionary
        db: Database session
    
    Returns:
        Created Article instance
    """
    article = Article(
        title=data.get('title', 'Untitled'),
        author=data.get('author', 'Unknown'),
        content=data.get('content', ''),
        summary=data.get('summary', ''),
        source_url=data.get('source_url', '')
    )
    
    db.add(article)
    db.commit()
    db.refresh(article)
    
    return article

def get_summary_by_id_util(article_id: int, db: Session) -> Dict[str, Any]:
    """
    Utility function to get article summary by ID.
    
    Args:
        article_id: ID of the article
        db: Database session
    
    Returns:
        Article data as dictionary
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    
    if not article:
        return {}
    
    return article.to_dict()