"""
Unit tests for Flask application core functionality.
"""

def test_app_creation(app):
    """Test that the Flask app is created successfully."""
    assert app is not None
    assert app.config['TESTING'] is True

def test_home_page(client):
    """Test that the home page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Financial Assistant' in response.data
    assert b'Track, Analyze, and Optimize Your Finances' in response.data

def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'ok'
    assert 'message' in json_data

def test_404_page(client):
    """Test that 404 errors are handled properly."""
    response = client.get('/nonexistent-page')
    assert response.status_code == 404
    assert b'404' in response.data

def test_app_config(app):
    """Test that the app has required configuration."""
    assert 'SECRET_KEY' in app.config
    assert 'DATABASE' in app.config
    assert app.config['DATABASE'].endswith('.db')

