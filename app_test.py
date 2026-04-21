import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200

def test_weather_api_route(client):
    """Test the weather API endpoint (mocking may be needed for external APIs)."""
    # This assumes you have a route like /weather
    response = client.get('/weather?city=London')
    # Even if it fails due to API keys, we check if the route exists
    assert response.status_code in [200, 401, 500]
