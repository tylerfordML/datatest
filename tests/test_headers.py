def test_request_id_generated(client):
    """
    Check: Does a request ID get automatically generated if client does not provide one
    Purpose: Verifies traceability middleware works for all requests
    
    """
    response = client.get("/v1/romannumeral?query=5")
    
    assert "X-Request-ID" in response.headers


def test_request_id_propagation(client):
    """
    Check: When a client provideds a request ID can it be found in the response headers
    Purpose: Supports upstream traceability and distributed request correlation
    
    """
    headers = {"X-Request-ID": "test-id-123"}
    response = client.get("/v1/romannumeral?query=5", headers=headers)
    
    assert response.headers["X-Request-ID"] == "test-id-123"

