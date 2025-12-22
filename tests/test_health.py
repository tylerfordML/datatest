def test_health_endpoint(client):
    """
    Check: Does the health endpoint respond with the correct status of 200 and 'ok'
    Purpose: Validates liveness probe endpoint used in production monitoring
    
    """
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
