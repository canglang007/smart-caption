# app/models/api_generator.py
import openai
import logging

logger = logging.getLogger(__name__)

class APIGenerator:
    """调用OpenAI/DeepSeek等API生成文案"""
    
    def __init__(self, api_key=None, base_url="https://api.deepseek.com"):
        self.client = openai.OpenAI(
            api_key=api_key or "your-api-key",  # 替换为你的API key
            base_url=base_url
        )
    
    def generate_caption(self, image_description, style="幽默搞笑"):
        """调用API生成文案"""
        try:
            style_instructions = {
                "幽默搞笑": "用幽默搞笑的方式，轻松有趣，让人会心一笑",
                "文艺清新": "用文艺清新的风格，语言优美，有意境",
                "简洁直接": "简洁直接，简短明了，不超过20字",
                "诗意抒情": "用诗意抒情的风格，富有诗意，情感真挚"
            }
            
            instruction = style_instructions.get(style, "自然流畅")
            
            prompt = f"""你是一个朋友圈文案生成助手。请根据以下图片描述，{instruction}地写一条朋友圈文案。

图片描述：{image_description}

要求：
1. 文案要贴近图片描述的内容
2. 符合朋友圈分享的语气
3. 直接输出文案，不要添加任何解释

文案："""
            
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个专业的朋友圈文案写手。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            result = response.choices[0].message.content.strip()
            
            # 清理结果
            result = result.replace('"', '').replace("文案：", "").strip()
            
            logger.info(f"Generated {style} caption: {result}")
            return result
            
        except Exception as e:
            logger.error(f"API generation error: {str(e)}")
            return f"看到{image_description}，分享这一刻的美好。"