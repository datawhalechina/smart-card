from typing import Optional, List

from fastapi import APIRouter
import logging

from services.summarize import intelligent_summary, fetch_web
from utils.standard_response import standard_response
from utils.generation_models import SummarizeRequest, SummarizeResponse, WebFetchResponse, WebFetchRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter()


@router.post("/generate", response_model = standard_response[SummarizeResponse])
async def summarize_content(summarize_req: SummarizeRequest):
    response_data = await intelligent_summary(summarize_req)
    res_data = standard_response[SummarizeResponse]
    res_data.data = response_data
    return res_data


@router.post("/fetch-web", response_model = standard_response[WebFetchResponse])
async def fetch_web_content(fetch_req: WebFetchRequest):
    response_data = await fetch_web(fetch_req)
    res_data = standard_response[WebFetchResponse]
    res_data.data = response_data
    return res_data