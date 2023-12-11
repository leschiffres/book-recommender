from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from typing import List
import os
from book_recommender.recommender import BookRecommender 

app = FastAPI()

# Templates configuration
templates = Jinja2Templates(directory="templates")

app.mount("/static/", StaticFiles(directory="static/"), name="static")

POSTGRES_CONFIG = {
    "host": os.environ['DB_HOST'],
    "port": os.environ['DB_PORT'],
    "user": os.environ['DB_USER'],
    "password": os.environ['DB_PASSWORD'],
    "database": os.environ['DB_NAME'],
}

book_recommender = BookRecommender(POSTGRES_CONFIG)


# books_data = [
#     {"title": "Book 1", "author": "Author 1", "description": "Description 1"},
#     {"title": "Book 2", "author": "Author 2", "description": "Description 2"},
#     # Add more books as needed
# ]


# def filter_books(search_term: str) -> List[dict]:
#     return [book for book in books_data if search_term.lower() in book["title"].lower()]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/search/", response_class=HTMLResponse)
async def search_books(request: Request, search_term: str = Form(...)):
    data = book_recommender.recommend_books(search_term)
    filtered_books = data[['book_name', 'author', 'description', 'url']].to_dict('records')
    print(filtered_books)
    return templates.TemplateResponse("results.html", {"request": request, "books": filtered_books})
