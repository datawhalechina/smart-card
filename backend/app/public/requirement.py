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
    res_data = standard_response[GenerationResponseData]
    res_data.data = response_data
    return res_data



@router.post("/download-html", response_model= standard_response[GenerationResponseData])
async def generate_files(payload: GenerationRequest):
    response_data = await generate_cart(payload)
    return response_data


# @app.get("/api/download-html/{file_id}")
# async def download_html(file_id: str):
#     file_path = os.path.join(OUTPUT_DIR, f"{file_id}.html")
#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="HTML file not found")
#     return FileResponse(file_path, media_type='text/html', filename=f"{file_id}.html")
