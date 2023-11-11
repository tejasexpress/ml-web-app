from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List
from enum import Enum
import requests
import os
import openai
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse

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

def get_response(input: Input):
    try:
        messages_dicts = [message.dict() for message in input.messages]
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = messages_dicts,
            temperature=input.temperature,
            frequency_penalty=input.frequency_penalty,
            stream=True,
        )
    except Exception as e:
        raise HTTPException(503, 'OpenAI call failed')
    try:
        for chunk in completion:
            current_content = chunk["choices"][0]["delta"].get("content", "")
            yield current_content
    except Exception as e:
        raise HTTPException(503, 'OpenAI call failed')

@app.post("/v1/submit")
async def submit(input: Input):
    return StreamingResponse(get_response(input), media_type="text/event-stream")