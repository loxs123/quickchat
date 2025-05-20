from quart import Quart, render_template, request, jsonify, Response, make_response, send_file
from werkzeug.utils import secure_filename
import os
import time
import random
import json
import httpx  # 替代 requests，用于异步调用
import re

# import crawler
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "\\crawler")
from crawler.crawler_factory import CrawlerFactory


app = Quart(__name__)

SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")

# 配置上传路径
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


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

@app.route("/stream_process", methods=["POST"])
async def stream_process():
    data = await request.get_json()
    input_text = data.get("text", "")
    mode = data.get("mode", "默认")
    if mode != 'search':
        return Response(stream_chat_model_api(input_text, mode), content_type="text/event-stream")
    else:
        cfgs = re.findall(r'\[(.*?)\]', input_text)
        cfgs = {cfg.split('=')[0] : cfg.split('=')[1] for cfg in cfgs}
        keywords = re.sub(r'\[.*?\]', '', input_text)
        cfgs['KEYWORDS'] = keywords
        platforms = ['xhs', 'wb', 'bili', 'zhihu', 'dy', 'tieba']

        async def generate():
            crawler = CrawlerFactory.create_crawler(platform=cfgs.get('P', random.choice(platforms)), **cfgs)
            async for note in crawler.start():
                yield f"data: {note}\n\n-$#$-"

        return Response(generate(), content_type="text/event-stream")

@app.route("/")
async def index():
    resp = await make_response(await render_template('index.html'))
    if not request.cookies.get('session_id'):
        resp.set_cookie('session_id', f'{time.time()}-{random.randint(1, 100)}')
    return resp


@app.route("/process", methods=["POST"])
async def process():
    data = await request.get_json()
    input_text = data.get("text", "")
    mode = data.get("mode", "默认")

    output = await chat_model_api(input_text, mode)
    return jsonify({"result": output})


@app.route("/upload", methods=["POST"])
async def upload():
    if "files" not in (await request.files):
        return jsonify({"error": "No file part"}), 400
    session_id = request.cookies.get('session_id')
    files = (await request.files).getlist("files")
    saved_files = []
    for file in files:
        if file.filename == "":
            continue
        filename = f'{session_id}.' + secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        await file.save(save_path)
        saved_files.append(file.filename)

    return jsonify({"uploaded": saved_files})


if __name__ == "__main__":
    import asyncio
    app.run(host='127.0.0.1', port=5001, debug=True)
