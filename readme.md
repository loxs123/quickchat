# LLM 快捷网页

一个双栏设计的 LLM 回复网页。

### 功能特点

* 流式输出
* 左右可以拖动
* 设置快捷指令按钮，无需每次输入

### 演示截图

![界面示意1](images/img1.png)
![界面示意2](images/img2.png)

---

## 部署说明

### 本地
```bash
pip install requests flask

git clone https://github.com/loxs123/quickchat.git
cd quickchat
export SILICONFLOW_API_KEY=YOURKEY
# API Key 获取地址：https://siliconflow.cn/

nohup python app.py &

```

### 结合 gunicorn 和 nginx

```bash
pip install gunicorn
nohup gunicorn -w 2 -b 127.0.0.1:8000 app:app &
sudo apt install nginx
sudo tee /etc/nginx/sites-available/myapp <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
# nginx: configuration file /etc/nginx/nginx.conf test is successful
sudo systemctl reload nginx

```

> 仅供学习使用。
