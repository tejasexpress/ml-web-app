from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class Input(BaseModel):
    model: str
    prompt: str
    temperature: float
    max_tokens: int

@app.post("/v1/submit")
async def submit(input: Input):
    header = {"Content-Type": "application/json"}
    payload = {
        "model": input.model,
        "prompt": input.prompt,
        "temperature": input.temperature,
        "max_tokens": input.max_tokens
    }
    response = requests.post("https://03fa-198-166-142-218.ngrok-free.app/v1/completions", headers=header, json=payload)
    if response.status_code == 200:
        output=response.json()
        return output['choices'][0]['text']
    return "Error: Unable to fetch response from server"

