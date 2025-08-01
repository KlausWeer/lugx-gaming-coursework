# game-service/test_game_service.py
import os
import requests

# The test function must also start with 'test_'
def test_get_games_endpoint():
    # We get the URL of the service to test from an environment variable.
    # This makes the test flexible. We can run it locally or in the pipeline.
    service_url = os.environ.get("SERVICE_URL", "http://localhost:5001")

    # Make a GET request to the /api/games endpoint
    response = requests.get(f"{service_url}/api/games")

    # --- Assertions ---
    # This is where we check if the test passed or failed.

    # 1. Check if the HTTP status code is 200 (OK)
    assert response.status_code == 200

    # 2. Check if the response content is valid JSON
    try:
        response_data = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    # 3. Check if the response is a list (as we expect a list of games)
    assert isinstance(response_data, list)

    print(f"\nSuccessfully tested {service_url}/api/games. Found {len(response_data)} games.")