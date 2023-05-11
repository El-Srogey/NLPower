# To Store Our Queries For Later Use

import sqlite3
import pandas as pd



class DBStorage:
    def __init__(self):
        # create a connection once class instantiated for a DB called links
        self.sql_connect = sqlite3.connect('links.db')
        self.create_table()
        
    
    def create_table(self):
        '''
            1. Make a DB connection
            2. Init the cursor
            3. The results table query (Create)
            4. Commit The Changes
        '''
        
        # create sql cursor to treats our sql operations
        cursor = self.sql_connect.cursor()
        
        table_query = '''
            CREATE TABLE IF NOT EXISTS results(
                id INTEGER PRIMARY KEY,  -- result_id
                query TEXT,
                rank INTEGER,  -- result page rank
                link TEXT,  
                snippet TEXT,  -- page desc
                html TEXT,   -- scraped page html
                title TEXT,  -- page title
                created DATATIME,  -- query time
                relevance INTEGER, -- ML purposes
                UNIQUE(query, link)  -- prevent getting the same link for the same query
            );
        '''
        cursor.execute(table_query)
        self.sql_connect.commit() 
        cursor.close()
        

    def insert_rows(self, values):
        cursor = self.sql_connect.cursor()
        # will try to insert the values into the DB
        try:
            # ??? to make sure values are formatted correctly
            cursor.execute('INSERT INTO results (query, rank, link, title, snippet, html, created) VALUES(?, ?, ?, ?, ?, ?, ?)', values)
            self.sql_connect.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
        cursor.close()  
    
        
    def query_results(self, query):
        df = pd.read_sql(f"SELECT * FROM results r WHERE r.query = '{query}' ORDER BY rank;", self.sql_connect)
        return df
        