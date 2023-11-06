from fastapi import FastAPI
from pydantic import BaseModel, validator
from typing import List
from enum import Enum
import requests
import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

app = FastAPI()

class ChatMessageRole(str, Enum):
    System = "system"
    User = "user"
    Assistant = "assistant"

class ChatCompletionMessage(BaseModel):
    role: ChatMessageRole
    content: str
    class Config:
        use_enum_values = True

class Input(BaseModel):
    messages: List[ChatCompletionMessage]
    temperature: float
    frequency_penalty: float

@app.post("/v1/submit")
async def submit(input: Input):
    messages_dicts = [message.dict() for message in input.messages]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = messages_dicts,
        temperature=input.temperature,
        frequency_penalty=input.frequency_penalty
    )
    return completion['choices'][0]['message']['content']