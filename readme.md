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
git clone https://github.com/loxs123/quickchat.git
cd quickchat
pip install -r requirements.txt
playwright install

# # linux 配置node
# 之前若安装过要删除干净
curl -fsSL https://fnm.vercel.app/install | bash
source ~/.bashrc
fnm install 16
fnm use 16
# window 配置node16
iwr -useb https://fnm.vercel.app/install | iex # [powershell + 管理员权限]
call fnm env --use-on-cd | cmd
fnm install 16
fnm use 16

export SILICONFLOW_API_KEY=YOURKEY
# API Key 获取地址：https://siliconflow.cn/

nohup python app.py &

```


## 体验网站

http://101.200.43.46/

> 仅供学习使用。
