# app/models/text_generator.py - 替换为使用 ChatGLM-6B-INT4
from transformers import AutoTokenizer, AutoModel
import torch
import logging
import re

logger = logging.getLogger(__name__)

class TextGenerator:
    def __init__(self, model_name="THUDM/chatglm-6b-int4"):
        """初始化ChatGLM-6B-INT4模型（量化版，适合消费级GPU）"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Loading ChatGLM-6B-INT4 on {self.device}...")
        
        # 使用量化版的ChatGLM-6B，只需约6GB显存或CPU运行
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(
            model_name, 
            trust_remote_code=True,
            dtype=torch.float16 if self.device == "cuda" else torch.float32
        )
        
        if self.device == "cuda":
            self.model = self.model.cuda()
        else:
            self.model = self.model.float()
        
        self.model.eval()
        logger.info("ChatGLM-6B loaded successfully.")
    
    def generate_caption(self, image_description, style="幽默搞笑"):
        """根据图片描述生成朋友圈文案"""
        try:
            # 构建更明确的提示词
            styles_prompts = {
                "幽默搞笑": f"请根据以下图片描述，用幽默搞笑的方式写一条朋友圈文案：{image_description}\n要求：轻松有趣，让人会心一笑，贴近图片内容。",
                "文艺清新": f"请根据以下图片描述，用文艺清新的风格写一条朋友圈文案：{image_description}\n要求：语言优美，有意境，有诗意，贴近图片内容。",
                "简洁直接": f"请根据以下图片描述，写一条简洁直接的朋友圈文案：{image_description}\n要求：简短明了，不超过20字，直接表达。",
                "诗意抒情": f"请根据以下图片描述，用诗意抒情的风格写一条朋友圈文案：{image_description}\n要求：富有诗意，情感真挚，有文学性，贴近图片内容。",
                "通用": f"请根据以下图片描述，写一条合适的朋友圈文案：{image_description}\n要求：自然流畅，适合朋友圈分享。"
            }
            
            prompt = styles_prompts.get(style, styles_prompts["通用"])
            
            # 添加更明确的指令
            full_prompt = f"{prompt}\n请直接输出文案，不要添加任何解释。文案："
            
            # 使用ChatGLM生成
            response, _ = self.model.chat(
                self.tokenizer,
                full_prompt,
                history=[],
                max_length=200,
                temperature=0.8,  # 降低随机性
                top_p=0.8,
                repetition_penalty=1.1
            )
            
            # 清理结果
            result = response.strip()
            
            # 移除可能的多余内容
            for remove_str in ["文案：", "好的，", "以下是", "根据您的描述", "根据描述"]:
                if result.startswith(remove_str):
                    result = result[len(remove_str):].strip()
            
            # 如果太长，截取合适的长度
            if len(result) > 80:
                # 找到第一个句号、感叹号或问号
                for end_char in ['。', '！', '!', '？', '?', '~', '...']:
                    idx = result.find(end_char)
                    if idx > 5:  # 至少有几个字
                        result = result[:idx+1]
                        break
                else:
                    # 没有找到结束符号，截取前50字
                    result = result[:50] + "..."
            
            logger.info(f"Generated {style} caption: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Text generation error: {str(e)}")
            # 备用方案：使用简单的模板
            templates = {
                "幽默搞笑": f"看到{image_description}，忍不住发个朋友圈！",
                "文艺清新": f"此刻的{image_description}，记录这一刻的美好。",
                "简洁直接": f"{image_description}",
                "诗意抒情": f"眼前这{image_description}，心中涌起无限诗意。",
                "通用": f"分享一张照片：{image_description}"
            }
            return templates.get(style, f"记录：{image_description}")