import pytest
from unittest.mock import patch, MagicMock
from src.controller.tts import TTSController
from src.parameters import Parameters


@pytest.fixture
def mock_tts_controller():
    with patch("src.controller.tts.pyttsx3.init") as mock_init:
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine
        return TTSController()


def test_speak(mock_tts_controller):
    mock_tts_controller.speak("Hello")
    mock_tts_controller.engine.save_to_file.assert_called_once_with("Hello", "response.mp3")
    mock_tts_controller.engine.runAndWait.assert_called_once()


def test_set_language(mock_tts_controller):
    mock_tts_controller.set_language("en")
    with pytest.raises(ValueError, match="Unsupported language"):
        mock_tts_controller.set_language("fr")


def test_apply_parameters(mock_tts_controller):
    mock_params = Parameters(rate=150, volume=0.8, gender="female")
    mock_tts_controller.apply_parameters(mock_params)
    mock_tts_controller.engine.setProperty.assert_any_call("rate", 150)
    mock_tts_controller.engine.setProperty.assert_any_call("volume", 0.8)
