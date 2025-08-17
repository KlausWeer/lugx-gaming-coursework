# game-service/test_game_service.py
import os
import requests

def test_get_games_endpoint():
    
    service_url = os.environ.get("SERVICE_URL", "http://localhost:5001")

    # GET request to the /api/games endpoint
    response = requests.get(f"{service_url}/api/games")

    

    # 1. check if the HTTP status code is 200
    assert response.status_code == 200

    # 2. check if the response content is valid JSON
    try:
        response_data = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    # 3 check if the response is a list 
    assert isinstance(response_data, list)

    print(f"\nSuccessfully tested {service_url}/api/games. Found {len(response_data)} games.")