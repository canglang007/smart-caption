# app/models/vision_model.py
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class VisionModel:
    def __init__(self):
        """初始化BLIP模型用于图像描述生成"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Loading vision model on {self.device}...")
        
        # 使用BLIP模型（基础版，相对轻量）
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        ).to(self.device)
        
        # 设置为评估模式
        self.model.eval()
        logger.info("Vision model loaded successfully.")
    
    def generate_caption(self, image_path, max_length=50):
        """生成图像描述"""
        try:
            # 打开并预处理图像
            image = Image.open(image_path).convert('RGB')
            
            # 使用BLIP生成描述（无条件生成）
            inputs = self.processor(image, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                out = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    num_beams=5,
                    temperature=0.7
                )
            
            caption = self.processor.decode(out[0], skip_special_tokens=True)
            logger.info(f"Generated caption: {caption}")
            return caption
            
        except Exception as e:
            logger.error(f"Error in vision model: {str(e)}")
            return "An interesting image"