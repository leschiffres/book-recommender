import psycopg2.extras
import pandas as pd
import os
from book_recommender.db import read_books, store_books, create_table
from book_recommender.embeddings import EmbeddingsProducer, SentenceTransformersEmbeddings
import logging
from tqdm import tqdm
import time
tqdm.pandas()

class BookRecommender():
    """
    This is a class whose main purpose is to manage the embeddings 
    i.e. compute them, store them and load them from the DB.
    """
    def __init__(self, POSTGRES_CONFIG, load_from_db=True):
        self.POSTGRES_CONFIG = POSTGRES_CONFIG
        self.transformer = SentenceTransformersEmbeddings()
        self.df = self.load_book_embeddings(load_from_db)

    def load_book_embeddings(self, load_from_db):
        """
        if load_from_db is set to True then it fetches everything from the database
        otherwise it reads the csv file, computes the embeddings, creates a postgres table and stores them in it.
        """
        if load_from_db:
            df = read_books(self.POSTGRES_CONFIG)
        else:
            
            create_table(self.POSTGRES_CONFIG)
            logging.info("Successfully created books table in postgres DB..")

            df = pd.read_csv('data/goodreads_data.csv').dropna()
            logging.info("Computing embeddings for all books.")
            df['embedding'] = df['description'].progress_apply(lambda x: self.transformer.get_embedding(x))
            # df['embedding'] = df['description'].apply(lambda x: self.transformer.get_embedding(x))
            logging.info("Finished computing embeddings.")

            df['genres'] = df['genres'].apply(lambda x: eval(x))
            df['embedding'] = df['embedding'].apply(lambda x: x.tolist())
            
            store_books(self.POSTGRES_CONFIG, df)
        return df

    def recommend_books(self, text, k=5):
        """
        Given a new user query this function computes the embedding and then uses the distance function as defined in the class
        SentenceTransformersEmbeddings and fetches the k most relevant books
        """
        new_embedding = self.transformer.get_embedding(text)
        self.df['cosine_similarity'] = self.df['embedding'].apply(lambda x: self.transformer.get_distance(x, new_embedding))
        self.df = self.df.sort_values(by='cosine_similarity', ascending=False, ignore_index=True)
        return self.df[['book_name', 'author', 'description',  'url']].head(k)
