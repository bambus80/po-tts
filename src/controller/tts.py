from src.parameters import Parameters
import pyttsx3


class TTSController:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()

    def speak(self, text: str) -> None:
        print(f"        TTS: Generating response - length:{len(text)}")
        self.engine.save_to_file(text, "response.mp3")
        self.engine.runAndWait()

    def set_language(self, language) -> None:
        match language:
            case "en":
                ...
            case _:
                raise ValueError("Unsupported language")

    def apply_parameters(self, params: Parameters) -> None:
        print(f"        TTS: Params updated - rate:{params.rate} volume:{params.volume} gender:{params.gender}")
        self.engine.setProperty("rate", params.rate)
        self.engine.setProperty("volume", params.volume)

        voices = self.engine.getProperty("voices")
        if hasattr(params, "gender"):
            if params.gender.lower() == "male":
                self.engine.setProperty("voice", voices[0].id)
            elif params.gender.lower() == "female" and len(voices) > 1:
                self.engine.setProperty("voice", voices[1].id)
