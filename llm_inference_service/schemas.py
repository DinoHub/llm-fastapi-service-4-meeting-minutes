"""Schemas for the API service"""

from pydantic import BaseModel


# pylint: disable=too-few-public-methods
class LLMResponse(BaseModel):
    """ASR service response format

    Attributes:
        status_code (int): default success status code
        text (str): output text from the LLM model
    """

    status_code: int = 200
    text: str
    
# pylint: disable=too-few-public-methods
class HealthResponse(BaseModel):
    """
    Response model for the `health` API.

    Attributes:
        status (str): The status message.
    """

    status: str = "HEALTHY"
