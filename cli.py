import click
import logging
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.database import SessionLocal, init_db, delete_articles_by_ids
from app.scrapping.scraper import scrape_articles
from app.processing.preprocessor import preprocess_text
from app.processing.postprocessor import postprocess_summary
from app.gemini.client import get_gemini_client
from app.models import Article

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.group()
def cli():
    pass

@cli.command()
@click.option('--url', '-u', required=True, help='URL to scrape articles from')
@click.option('--limit', '-l', default=5, help='Maximum number of articles to scrape')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')

def scrape(url: str, limit: int, verbose: bool):
    """Scrape articles from a URL and store them with summaries."""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize database
        init_db()
        db = SessionLocal()
        
        click.echo(f"Scraping articles from: {url}")
        click.echo(f"Limit: {limit} articles")
        
        # Scrape articles
        scraped_articles = scrape_articles(url, limit)
        
        if not scraped_articles:
            click.echo("No articles found at the provided URL")
            return
        
        click.echo(f"Found {len(scraped_articles)} articles")
        
        # Get Gemini client
        gemini_client = get_gemini_client()
        processed_count = 0
        
        with click.progressbar(scraped_articles, label='Processing articles') as articles:
            for article_data in articles:
                try:
                    # Preprocess content
                    preprocessed_content = preprocess_text(article_data['content'])
                    
                    # Summarize with Gemini
                    summary = gemini_client.summarize_article(
                        title=article_data['title'],
                        content=preprocessed_content,
                        author=article_data.get('author')
                    )
                    
                    # Post-process summary
                    final_summary = postprocess_summary(summary)
                    
                    # Store in database
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
                    
                    processed_count += 1
                    
                    if verbose:
                        click.echo(f"\n Processed: {article.title}")
                        click.echo(f" Summary: {final_summary[:100]}...")
                        
                except Exception as e:
                    logger.error(f"Error processing article: {str(e)}")
                    continue
        
        click.echo(f"\n Successfully processed {processed_count} articles!")
        
    except Exception as e:
        click.echo(f" Error: {str(e)}")
    finally:
        db.close()

@cli.command()
@click.option('--id', '-i', required=True, type=int, help='Article ID to retrieve')

def get_summary(id: int):
    """Get article summary by ID."""
    try:
        # Initialize database
        init_db()
        db = SessionLocal()
        
        article = db.query(Article).filter(Article.id == id).first()
        
        if not article:
            click.echo(f" Article with ID {id} not found")
            return
        
        click.echo(f"\n Title: {article.title}")
        click.echo(f"  Author: {article.author}")
        click.echo(f" Source: {article.source_url}")
        click.echo(f" Created: {article.created_at}")
        click.echo(f"\n Summary:")
        click.echo(f"{article.summary}")
        click.echo(f"\n Original Content (first 200 chars):")
        click.echo(f"{article.content[:200]}...")
        
    except Exception as e:
        click.echo(f" Error: {str(e)}")
    finally:
        db.close()

@cli.command()

@click.option('--limit', '-l', default=10, help='Maximum number of articles to list')
def list_articles(limit: int):
    """List all stored articles."""
    try:
        # Initialize database
        init_db()
        db = SessionLocal()
        
        articles = db.query(Article).limit(limit).all()
        
        if not articles:
            click.echo(" No articles found in database")
            return
        
        click.echo(f"\n Found {len(articles)} articles:")
        click.echo("-" * 80)
        
        for article in articles:
            click.echo(f" ID: {article.id}")
            click.echo(f" Title: {article.title}")
            click.echo(f"  Author: {article.author}")
            click.echo(f" Created: {article.created_at}")
            click.echo(f" Summary: {article.summary[:100]}...")
            click.echo("-" * 80)
        
    except Exception as e:
        click.echo(f" Error: {str(e)}")
    finally:
        db.close()

@cli.command()

@click.option('--id', '-i', required=True, type=int, help='Article ID to delete')
@click.confirmation_option(prompt='Are you sure you want to delete this article?')
def delete_article(id: int):
    """Delete an article by ID."""
    try:
        # Initialize database
        init_db()
        db = SessionLocal()
        
        article = db.query(Article).filter(Article.id == id).first()
        
        if not article:
            click.echo(f" Article with ID {id} not found")
            return
        
        title = article.title
        db.delete(article)
        db.commit()
        
        click.echo(f" Deleted article: {title}")
        
    except Exception as e:
        click.echo(f" Error: {str(e)}")
    finally:
        db.close()

@cli.command()

def init_database():
    """Initialize the database and create tables."""
    try:
        init_db()
        click.echo(" Database initialized successfully!")
    except Exception as e:
        click.echo(f" Error initializing database: {str(e)}")

@cli.command()
def test_gemini():
    """Test Gemini API connection."""
    try:
        gemini_client = get_gemini_client()
        test_text = "This is a test text to check if Gemini API is working properly."
        summary = gemini_client.summarize_text(test_text)
        
        click.echo(" Gemini API connection successful!")
        click.echo(f" Test summary: {summary}")
        
    except Exception as e:
        click.echo(f" Gemini API error: {str(e)}")

@cli.command()
@click.option('--ids', '-i', multiple=True, type=int, help="IDs of articles to delete")
@click.confirmation_option(prompt='Are you sure you want to delete these articles?')
def delete_articles(ids):
    """Delete multiple articles by their IDs."""
    try:
        # Initialize database
        init_db()
        db = SessionLocal()

        if not ids:
            click.echo(" No IDs provided. Use --ids to specify article IDs.")
            return

        articles = db.query(Article).filter(Article.id.in_(ids)).all()

        if not articles:
            click.echo(f" No articles found for the provided IDs: {ids}")
            return

        for article in articles:
            db.delete(article)
            click.echo(f" Deleted article: {article.title} (ID: {article.id})")

        db.commit()
        click.echo(" All specified articles have been deleted successfully!")

    except Exception as e:
        click.echo(f" Error: {str(e)}")
    finally:
        db.close()
if __name__ == '__main__':
    cli()