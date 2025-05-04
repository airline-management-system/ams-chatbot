def test_ping(client):
    response = client.get('/api/v1/ping')
    assert response.status_code == 200
    assert response.get_data(as_text=True) == 'pong'

#def test_generate(client):
 #   response = client.get('/api/v1/generate')
  #  assert response.status_code == 200

def test_query_model(client):
    response = client.get('/api/v1/query_model')
    assert response.status_code == 200