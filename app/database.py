import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from app.models import Article
from app.base import Base

load_dotenv()

# Database URL from environment variable
DATABASE_URL = os.getenv("DB_URL", "sqlite:///./articles.db")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        db.expire_on_commit = True
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database and create tables."""
    from app.models import Article  # Import here to avoid circular imports
    Base.metadata.create_all(bind=engine)

def delete_articles_by_ids(db: Session, ids: list[int]) -> bool:
    """Delete multiple articles by their IDs."""
    try:
        articles = db.query(Article).filter(Article.id.in_(ids)).all()
        if not articles:
            return False

        for article in articles:
            db.delete(article)

        db.commit()
        return True
    except Exception as e:
        print(f"Error deleting articles: {e}")
        return False