from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import string
import random

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

url_store = {}

class URLRequest(BaseModel):
    original_url: str

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.post("/shorten")
def shorten_url(request: URLRequest):
    short_code = generate_short_code()
    url_store[short_code] = request.original_url
    return {"short_url": f"http://localhost:8000/{short_code}"}

@app.get("/{short_code}")
def redirect_url(short_code: str):
    if short_code in url_store:
        return RedirectResponse(url_store[short_code])
    return {"error": "URL not found"}
