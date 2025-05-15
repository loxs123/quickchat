from flask import Flask, render_template, request, jsonify, Response
import requests
import json
import os

app = Flask(__name__)

SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")

def chat_model_api(query, mode="默认"):
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
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ 接口调用失败：{str(e)}"


def stream_chat_model_api(query, mode="默认"):
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

    response = requests.post(url, json=payload, headers=headers, stream=True)

    def generate():
        for line in response.iter_lines():
            if not line:
                continue
            if line.startswith(b"data: "):
                res = line.decode("utf-8")[len("data:"):].strip()
                if res == "[DONE]":
                    break
                try:
                    parsed = json.loads(res)
                    content = parsed["choices"][0]["delta"].get("content") or ""
                    reasoning_content = parsed["choices"][0]["delta"].get("reasoning_content") or ""
                    chunk = content + reasoning_content
                    yield f"data: {chunk}-$#$#$#$-"
                except Exception as e:
                    yield f"data: [ERROR] {str(e)}-$#$#$#$-"
                    break
    return generate()

# === 首页路由 ===
@app.route("/")
def index():
    return render_template("index.html")

# === 接收前端文本并调用大模型 ===
@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    input_text = data.get("text", "")
    mode = data.get("mode", "默认")

    output = chat_model_api(input_text, mode)
    return jsonify({"result": output})


@app.route("/stream_process", methods=["POST"])
def stream_process():
    data = request.get_json()
    input_text = data.get("text", "")
    mode = data.get("mode", "默认")
    return Response(stream_chat_model_api(input_text, mode), content_type="text/event-stream")


# === 启动应用 ===
if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=False, host="0.0.0.0", port=80)
