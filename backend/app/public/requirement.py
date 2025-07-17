from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
import logging
from utils.standard_response import standard_response
from services.generate_cart import generate_cart
from utils.generation_models import GenerationResponseData, GenerationRequest



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter()

@router.post("/generate", response_model= standard_response[GenerationResponseData])
async def generate_files(payload: GenerationRequest):
    response_data = await generate_cart(payload)
    return response_data