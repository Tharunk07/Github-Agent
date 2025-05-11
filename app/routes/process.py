from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from app.tasks import perform_github_agent_process
from pydantic import BaseModel
app = FastAPI()

class ChatRequest(BaseModel):
    user_message: str

@app.get("/")
async def homepage():
    return JSONResponse("API is Running")

@app.post("/chat")
async def chat_response(request : ChatRequest):
    return StreamingResponse(await perform_github_agent_process(request.user_message), media_type="application/json")