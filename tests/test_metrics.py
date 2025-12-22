def test_metrics_endpoint(client):
    """
    Check: Prometheus metrics endpoint responds with 200 and contains expected counters
    Purpose: Validates that instrumentation is correctly exposed for observability
    
    """
    response = client.get("/metrics")
    
    assert response.status_code == 200
    assert "http_requests_total" in response.text
