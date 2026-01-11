# app/models/api_generator.py
import requests
import json
import logging
import os

logger = logging.getLogger(__name__)

class APIGenerator:
    """调用兼容OpenAI API格式的大模型服务（如DeepSeek）"""

    def __init__(self):
        # 从环境变量安全读取配置
        self.api_key = os.getenv("AI_API_KEY")
        self.base_url = os.getenv("AI_API_BASE", "https://api.deepseek.com")
        self.model = os.getenv("AI_MODEL", "deepseek-chat")
        
        if not self.api_key:
            logger.warning("未找到AI_API_KEY环境变量，API生成器将不可用。")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_caption(self, image_description: str, style: str = "通用") -> str:
        """
        调用大模型API生成朋友圈文案
        """
        if not self.api_key:
            return self._fallback_caption(image_description, style)
        
        # 精心设计的提示词（Prompt），是获得好文案的关键
        system_prompt = "你是一个专业的朋友圈文案写手，擅长创作自然、贴合场景的分享文案。请直接输出文案，不要任何解释。"
        user_prompt = f"请根据以下图片描述，写一条{style}风格的朋友圈文案：\n图片描述：{image_description}\n要求：语言符合{style}风格，直接输出文案。"

        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 150
        }

        try:
            logger.info(f"[API模式] 请求生成文案，风格：{style}")
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            caption = result["choices"][0]["message"]["content"].strip()
            logger.info(f"[API模式] 生成成功，长度：{len(caption)}")
            return caption
            
        except Exception as e:
            logger.error(f"[API模式] 请求失败，将使用备用文案: {e}")
            return self._fallback_caption(image_description, style)

    def _fallback_caption(self, description: str, style: str) -> str:
        """API调用失败时的备用方案（复用Simple模板逻辑）"""
        import random
        fallback_templates = {
            "幽默搞笑": [f"看到{description}，笑不活了！", f"今日份快乐：{description}"],
            "文艺清新": [f"静静地欣赏{description}。", f"{description}，时光都慢了。"],
            "简洁直接": [description, f"分享：{description}"],
            "诗意抒情": [f"{description}，如诗如画。", f"眼前的{description}，心中诗意。"],
        }
        templates = fallback_templates.get(style, [description])
        return random.choice(templates)