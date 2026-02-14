from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base, sessionmaker
import string
import random
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DATABASE_URL = "sqlite:///./urls.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"

    short_code = Column(String, primary_key=True, index=True)
    original_url = Column(String)

Base.metadata.create_all(bind=engine)

class URLRequest(BaseModel):
    original_url: str

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.post("/shorten")
def shorten_url(request: URLRequest, req: Request):
    db = SessionLocal()
    short_code = generate_short_code()

    db_url = URL(short_code=short_code, original_url=request.original_url)
    db.add(db_url)
    db.commit()
    db.close()

    base_url = str(req.base_url).rstrip("/")
    return {"short_url": f"{base_url}/{short_code}"}

@app.get("/{short_code}")
def redirect_url(short_code: str):
    db = SessionLocal()
    db_url = db.query(URL).filter(URL.short_code == short_code).first()
    db.close()

    if db_url:
        return RedirectResponse(db_url.original_url)

    return {"error": "URL not found"}
