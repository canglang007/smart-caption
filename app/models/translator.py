# app/models/translator.py
from transformers import MarianMTModel, MarianTokenizer
import torch
import logging

logger = logging.getLogger(__name__)

class Translator:
    def __init__(self):
        """初始化翻译模型（英译中）"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Loading translator model on {self.device}...")
        
        # 使用 Helsinki-NLP 的英译中模型
        model_name = "Helsinki-NLP/opus-mt-en-zh"
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name).to(self.device)
        
        self.model.eval()
        logger.info("Translator model loaded successfully.")
    
    def translate(self, text):
        """翻译英文到中文"""
        try:
            # 对文本进行分词
            batch = self.tokenizer([text], return_tensors="pt", padding=True).to(self.device)
            
            # 生成翻译
            with torch.no_grad():
                gen = self.model.generate(**batch)
            
            translated = self.tokenizer.batch_decode(gen, skip_special_tokens=True)
            return translated[0]
            
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return text  # 如果翻译失败，返回原文