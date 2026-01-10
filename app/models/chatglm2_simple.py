# app/models/chatglm2_simple.py
import torch
from transformers import AutoConfig, AutoTokenizer, AutoModel
import logging
import os

logger = logging.getLogger(__name__)

class ChatGLM2Simple:
    """极简版 ChatGLM2，避免量化问题"""
    
    def __init__(self, model_path=None):
        self.model_path = model_path or r".\model_cache\chatglm2-6b-int4"
        self._init_model()
    
    def _init_model(self):
        """初始化模型，使用最简方式"""
        try:
            logger.info("使用极简模式加载 ChatGLM2...")
            
            # 方法：先加载 config，然后手动处理
            config = AutoConfig.from_pretrained(
                self.model_path,
                trust_remote_code=True,
                local_files_only=True
            )
            
            # 禁用量化相关配置
            if hasattr(config, 'quantization_bit'):
                config.quantization_bit = None
            if hasattr(config, 'quantization_method'):
                config.quantization_method = None
            
            # 加载 tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True,
                local_files_only=True,
                config=config
            )
            
            # 使用 from_config 而不是 from_pretrained，避免自动量化
            self.model = AutoModel.from_config(
                config,
                trust_remote_code=True
            )
            
            # 加载权重（跳过量化层）
            state_dict = torch.load(
                os.path.join(self.model_path, "pytorch_model.bin"),
                map_location='cpu'
            )
            
            # 过滤掉量化相关的权重
            filtered_state_dict = {}
            for key, value in state_dict.items():
                if 'quant' not in key.lower():
                    filtered_state_dict[key] = value
            
            # 加载过滤后的权重
            missing_keys, unexpected_keys = self.model.load_state_dict(
                filtered_state_dict, strict=False
            )
            
            logger.info(f"加载完成，缺失的键: {len(missing_keys)}，意外的键: {len(unexpected_keys)}")
            
            self.model.eval()
            logger.info("极简模式加载成功")
            
        except Exception as e:
            logger.error(f"极简模式加载失败: {e}")
            # 回退到 SimpleTextGenerator
            from .simple_generator import SimpleTextGenerator
            self.model = SimpleTextGenerator()
            self.is_fallback = True
            logger.info("已回退到 SimpleTextGenerator")
    
    def generate_caption(self, description, style="通用"):
        if hasattr(self, 'is_fallback') and self.is_fallback:
            # 使用回退生成器
            return self.model.generate_caption(description, style)
        
        try:
            prompt = f"请写一条关于{description}的{style}风格朋友圈文案"
            
            response, _ = self.model.chat(
                self.tokenizer,
                prompt,
                history=[],
                max_length=60
            )
            
            return response.strip()
        except:
            return f"{description}，值得分享"