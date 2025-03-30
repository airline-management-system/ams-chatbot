def test_ping(client):
    response = client.get('/api/v1/ping')
    assert response.status_code == 200
    assert response.get_data(as_text=True) == 'pong'