from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel
from src.controller.tts import TTSController
from src.parameters import Parameters
from src.util import delete_temp_audio


def get_parameters():
    return Parameters()


app = FastAPI()
tts_controller = TTSController()


class TextToSpeechRequest(BaseModel):
    text: str


class ParameterModel(BaseModel):
    lang: str = "en"
    rate: int = 125
    volume: float = 1.0
    gender: str = "male"


@app.get("/")
async def root():
    return {"message": "hi!"}


@app.post("/to_speech")
async def to_speech(request: TextToSpeechRequest, bg_tasks: BackgroundTasks):
    bg_tasks.add_task(delete_temp_audio)
    tts_controller.speak(request.text)
    return FileResponse("response.mp3", media_type="audio/mpeg", filename="response.mp3")


@app.patch("/set_parameter")
async def set_parameter(update: ParameterModel, parameters: Parameters = Depends(get_parameters)):
    try:
        parameters.update_parameters(update)
        tts_controller.apply_parameters(parameters)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid setting")
    return {"message": "Parameters set!"}
