# backend/services/generateCart.py

import os
import uuid
import logging
import asyncio
from fastapi import HTTPException
import requests

from config.prompt_config import SYSTEM_PROMPT_SUMMARIZE_2MD
from integration.llm_prompt import call_ark_llm, extract_html_from_response
from utils.generation_models import GenerationRequest, GenerationResponseData, GenerationMode, SummarizeRequest, \
    SummarizeResponse, WebFetchResponse, WebFetchRequest
from utils.llm_caller import generate_content_with_llm
from config.config import settings

logger = logging.getLogger(__name__)

USER_PROMPT_WEB_DESIGNER = """"
<!-- 请在这里添加您的用户提示 -->
"""

# 智能总结服务
async def intelligent_summary(summarize_req: SummarizeRequest) -> SummarizeResponse:
    response_data = ""
    try:
        content = summarize_req.content

        if not content:
            response_data = SummarizeResponse(
                summary="",
                success=False,
                message="请提供需要总结的内容"
            )

        summarize_prompt = f"""请对以下内容进行简洁明了的总结，突出关键信息，保持语言简练：
                            {content}
                            总结：
                            """

        model_to_use = summarize_req.model if summarize_req.model else settings.ARK_BASE_MODEL


        summary = await generate_content_with_llm(
            prompt=summarize_prompt,
            sys_prompt=SYSTEM_PROMPT_SUMMARIZE_2MD,
            model=model_to_use,
            temperature=0.5
        )

        response_data = SummarizeResponse(
            summary=summary.strip(),
            success=True
        )
    except Exception as e:
        logger.error(f"内容总结失败: {str(e)}")
        response_data = SummarizeResponse(
            summary="",
            success=False,
            message=f"总结生成失败: {str(e)}"
        )

    return response_data


# 生成HTML服务
async def fetch_web(fetch_req: WebFetchRequest) -> WebFetchResponse:
    try:
        url = fetch_req.url.strip()

        if not url:
            return WebFetchResponse(
                content="",
                success=False,
                message="请提供有效的URL"
            )

        jina_url = f"{settings.JINA_API_URL}{url}"

        if not settings.JINA_API_KEY:
            logger.error("JINA_API_KEY environment variable not found")
            return WebFetchResponse(
                content="",
                success=False,
                message="Jina API密钥未配置，请检查环境变量"
            )

        headers = {'Authorization': f'Bearer {settings.JINA_API_KEY}'}

        logger.info(f"Fetching web content from: {url}")

        response = requests.get(jina_url, headers=headers)
        response.raise_for_status()

        content = response.text

        return WebFetchResponse(
            content=content,
            success=True
        )
    except Exception as e:
        logger.error(f"获取网页内容失败: {str(e)}")
        return WebFetchResponse(
            content="",
            success=False,
            message=f"获取网页内容失败: {str(e)}"
        )