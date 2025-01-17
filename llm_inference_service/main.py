import logging

import uvicorn
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from starlette.status import HTTP_200_OK
from vllm import LLM, SamplingParams
from pydantic import BaseModel

from schemas import LLMResponse, HealthResponse
from llm import LLMForSummary
import yaml

SERVICE_HOST = "0.0.0.0"
SERVICE_PORT = 8080

logging.basicConfig(
    format="%(levelname)s | %(asctime)s | %(message)s", level=logging.INFO
)

class ChatMessage(BaseModel):
    message: str
    
config = yaml.safe_load(open("/opt/app-root/src/llm_inference_service/config.yaml"))

model_choice = config['model_choice']
tensor_parallel_size = config['tensor_parallel_size']
gpu_memory_utilization = config['gpu_memory_utilization']
max_model_len = config['max_model_len']
max_context_length = config['max_context_length']
chunking_strat = config['chunking_strat']
summary_limit = config['summary_limit']

llm = LLMForSummary(model_path = model_choice, 
                    tensor_parallel_size = tensor_parallel_size,
                    gpu_memory_utilization = gpu_memory_utilization,
                    max_model_len = max_model_len,
                    max_context_length = max_context_length,
                    chunking_strat = chunking_strat,
                    summary_limit = summary_limit)

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
        final_str = llm.llm_orchestrator(prompt.message)
        return {"text": final_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))