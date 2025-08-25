from src.web import create_app

app = create_app(env="test")
app.testing = True
client = app.test_client()

def test_web():
	response = client.get("/")
	assert b"Inicio"in response.data