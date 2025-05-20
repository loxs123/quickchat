import os
import time
import random
import json
import httpx  # 替代 requests，用于异步调用
import re
import copy

import asyncio
from playwright.async_api import async_playwright
from quart import Quart, render_template, request, jsonify, Response, make_response, send_file

# import crawler
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/crawler")
from crawler.crawler_factory import CrawlerFactory
import crawler.config as cfg

from utils import chat_model_api, stream_chat_model_api

app = Quart(__name__)

# 配置上传路径
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

crawler_cache = {}
playwright = None
en2zh = {'xhs': '小红书', 'bili': '哔哩哔哩', 'dy': '抖音', 'tieba': '贴吧', 'wb': '微博', 'zhihu': '知乎'}

@app.before_serving
async def startup():
    global crawler_cache, playwright
    print("🌟 App starting...")
    playwright = await async_playwright().start()
    # 初始化 crawler_cache
    crawler_cache['小红书'] = CrawlerFactory.create_crawler('xhs', playwright)
    await crawler_cache['小红书'].start()
    crawler_cache['哔哩哔哩'] = CrawlerFactory.create_crawler('bili', playwright)
    await crawler_cache['哔哩哔哩'].start()
    # crawler_cache['抖音'] = CrawlerFactory.create_crawler('dy', playwright)
    # await crawler_cache['抖音'].start()
    crawler_cache['贴吧'] = CrawlerFactory.create_crawler('tieba', playwright)
    await crawler_cache['贴吧'].start()
    crawler_cache['微博'] = CrawlerFactory.create_crawler('wb', playwright)
    await crawler_cache['微博'].start()
    crawler_cache['知乎'] = CrawlerFactory.create_crawler('zhihu', playwright)
    await crawler_cache['知乎'].start()

    # await asyncio.gather(
    #     crawler_cache['小红书'].start(),
    #     crawler_cache['哔哩哔哩'].start(),
    #     crawler_cache['抖音'].start(),
    #     crawler_cache['贴吧'].start(),
    #     crawler_cache['微博'].start(),
    #     crawler_cache['知乎'].start()
    # )
    
@app.after_serving
async def shutdown():
    playwright.stop()
    print("App is shutting down...")
    # 退出时遍历并关闭所有 crawler
    for crawler in crawler_cache.values():
        if hasattr(crawler, 'close') and callable(crawler.close):
            try:
                await crawler.close()
            except Exception as e:
                print(f"Error logging out crawler: {e}")
    print('[DONE]')

@app.route("/loxs")
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
        platforms_sort = ['贴吧', '微博', '哔哩哔哩', '小红书', '知乎', '抖音']
        if 'P' in cfgs:
            platforms = cfgs['P'].split(',')
            platforms = [en2zh[p.strip()] for p in platforms if p.strip() in en2zh]
        else:
            platforms = list(crawler_cache.keys())
        platforms.sort(key = lambda x: platforms_sort.index(x))

        async def generate():
            # 这里可以根据需要选择不同的平台
            abnormals = []
            for p in platforms:
                cnt = 0
                crawler = crawler_cache[p]
                async for note in crawler.search(**cfgs):
                    yield f"data: ## {p}\n{note}\n\n-$#$-"
                    cnt += 1
                if cnt == 0:
                    abnormals.append(p)

            summary = '请求的平台为：' + ', '.join(platforms)

            if len(abnormals) > 0:
                summary += ', 但以下平台没有获取数据：' + ', '.join(abnormals)
            else:
                summary += ', 均请求成功'

            yield f"data: {summary}\n\n-$#$-"
        return Response(generate(), content_type="text/event-stream")


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

# if __name__ == "__main__":
#     import hypercorn.asyncio
#     from hypercorn.config import Config
#     config = Config()
#     config.bind = ["0.0.0.0:80"]
#     config.startup_timeout = 500  # 延长 lifespan startup 阶段的等待时间
#     asyncio.run(hypercorn.asyncio.serve(app, config))
