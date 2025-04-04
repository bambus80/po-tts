from pydantic import BaseModel


class Parameters(BaseModel):
    lang: str = "en"
    rate: int = 125
    volume: float = 1.0
    gender: str = "male"

    def update_parameters(self, update: "Parameters"):
        self.lang = update.lang
        self.rate = update.rate
        self.volume = update.volume
        self.gender = update.gender
