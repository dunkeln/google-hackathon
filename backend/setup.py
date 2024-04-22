import sqlite3 as sql
import logging

# Configure logging
logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
        )


def connect_db(file: str):
    """ Connects to the specified SQLite database file. """
    try:
        conn = sql.connect(file)
        return conn
    except sql.Error as e:
        logging.error(f"Database connection failed: {e}")
        return None


create_tables = '''
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT CHECK(LENGTH(name) <= 20) NOT NULL,
    project TEXT NOT NULL,
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    email TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    uname TEXT CHECK(LENGTH(uname) <= 20) NOT NULL,
    project_id INTEGER,
    email TEXT NOT NULL UNIQUE,
    FOREIGN KEY(project_id) REFERENCES projects(id)
);
CREATE TABLE IF NOT EXISTS chats (
    user_id INTEGER,
    chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);
CREATE TABLE IF NOT EXISTS log (
    chat_id INTEGER,
    role TEXT CHECK(role IN ('GEM', 'USER')) NOT NULL,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY(chat_id) REFERENCES chats(chat_id)
);
'''


def spawn(conn):
    """ Spawns tables based on the provided SQL creation script. """
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.executescript(create_tables)
            conn.commit()
            logging.info("Tables created successfully.")
        except sql.Error as e:
            logging.error(f"Failed to execute table creation script: {e}")
        finally:
            cursor.close()


def to(conn: sql.Connection, table: str):
    queries = {
        'projects':
            'INSERT INTO projects (name, project, email) VALUES (?, ?, ?)',
        'users':
            'INSERT INTO users (uname, project_id, email) VALUES (?, ?, ?)',
        'chats': 'INSERT INTO chats (user_id) VALUES (?)',
        'log': 'INSERT INTO log (chat_id, role, message) VALUES (?, ?, ?)'
    }

    def add(values):
        with conn:
            cursor = conn.cursor()
            try:
                cursor.execute(queries[table], values)
                conn.commit()
                logging.info("Data inserted successfully.")
            except sql.Error as e:
                logging.error(f"Failed to insert data: {e}")
            finally:
                cursor.close()

    return add


if __name__ == '__main__':
    conn = connect_db('db/por_gemini.db')
    spawn(conn)
    to_projects = to(conn, 'projects')
    to_projects((
        'Amazon',
        'for the clients',
        'amazon@amazon.com'))