# 智能朋友圈文案生成器 API 文档

## 概述
基于深度学习与多模态AI的智能朋友圈文案生成服务，支持图片上传、自动描述生成、多风格文案生成。

## 基础信息
- 服务地址: `http://your-domain.com`
- 内容类型: `application/json` (API) / `multipart/form-data` (文件上传)
- 认证: 目前无需认证

## API端点

### 1. 首页
- **URL**: `/`
- **方法**: `GET`
- **描述**: 返回Web界面
- **响应**: HTML页面

### 2. 生成文案
- **URL**: `/api/generate`
- **方法**: `POST`
- **描述**: 上传图片并生成文案
- **请求格式**: `multipart/form-data`
- **参数**:
  - `image` (文件): 图片文件 (jpg, png, gif)
  - `styles` (字符串, 可选): JSON数组，指定文案风格，默认 `["幽默搞笑", "文艺清新", "简洁直接"]`

- **成功响应** (200):
```json
{
  "success": true,
  "image_description": "图片的中文描述",
  "original_description": "图片的英文描述",
  "image_url": "/static/uploads/filename.jpg",
  "captions": {
    "幽默搞笑": "幽默风格的文案",
    "文艺清新": "文艺风格的文案",
    "简洁直接": "简洁风格的文案"
  },
  "styles": ["幽默搞笑", "文艺清新", "简洁直接"]
}