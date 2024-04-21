import sqlite3 as sql
from sqlite3 import Error
import logging

def connect_db(file: str):
    conn = None
    try:
        conn = sql.connect(file)
    except Error as e:
        logging.error(e)
    finally:
        if conn:
            conn.close()


create_tables = '''
        CREATE TABLE IF NOT EXISTS projects (
            id integer PRIMARY KEY AUTOINCREMENT,
            name text CHECK(LENGTH(cname) <= 20) NOT NULL,
            project text NOT NULL,
            created_time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            email text NOT NULL UNIQUE,
            );
        CREATE TABLE IF NOT EXISTS users (
            user_id integer PRIMARY KEY AUTOINCREMENT,
            uname text CHECK(LENGTH(uname) <= 20) NOT NULL,
            project_id integer FOREIGN KEY,
            email text NOT NULL UNIQUE,
            FOREIGN KEY(project_id) REFERENCES projects(id),
            );
        CREATE TABLE IF NOT EXISTS chats (
            user_id integer,
            chat_id integer PRIMARY KEY AUTOINCREMENT,
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            );
        CREATE TABLE IF NOT EXISTS log (
            chatid integer FOREIGN KEY,
            role TEXT CHECK(role IN ('GEM', 'USER')) NOT NULL,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            FOREIGN KEY(chat_id) REFERENCES chats(chat_id),
            );
    '''

# spawn table
def spawn(conn: sql.Connection):
    """
        Spawns table based on query
        
        Args:
            conn (sql.Connection): path to the sql database to connect to
        
    """
    try:
        q = conn.cursor()
        q.execute(create_tables)
    except Error as e:
        logging.error(e)
