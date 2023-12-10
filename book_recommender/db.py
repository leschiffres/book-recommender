from sqlalchemy import create_engine
import psycopg2
import psycopg2.extras
import pandas as pd
import numpy as np

def create_table(POSTGRES_CONFIG):
    pg_connection = psycopg2.connect(**POSTGRES_CONFIG)

    with pg_connection.cursor() as pg_cur:
        query = """
         CREATE TABLE IF NOT EXISTS books (
         book_name VARCHAR(255) NOT NULL,
         author VARCHAR(255) NOT NULL,
         description TEXT,
         genres TEXT[] NOT NULL,
         url VARCHAR(255),
         embedding FLOAT[]
         );
        """

        pg_cur.execute(query)
    pg_connection.commit()
    pg_connection.close()

def insert_books_sql_alchemy(POSTGRES_CONFIG, data:pd.DataFrame):
    data['embedding'] = data['embedding'].apply(lambda x: x.tolist())
    engine = create_engine("postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
        user= POSTGRES_CONFIG['user'],
        password= POSTGRES_CONFIG['password'],
        host= POSTGRES_CONFIG['host'],
        port= POSTGRES_CONFIG['port'],
        database= POSTGRES_CONFIG['database'],
    ))
    data.to_sql('books', engine, index=False, if_exists='replace')

def store_books(POSTGRES_CONFIG, data:pd.DataFrame):
    update_query = """
    INSERT INTO books(book_name, author, description, genres, url, embedding)
    VALUES %s
    """
    pg_connection = psycopg2.connect(**POSTGRES_CONFIG)
    with pg_connection.cursor() as pg_cur:

        psycopg2.extras.execute_values (
            pg_cur, 
            update_query, 
            list(map(tuple, data[['book_name', 'author', 'description', 'genres', 'url', 'embedding']].values)), 
            template=None, 
            page_size=100
        )
        
    pg_connection.commit()
    pg_connection.close()

def read_books(POSTGRES_CONFIG):
    query = """
    SELECT * FROM books
    """
    pg_connection = psycopg2.connect(**POSTGRES_CONFIG)
    with pg_connection.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as pg_cur:
        pg_cur.execute(query)
        df = pd.DataFrame(pg_cur.fetchall())
        # df['embedding'] = df['embedding'].apply(lambda x: np.array(list(eval(x))).astype(np.float32))
    return df


if __name__ == '__main__':
    create_table()