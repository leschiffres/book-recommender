from book_recommender.recommender import BookRecommender
import os
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

POSTGRES_CONFIG = {
    "host": os.environ['DB_HOST'],
    "port": os.environ['DB_PORT'],
    "user": os.environ['DB_USER'],
    "password": os.environ['DB_PASSWORD'],
    "database": os.environ['DB_NAME'],
}

if __name__ == "__main__":
    # br = BookRecommender(POSTGRES_CONFIG, load_from_db=False)
    br = BookRecommender(POSTGRES_CONFIG, load_from_db=True)
    while True:
        desc = input("Please give your description about a book that you want to read:\n")
        books = br.recommend_books(desc)
        import ipdb; ipdb.set_trace()
        