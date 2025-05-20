# LLM 快捷网页

## 目录
- [LLM 快捷网页](#llm-快捷网页)
  - [目录](#目录)
    - [功能特点](#功能特点)
    - [演示截图](#演示截图)
  - [部署说明](#部署说明)
    - [本地部署](#本地部署)
      - [Linux 环境配置 \[不支持知乎，知乎需要打开网页登录\]](#linux-环境配置-不支持知乎知乎需要打开网页登录)
      - [Windows 环境配置](#windows-环境配置)
  - [体验网站](#体验网站)

### 功能特点

* 流式输出
* 左右栏可以拖动调整
* 设置快捷指令按钮，无需每次输入
* 支持查询小红书、知乎、微博、贴吧、B站的内容

### 演示截图

![界面示意1](images/img1.png)
![界面示意2](images/img2.png)

---

## 部署说明

### 本地部署

#### Linux 环境配置 [不支持知乎，知乎需要打开网页登录]

1. 克隆仓库：
    ```bash
    git clone https://github.com/loxs123/quickchat.git
    cd quickchat
    ```

2. 安装依赖：
    ```bash
    pip install -r requirements.txt
    playwright install
    ```

3. 配置 Node.js：
    - 确保之前安装的 Node.js 已完全卸载。
    - 安装 fnm（快速 Node.js 版本管理器）：
        ```bash
        curl -fsSL https://fnm.vercel.app/install | bash
        source ~/.bashrc
        fnm install 16
        fnm use 16
        ```

4. 设置 API Key：
    ```bash
    export SILICONFLOW_API_KEY=YOURKEY
    ```
    - API Key 获取地址：https://siliconflow.cn/

5. 启动应用：
    ```bash
    nohup python app.py &
    ```

#### Windows 环境配置

1. 克隆仓库：
    ```bash
    git clone https://github.com/loxs123/quickchat.git
    cd quickchat
    ```

2. 安装依赖：
    ```bash
    pip install -r requirements.txt
    playwright install
    ```

3. 安装 Node.js 16：
    - 从 Node.js 官网下载并安装 Node.js 16 版本：https://nodejs.org/en/download/

4. 设置 API Key：
    ```bash
    set SILICONFLOW_API_KEY=YOURKEY
    ```
    - API Key 获取地址：https://siliconflow.cn/

5. 启动应用：
    ```bash
    python app.py
    ```

## 体验网站

http://101.200.43.46/loxs

> 仅供学习使用。
