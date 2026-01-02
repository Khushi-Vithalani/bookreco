from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ..db import get_db
from ..models import Book

router = APIRouter(prefix="/books", tags=["books"])

@router.get("")
def list_books(
    q: str | None = Query(default=None, description="Search by title/author"),
    fiction: bool | None = Query(default=None, description="true=fiction, false=non-fiction"),
    limit: int = Query(default=30, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    query = db.query(Book)

    if q:
        like = f"%{q}%"
        query = query.filter(or_(Book.title.ilike(like), Book.authors.ilike(like)))

    if fiction is not None:
        query = query.filter(Book.fiction == fiction)

    total = query.count()
    books = query.order_by(Book.id.desc()).offset(offset).limit(limit).all()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": [
            {
                "id": b.id,
                "title": b.title,
                "authors": b.authors.split("|") if b.authors else [],
                "fiction": b.fiction,
                "year": b.year,
                "cover_url": b.cover_url,
                "tags": b.tags.split("|") if b.tags else [],
            }
            for b in books
        ],
    }

@router.get("/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    b = db.query(Book).filter(Book.id == book_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Book not found")

    return {
        "id": b.id,
        "title": b.title,
        "authors": b.authors.split("|") if b.authors else [],
        "fiction": b.fiction,
        "description": b.description,
        "year": b.year,
        "cover_url": b.cover_url,
        "tags": b.tags.split("|") if b.tags else [],
    }