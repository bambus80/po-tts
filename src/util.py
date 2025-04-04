import os


def delete_temp_audio() -> None:
    os.remove("./response.mp3")
