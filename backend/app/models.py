from sqlalchemy import Column, Integer, String, Boolean, Text
from .db import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    ol_key = Column(String(64), unique=True, index=True, nullable=True)
    title = Column(String(512), nullable=False, index=True)
    authors = Column(String(512), nullable=True)   # pipe-separated
    fiction = Column(Boolean, default=True)
    description = Column(Text, nullable=True)
    tags = Column(String(1024), nullable=True)     # pipe-separated
    year = Column(Integer, nullable=True)
    cover_url = Column(String(1024), nullable=True)