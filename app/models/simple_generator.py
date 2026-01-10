# app/models/simple_generator.py
import random
import logging

logger = logging.getLogger(__name__)

class SimpleTextGenerator:
    """基于模板的简单文案生成器"""
    
    def __init__(self):
        self.templates = {
            "幽默搞笑": [
                "看到{description}，笑死我了！",
                "今日份的快乐源泉：{description}",
                "{description}，这不得发个朋友圈炫耀一下？",
                "捕捉到一只野生{description}，快来看！",
                "{description}，这也太可爱/搞笑了吧！"
            ],
            "文艺清新": [
                "风轻轻吹过，带来{description}的温柔",
                "记录这一刻的{description}，岁月静好",
                "{description}，是时光赠予的礼物",
                "遇见{description}，心生欢喜",
                "这{description}，温柔了时光"
            ],
            "简洁直接": [
                "{description}",
                "分享：{description}",
                "记录：{description}",
                "{description}，美好的一天",
                "今日所见：{description}"
            ],
            "诗意抒情": [
                "{description}，如诗如画",
                "眼前的{description}，道不尽心中诗意",
                "{description}，恍若梦中风景",
                "这{description}，诉说着时光的故事",
                "{description}，心中涌起无限感慨"
            ]
        }
    
    def generate_caption(self, image_description, style="幽默搞笑"):
        """基于模板生成文案"""
        try:
            # 获取对应风格的模板列表
            style_templates = self.templates.get(style, self.templates["简洁直接"])
            
            # 随机选择一个模板
            template = random.choice(style_templates)
            
            # 填充描述
            result = template.format(description=image_description)
            
            # 如果是"简洁直接"风格，确保简短
            if style == "简洁直接" and len(result) > 20:
                result = image_description
            
            logger.info(f"Generated {style} caption: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Simple generation error: {str(e)}")
            return f"分享：{image_description}"