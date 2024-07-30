from typing import Union, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Define models for request payloads
class SetWebhookRequest(BaseModel):
    url: str

class GetDestinationsRequest(BaseModel):
    destinations: List[str]

class SelectDestinationRequest(BaseModel):
    destination_id: int

class SendTextRequest(BaseModel):
    text: str

class SendFileRequest(BaseModel):
    file: Union[str, bytes]

class CloseChatRequest(BaseModel):
    reason: str
    user_id: int

@app.post("/setWebhook")
def set_webhook(request: SetWebhookRequest):
    if not request.url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL")
    return {"url": request.url}

@app.get("/getDestinations")
def get_destinations(destinations: List[str]):
    return {"destinations": destinations}

@app.post("/selectDestination")
def select_destination(request: SelectDestinationRequest):
    if request.destination_id < 0:
        raise HTTPException(status_code=400, detail="Invalid destination ID")
    return {"destination_id": request.destination_id}

@app.post("/sendText")
def send_text(request: SendTextRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    return {"text": request.text}

@app.post("/sendFile")
def send_file(request: SendFileRequest):
    if isinstance(request.file, str):
        if not request.file.startswith("http"):
            raise HTTPException(status_code=400, detail="Invalid file URL")
    elif not request.file:
        raise HTTPException(status_code=400, detail="File cannot be empty")
    return {"file": request.file}

@app.post("/closeChat")
def close_chat(request: CloseChatRequest):
    return {"data": request.dict()}
