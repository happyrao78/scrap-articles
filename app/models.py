"""Database models."""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.base import Base

class Article(Base):
    """Article model for storing scraped and summarized content."""
    
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    author = Column(String(200), nullable=True)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    source_url = Column(String(1000), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "content": self.content,
            "summary": self.summary,
            "source_url": self.source_url,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }