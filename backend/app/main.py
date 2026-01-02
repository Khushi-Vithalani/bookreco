from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import Base, engine
from .routers.books import router as books_router

import os

app = FastAPI(title="BookReco API")

# MVP: create tables automatically
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/debug/db-url")
def debug_db_url():
    return {"DATABASE_URL": os.getenv("DATABASE_URL")}

app.include_router(books_router)

from .db import SessionLocal
from sqlalchemy import text

@app.get("/debug/book-count")
def debug_book_count():
    db = SessionLocal()
    try:
        count = db.execute(text("SELECT COUNT(*) FROM books")).scalar()
        return {"count": int(count)}
    finally:
        db.close()