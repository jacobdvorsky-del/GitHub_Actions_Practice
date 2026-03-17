

def test_get_health_returns_status_code_200(health_api):
    response = health_api.get_health()
    assert response.status_code == 200

def test_get_health_returns_status_healthy(health_api):
    response = health_api.get_health()
    assert response.json()["status"] == "healthy"
