import os
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Database Schema ---
# You'll need to create the 'orders' table in your database.
# SQL to run in the database pod:
# CREATE TABLE orders (
#     id SERIAL PRIMARY KEY,
#     cart_items JSONB,
#     total_price NUMERIC(10, 2) NOT NULL,
#     created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
# );
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
    return "<h1>Order Service is running!</h1>"

@app.route('/orders', methods=['POST'])
def create_order():
    """Creates a new order and saves it to the database."""
    # Get the order data from the request body
    new_order_data = request.get_json()
    if not new_order_data or 'cart_items' not in new_order_data or 'total_price' not in new_order_data:
        return jsonify({"error": "Missing required order data"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # The SQL command to insert a new order
        sql = "INSERT INTO orders (cart_items, total_price) VALUES (%s, %s) RETURNING id;"
        
        # Execute the command with the data from the request
        cur.execute(sql, (
            jsonify(new_order_data['cart_items']).get_data(as_text=True), 
            new_order_data['total_price']
        ))
        
        # Get the ID of the new order
        new_order_id = cur.fetchone()[0]
        
        # Commit the transaction to save the changes
        conn.commit()
        
        cur.close()
        conn.close()
        
        return jsonify({"status": "success", "order_id": new_order_id}), 201

    except Exception as e:
        return jsonify({"error": f"Database error: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)