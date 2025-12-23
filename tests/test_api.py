def test_single_conversion(client):
    """
    
    Check: Does a valid single integer query return the correct Roman numeral
    Purpose: Verifies HTTP endpoint behavior and JSON response format
    
    """
    response = client.get("/v1/romannumeral?query=10")
    
    assert response.status_code == 200
    assert response.json() == {
        "input": "10",
        "output": "X"
    }


def test_invalid_query(client):
    """
    
    Check: When a input is out-of-range does it trigger a HTTP 400 code
    Purpose: Validates input validation and proper error messaging
    
    """
    response = client.get("/v1/romannumeral?query=300")
    
    assert response.status_code == 400
    assert "Input must be between" in response.json()["detail"]


def test_missing_query(client):
    """
    
    Check: When a query parameter is missing does it trigger a HTTP 400 code
    Purpose: Ensures the service handles missing required parameters
    
    """
    response = client.get("/v1/romannumeral")
    
    assert response.status_code == 400

def test_range_conversion(client):
    """
    
    Check: Does a range query return the correct list of conversions in ascending order
    Purpose: Validates async processing and aggregation of multiple conversions
    
    """
    response = client.get("/v1/romannumeral?min=1&max=3")
    
    assert response.status_code == 200
    expected = {
        "conversions": [
            {"input": "1", "output": "I"},
            {"input": "2", "output": "II"},
            {"input": "3", "output": "III"},
        ]
    }
    assert response.json() == expected


def test_range_invalid_min_greater_than_max(client):
    """
    
    Check: When the min >= max does it return a HTTP 400 code
    Purpose: Validates input validation for range queries
    
    """
    response = client.get("/v1/romannumeral?min=5&max=3")
    

    assert response.status_code == 400
