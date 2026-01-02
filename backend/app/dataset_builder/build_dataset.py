import argparse
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..models import Book
from .sources.openlibrary import search_openlibrary

def is_fiction_from_subjects(subjects: list[str]) -> bool:
    non_fiction_keywords = {
        "history", "biography", "business", "economics", "psychology", "science",
        "philosophy", "self-help", "politics", "technology", "health"
    }
    subj = " ".join(s.lower() for s in subjects)
    return not any(k in subj for k in non_fiction_keywords)

def cover_url_from_cover_i(cover_i: int | None) -> str | None:
    if not cover_i:
        return None
    return f"https://covers.openlibrary.org/b/id/{cover_i}-L.jpg"

def upsert_books(db: Session, docs: list[dict]):
    inserted = 0
    updated = 0
    skipped = 0

    for d in docs:
        title = d.get("title")
        if not title:
            skipped += 1
            continue

        ol_key = d.get("key")
        authors = d.get("author_name", [])[:5]
        subjects = d.get("subject", [])[:12]
        year = d.get("first_publish_year")
        fiction = is_fiction_from_subjects(subjects)
        cover_url = cover_url_from_cover_i(d.get("cover_i"))

        existing = db.query(Book).filter(Book.ol_key == ol_key).first() if ol_key else None
        if existing:
            existing.title = title
            existing.authors = "|".join(authors) if authors else existing.authors
            existing.tags = "|".join(subjects) if subjects else existing.tags
            existing.year = year or existing.year
            existing.cover_url = cover_url or existing.cover_url
            existing.fiction = fiction
            updated += 1
            continue

        db.add(Book(
            ol_key=ol_key,
            title=title,
            authors="|".join(authors) if authors else None,
            tags="|".join(subjects) if subjects else None,
            year=year,
            cover_url=cover_url,
            fiction=fiction,
            description=None,
        ))
        inserted += 1

    db.commit()
    return inserted, updated, skipped

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--query", required=True)
    p.add_argument("--limit", type=int, default=500)
    args = p.parse_args()

    docs = search_openlibrary(args.query, limit=args.limit)

    db = SessionLocal()
    try:
        inserted, updated, skipped = upsert_books(db, docs)
        print(f"Fetched={len(docs)} Inserted={inserted} Updated={updated} Skipped={skipped}")
    finally:
        db.close()

if __name__ == "__main__":
    main()