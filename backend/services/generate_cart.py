# backend/services/generateCart.py

import os
import uuid
import logging
import asyncio
from fastapi import HTTPException

from integration.llm_prompt import call_ark_llm, extract_html_from_response
from utils.generation_models import GenerationRequest, GenerationResponseData, GenerationMode

logger = logging.getLogger(__name__)

OUTPUT_DIR = "generated_htmls"
USER_PROMPT_WEB_DESIGNER = """"
<!-- 请在这里添加您的用户提示 -->
"""

async def generate_cart(payload: GenerationRequest) -> GenerationResponseData:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file_id = str(uuid.uuid4())
    llm_raw_response = ""
    html_path = ""

    if payload.mode == GenerationMode.PROMPT:
        if not payload.prompt:
            raise HTTPException(status_code=400, detail="PROMPT模式需要提供prompt")

        logger.info(f"处理PROMPT模式 - file_id: {file_id}")

        combined_prompt = USER_PROMPT_WEB_DESIGNER + payload.prompt

        prompt_path = os.path.join(OUTPUT_DIR, f"{file_id}_prompt.txt")
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(payload.prompt)

        try:
            logger.info(f"使用模型 '{payload.model or 'default'}' 调用LLM")

            model_to_use = payload.model or "deepseek-v3-250324"
            temperature_to_use = payload.temperature or 0.7

            llm_raw_response = await asyncio.to_thread(
                call_ark_llm,
                prompt=combined_prompt,
                model_id=model_to_use,
                temperature=temperature_to_use
            )

            html_content = extract_html_from_response(llm_raw_response)

            html_path = os.path.join(OUTPUT_DIR, f"{file_id}.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            logger.info(f"HTML内容已保存到: {html_path}")

        except Exception as e:
            logger.error(f"通过LLM生成内容时发生错误: {e}", exc_info=True)
            error_message = f"LLM调用期间发生内部服务器错误: {str(e)}"
            return GenerationResponseData(
                file_id=file_id,
                success=False,
                html_path="",
                raw_llm_response=None,
                message=error_message
            )

    elif payload.mode == GenerationMode.PASTE:
        if not payload.html_input:
            raise HTTPException(status_code=400, detail="PASTE模式需要提供HTML输入")
        logger.info(f"处理PASTE模式 - file_id: {file_id}")
        html_path = os.path.join(OUTPUT_DIR, f"{file_id}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(payload.html_input)
        logger.info(f"HTML文件已直接保存: {html_path}")
    else:
        raise HTTPException(status_code=400, detail="无效的生成模式")

    html_url = f"/api/download-html/{file_id}"

    response_data = GenerationResponseData(
        file_id=file_id,
        success=True,
        html_path=html_url,
        raw_llm_response=llm_raw_response if payload.mode == GenerationMode.PROMPT else None,
        message="HTML卡片生成成功"
    )

    return response_data

