from typing import Optional, List

from fastapi import APIRouter, HTTPException
import logging

from config.config import settings
import os
from fastapi.responses import FileResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/{file_id}")
async def download_html(file_id: str):
    file_path = os.path.join(settings.OUTPUT_DIR, f"{file_id}.html")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="HTML file not found")
    return FileResponse(file_path, media_type='text/html', filename=f"{file_id}.html")

