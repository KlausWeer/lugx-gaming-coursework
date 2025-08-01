import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# --- Database Schema ---
# Before running, you'll need to create the 'games' table in your database.
# You can connect to the database pod and run this SQL command:
# CREATE TABLE games (
#     id SERIAL PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     category VARCHAR(100),
#     price NUMERIC(10, 2)
# );
# INSERT INTO games (name, category, price) VALUES ('Cloud Raider', 'Action RPG', 59.99);
# INSERT INTO games (name, category, price) VALUES ('Cyber Runner', 'Sci-Fi', 49.99);
# -----------------------


def get_db_connection():
    """Establishes a connection to the database using environment variables."""
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD")
    )
    return conn

@app.route('/')
def index():
    """A simple endpoint to confirm the service is running."""
    return "<h1>Game Service is running!</h1>"


@app.route('/api/games', methods=['GET'])
def get_games():
    """Fetches all games from the database and returns them as JSON."""
    try:
        conn = get_db_connection()
        # A cursor allows us to execute SQL commands
        cur = conn.cursor()
        cur.execute('SELECT id, name, category, price FROM games;')
        
        # Fetch all rows from the query
        rows = cur.fetchall()

        # Get column names from the cursor description
        colnames = [desc[0] for desc in cur.description]

        # Close the cursor and connection
        cur.close()
        conn.close()
        
        # Format the data into a list of dictionaries for proper JSON serialization
        games_list = []
        for row in rows:
            games_list.append(dict(zip(colnames, row)))
            
        return jsonify(games_list)

    except Exception as e:
        # If anything goes wrong, return an error message
        return jsonify({"error": f"Database error: {e}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

#trigerring the game service workflow.
# Checking Github Actions