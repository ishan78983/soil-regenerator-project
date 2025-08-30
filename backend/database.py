import sqlite3
from sqlite3 import Error

DATABASE_FILE = "backend/recommendations.db"

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    """Create the recommendations table if it doesn't exist."""
    sql_create_table = """
    CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        location TEXT,
        ph_level REAL NOT NULL,
        organic_matter REAL NOT NULL,
        moisture_content REAL NOT NULL,
        previous_crop TEXT,
        recommendation_text TEXT NOT NULL
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_create_table)
    except Error as e:
        print(e)

def save_recommendation(conn, data):
    """Save a new recommendation to the database."""
    sql = ''' INSERT INTO recommendations(location, ph_level, organic_matter, moisture_content, previous_crop, recommendation_text)
              VALUES(?,?,?,?,?,?) '''
    cursor = conn.cursor()
    recommendation_data = (
        data['location'],
        data['ph_level'],
        data['organic_matter'],
        data['moisture_content'],
        data['previous_crop'],
        data['recommendation_text']
    )
    cursor.execute(sql, recommendation_data)
    conn.commit()
    return cursor.lastrowid

def get_all_recommendations(conn):
    """Query all rows in the recommendations table."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recommendations ORDER BY timestamp DESC")
    
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    
    # Convert list of tuples to list of dictionaries for easier use
    recommendations = [dict(zip(columns, row)) for row in rows]
    return recommendations

def init_database():
    """Initialize the database and table."""
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")