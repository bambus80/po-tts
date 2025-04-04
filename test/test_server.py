from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from src.parameters import Parameters


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200 and response.json() == {"message": "hi!"}


def test_to_speech(mock_tts_controller):
    with patch("main.tts_controller", mock_tts_controller):
        response = client.post("/to_speech", json={"text": "Hello"})
        assert response.status_code == 200 and response.headers["content-type"] == "audio/mpeg"


def test_set_parameter():
    with patch("main.get_parameters", return_value=Parameters()) as mock_get_params:
        response = client.patch("/set_parameter", json={"lang": "en", "rate": 120, "volume": 0.9, "gender": "female"})
        assert response.status_code == 200 and response.json() == {"message": "Parameters set!"}
