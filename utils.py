import httpx
import os
import json

SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")

async def chat_model_api(query, mode="默认"):
    prompt_prefix = {
        "translate": "请将以下内容翻译成中文：",
        "polish": "请润色以下文字，使其更通顺自然：",
        "solve": "请解答下面的问题，并给出详细的解题步骤：",
        "默认": ""
    }
    prompt = prompt_prefix.get(mode, "") + query

    payload = {
        "model": "Qwen/Qwen2.5-72B-Instruct",
        "messages": [{
            "role": "user",
            "content": prompt,
        }]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {SILICONFLOW_API_KEY}"
    }
    url = "https://api.siliconflow.cn/v1/chat/completions"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ 接口调用失败：{str(e)}"


async def stream_chat_model_api(query, mode="默认"):
    prompt_prefix = {
        "translate": "请将以下内容翻译成中文：",
        "polish": "请润色以下文字，使其更通顺自然：",
        "solve": "请解答下面的问题，并给出详细的解题步骤：",
        "默认": ""
    }
    prompt = prompt_prefix.get(mode, "") + query
    url = "https://api.siliconflow.cn/v1/chat/completions"

    payload = {
        "model": "Qwen/Qwen2.5-72B-Instruct",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": True,
        "max_tokens": 4096,
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {SILICONFLOW_API_KEY}"
    }

    async with httpx.AsyncClient() as client:
        async with client.stream("POST", url, json=payload, headers=headers) as response:
            async for line in response.aiter_lines():
                if not line:
                    continue
                if line.startswith("data: "):
                    res = line[len("data: "):].strip()
                    if res == "[DONE]":
                        break
                    try:
                        parsed = json.loads(res)
                        content = parsed["choices"][0]["delta"].get("content") or ""
                        reasoning_content = parsed["choices"][0]["delta"].get("reasoning_content") or ""
                        chunk = content + reasoning_content
                        yield f"data: {chunk}-$#$-"
                    except Exception as e:
                        yield f"data: [ERROR] {str(e)}-$#$-"
                        break