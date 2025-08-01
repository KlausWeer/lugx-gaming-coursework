from flask import Flask, request, jsonify
import clickhouse_connect

app = Flask(__name__)

# --- Replace with your ClickHouse Cloud details! ---
CLICKHOUSE_HOST = 'j37jfjnak1.asia-southeast1.gcp.clickhouse.cloud'
CLICKHOUSE_USER = 'default' # Usually 'default'
CLICKHOUSE_PASSWORD = 'il~35XgxRh~J2'
# ----------------------------------------------------

# This endpoint will listen for data sent from the frontend
@app.route('/track', methods=['POST'])
def track_event():
    # Get the JSON data sent by the client (the frontend)
    event_data = request.get_json()

    # Basic validation to ensure we have the data we need
    if not event_data:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400

    try:
        # Establish connection to ClickHouse Cloud
        client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            user=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
            secure=True # Important for Cloud connections
        )
        
        # Prepare the data for insertion
        # The column names must match your table definition
        columns = ['event_type', 'page_url', 'user_id']
        data_to_insert = [
            [
                event_data.get('event_type', 'unknown'), # Default to 'unknown'
                event_data.get('page_url', ''),          # Default to empty string
                event_data.get('user_id', '') 
            ]
        ]

        # Insert the data into your table
        client.insert('lugx_events', data_to_insert, column_names=columns)

        # Return a success message
        return jsonify({'status': 'success'}), 200

    except Exception as e:
        # Print the error to your terminal for debugging
        print(f"Error inserting into ClickHouse: {e}")
        # Return a server error message
        return jsonify({'status': 'error', 'message': 'Could not process event'}), 500

if __name__ == '__main__':
    # Run this service on a different port, e.g., 5003
    app.run(host='0.0.0.0', port=5003)