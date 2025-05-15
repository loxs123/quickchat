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

```bash
pip install requests flask gunicorn

export SILICONFLOW_API_KEY=YOURKEY
# API Key 获取地址：https://siliconflow.cn/

gunicorn -w 2 -b 127.0.0.1:80 app:app
```

> 仅供学习和研究使用。
