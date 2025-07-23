import os
import asyncio
import logging
import httpx
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import HTTPException # Re-import HTTPException if needed for raising errors

from config.config import settings

load_dotenv()
# Configure logging (can inherit from main app or configure separately)
logger = logging.getLogger(__name__)
# Ensure logger is configured if this module is run independently or before main app config
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)

# Load environment variables directly (assuming dotenv is called in the main script)
# LLM Configuration (Original - can be fallback or replaced)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions") # Provide default URL

# LLM Configuration (New - Ark Platform via OpenAI client)
ARK_API_KEY = settings.ARK_API_KEY
ARK_BASE_URL = settings.ARK_BASE_URL

# Default model IDs (can be overridden by caller)
DEFAULT_ORIGINAL_MODEL = "ep-m-20250330105359-r7wqp" # Or "deepseek-chat" if preferred

# --- Internal LLM Call Functions ---

async def _call_original_llm(prompt: str, model: str, temperature: float) -> str:
    """Internal function to call the LLM using the original httpx method."""
    if not DEEPSEEK_API_KEY:
        logger.error("DEEPSEEK_API_KEY environment variable not set for original LLM call.")
        # Raise HTTPException directly if this function needs to interact with FastAPI error handling
        # Or return an error indicator / raise a custom exception
        raise HTTPException(status_code=500, detail="LLM API key not configured (original method)")

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(DEEPSEEK_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            if data.get('choices') and len(data['choices']) > 0:
                return data['choices'][0]['message']['content']
            else:
                logger.error(f"LLM API response missing expected data: {data}")
                raise HTTPException(status_code=500, detail="Invalid LLM API response (original method)")
        except httpx.RequestError as e:
            logger.error(f"Error calling original LLM API: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to connect to LLM API (original method): {e}")
        except httpx.HTTPStatusError as e:
            logger.error(f"Original LLM API request failed: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"LLM API error (original method): {e.response.text}")

async def _call_ark_llm(prompt: str, model: str, temperature: float, sys_prompt: str = None) -> str:
    """Internal function to call the Ark LLM platform using the OpenAI client."""
    if not ARK_API_KEY:
        logger.error("ARK_API_KEY environment variable not set.")
        raise HTTPException(status_code=500, detail="LLM API key not configured (Ark method)")

    try:
        client = OpenAI(
            api_key=ARK_API_KEY,
            base_url=ARK_BASE_URL,
            timeout=1800.0, # 1800 seconds = 30 minutes
        )

        logger.info(f"Sending request to Ark LLM. Model: {model}, Temperature: {temperature}")

        messages = []
        if sys_prompt:
            messages.append({"role": "system", "content": sys_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=model, # User specifies the Ark model ID here
            messages=messages,
            temperature=temperature
        )

        if hasattr(response.choices[0].message, 'reasoning_content'):
            logger.info(f"LLM Reasoning Content: {response.choices[0].message.reasoning_content}")

        return response.choices[0].message.content

    except Exception as e: # Catch potential OpenAI client errors
        logger.error(f"Error calling Ark LLM API: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to call LLM API (Ark method): {e}")


# --- Public Function ---

async def generate_content_with_llm(prompt: str, model: str | None = None, temperature: float = 0.7, sys_prompt: str = None) -> str:
    """
    Generates content using the appropriate LLM based on available API keys.

    Args:
        prompt: The input prompt for the LLM.
        model: The specific model ID to use. If None, uses defaults based on API key.
        temperature: The generation temperature.
        sys_prompt: Optional system prompt to use for the LLM request.

    Returns:
        The generated content string.

    Raises:
        HTTPException: If API keys are missing or API calls fail.
    """
    if ARK_API_KEY:
        logger.info("ARK_API_KEY found, using Ark LLM method.")
        effective_model = model or settings.ARK_BASE_MODEL
        logger.info(f"Calling Ark LLM with model: {effective_model}")
        return await _call_ark_llm(prompt, effective_model, temperature, sys_prompt)
    elif DEEPSEEK_API_KEY:
        logger.warning("ARK_API_KEY not found, falling back to original LLM method.")
        effective_model = model or DEFAULT_ORIGINAL_MODEL
        logger.info(f"Calling original LLM with model: {effective_model}")
        # Original method doesn't support system prompt yet
        return await _call_original_llm(prompt, effective_model, temperature)
    else:
        logger.error("Neither ARK_API_KEY nor DEEPSEEK_API_KEY are set.")
        raise HTTPException(status_code=500, detail="No LLM API Key configured.")