import logging

import uvicorn
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from starlette.status import HTTP_200_OK
from vllm import LLM, SamplingParams
from pydantic import BaseModel

from schemas import LLMResponse, HealthResponse
from llm import LLMForSummary

SERVICE_HOST = "0.0.0.0"
SERVICE_PORT = 8080

logging.basicConfig(
    format="%(levelname)s | %(asctime)s | %(message)s", level=logging.INFO
)

class ChatMessage(BaseModel):
    message: str


llm = LLMForSummary(model_path = "models/llama/Llama-3.2-3B-Instruct", 
                    tensor_parallel_size = 1,
                    gpu_memory_utilization = 0.6,
                    max_model_len = 16000,
                    max_context_length = 7000)

app = FastAPI()

@app.get("/")
async def read_root():
    """Root Call"""
    return {"message": "This is an LLM service."}

@app.get("/health")
async def read_health() -> HealthResponse:
    """
    Check if the API endpoint is available.

    This endpoint is used by Docker to check the health of the container.
    """
    return {"status": "HEALTHY"}

@app.post("/llm_generate_meeting_minutes")
async def generate(prompt: ChatMessage):
    try:
        final_str = llm.generate_meeting_minutes(prompt.message)
        return {"text": final_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/llm_orchestrator")
async def generate(prompt: ChatMessage):
    try:
        final_str = llm.orchestrator(prompt.message)
        return {"text": final_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))