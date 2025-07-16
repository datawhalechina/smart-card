import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
from prompt_config import SYSTEM_PROMPT_WEB_DESIGNER, USER_PROMPT_WEB_DESIGNER, SYSTEM_PROMPT_SUMMARIZE_2MD
import re

# Load environment variables from a .env file if present
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def call_ark_llm(prompt: str, sys_prompt: str = SYSTEM_PROMPT_WEB_DESIGNER, model_id: str = "deepseek-v3-250324",
                 temperature: float = 0.7) -> str:
    """
    Calls the Ark platform LLM using the OpenAI client library.

    Args:
        prompt (str): The user prompt to send to the LLM.
        model_id (str): The model ID to use (e.g., "deepseek-r1-250120").
                        Defaults to "deepseek-r1-250120".
        temperature (float): Controls randomness. Lower is more deterministic.
                             Defaults to 0.7.

    Returns:
        str: The content of the LLM's response message.

    Raises:
        ValueError: If the ARK_API_KEY environment variable is not set.
        Exception: If the API call fails.
    """
    api_key = os.environ.get("ARK_API_KEY")
    # Use the provided base_url or default to the one in the example
    base_url = os.environ.get("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")

    if not api_key:
        logger.error("ARK_API_KEY environment variable not found.")
        raise ValueError("ARK_API_KEY environment variable must be set.")

    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            # Set a long timeout as recommended for potentially long-running models
            timeout=1800.0,  # 1800 seconds = 30 minutes
        )

        logger.info(f"Sending request to Ark LLM. Model: {model_id}, Temperature: {temperature}")
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                # You can add a system prompt here if needed:
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            # Add other parameters like max_tokens if necessary
            # max_tokens=1024,
        )

        message = response.choices[0].message

        # Check for and log reasoning content if the model provides it
        if hasattr(message, 'reasoning_content') and message.reasoning_content:
            logger.info("LLM Reasoning Content Detected:")
            # You might want to print this or handle it differently
            print("--- Reasoning Content ---")
            print(message.reasoning_content)
            print("--- End Reasoning Content ---")

        content = message.content
        logger.info("Successfully received response from Ark LLM.")
        return content

    except Exception as e:
        logger.error(f"Error during Ark LLM API call: {e}", exc_info=True)
        # Re-raise the exception to be handled by the caller
        raise Exception(f"Failed to get response from Ark LLM: {e}")


def extract_html_from_response(response_text):
    """
    从LLM响应中提取HTML内容

    参数:
        response_text: LLM返回的完整文本

    返回:
        提取出的HTML内容，如果没有找到则返回原始文本
    """
    # 尝试匹配完整的HTML文档（从<!DOCTYPE>或<html>开始到</html>结束）
    html_pattern = r'(?:<!DOCTYPE\s+html[^>]*>|<html[^>]*>)[\s\S]*?</html>'
    match = re.search(html_pattern, response_text, re.IGNORECASE)

    if match:
        return match.group(0)

    # 如果没有找到完整HTML，尝试匹配被代码块包围的HTML
    code_block_pattern = r'```(?:html)?\s*((?:<!DOCTYPE\s+html[^>]*>|<html[^>]*>)[\s\S]*?</html>)\s*```'
    match = re.search(code_block_pattern, response_text, re.IGNORECASE)

    if match:
        return match.group(1)

    # 如果仍然没有找到，尝试匹配任何HTML片段
    html_fragment_pattern = r'<[^>]+>[\s\S]*?</[^>]+>'
    match = re.search(html_fragment_pattern, response_text)

    if match:
        return match.group(0)

    # 如果所有模式都没有匹配，返回原始文本
    return response_text


# --- Example Usage ---
if __name__ == "__main__":
    # Make sure you have a .env file in the same directory
    # with your ARK_API_KEY, like:
    # ARK_API_KEY="your_actual_ark_api_key_here"
    # ARK_BASE_URL="https://ark.cn-beijing.volces.com/api/v3" # Optional, if different

    # Define your prompt
    my_prompt = USER_PROMPT_WEB_DESIGNER + "解释一下什么是大型语言模型 (LLM)，并举例说明其应用。"
    specific_model = "deepseek-v3-250324"  # Or another model you have access to

    try:
        # Call the function with your prompt
        llm_response = call_ark_llm(prompt=my_prompt, model_id=specific_model)

        # 提取HTML内容
        html_content = extract_html_from_response(llm_response)

        # 将HTML内容保存到文件
        html_file_path = "llm_generated.html"
        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"HTML内容已保存到: {html_file_path}")

        # Print the result
        print("\n--- LLM Response ---")
        print(llm_response)

        print("--- End LLM Response ---")

    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except Exception as ex:
        print(f"An error occurred: {ex}")