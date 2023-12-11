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
    # Set the load_from_db to False to compute the embeddings for the first time
    br = BookRecommender(POSTGRES_CONFIG, load_from_db=False)
    while True:
        desc = input("Please give your description about a book that you want to read:\n")
        books = br.recommend_books(desc)
        import ipdb; ipdb.set_trace()
        