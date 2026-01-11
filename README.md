# 智能朋友圈文案生成器

## 项目简介
基于深度学习与多模态AI的智能朋友圈文案生成服务，支持图片上传、自动描述生成、多风格文案生成。

## 功能特性
- 🖼️ **图片上传**: 支持JPG、PNG、GIF格式
- 🤖 **智能识别**: 使用BLIP模型自动识别图片内容
- 🌐 **多语言支持**: 自动翻译为中文描述
- 🎨 **多风格文案**: 支持幽默搞笑、文艺清新、简洁直接、诗意抒情等多种风格
- 🚀 **云服务化**: 支持Docker一键部署
- 📱 **响应式设计**: 适配桌面和移动设备

## 技术架构
```bash
┌─────────────────────────────────────────────┐
│ 前端界面 │
│ (HTML5 + CSS3 + JavaScript) │
└───────────────────┬─────────────────────────┘
│ HTTP/JSON
┌───────────────────▼─────────────────────────┐
│ Flask Web服务 │
└─────┬──────────────────────┬────────────────┘
│ │
┌─────▼──────┐ ┌────────▼──────────┐
│ 视觉模型 │ │ 文案生成器 │
│ (BLIP) │ │ (SimpleTextGen) │
└────────────┘ └───────────────────┘
│ │
┌─────▼──────┐ ┌────────▼──────────┐
│ 翻译模型 │ │ 模板引擎 │
│ (MarianMT) │ └───────────────────┘
└────────────┘
```
## 快速开始

### 本地运行
```bash
# 1. 克隆项目
git clone https://github.com/yourusername/smart-caption.git
cd smart-caption

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行服务
python run.py

# 5. 访问 http://localhost:5000

```
```text
项目结构
smart-caption/
├── app/                    # 应用代码
│   ├── models/            # AI模型
│   ├── services/          # 业务服务
│   └── routes/            # 路由
├── static/                # 静态文件
├── config/                # 配置文件
├── requirements.txt       # Python依赖
└── run.py                # 应用入口
```


## 部署到云平台
采用的是railway平台部署的方法，可以采用命令行部署的方法。
```Procfile
# 创建Procfile文件
web: gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 300 --preload run:app
```
### **railway命令行部署**
```bash

# 1. 安装 Railway CLI
# 2. 登录
railway login

# 3. 初始化项目
railway init
 

# 4. 连接到现有项目或新建项目
railway link 

# 5. 部署
railway up

# 6.设置环境变量
railway variables set GENERATOR_TYPE simple
# 也可以在网页中variable进行以下设置
GENERATOR_TYPE=api
AI_API_KEY=xxxx # 输入自己的api
AI_API_BASE=https://api.deepseek.com  # 以DeepSeek为例
AI_MODEL=deepseek-chat

# 7. 打开应用
railway open
# 打开后在settings获取网页链接
```