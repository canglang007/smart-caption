# app/services/caption_service.py
import os
import uuid
from PIL import Image
import logging
from ..models.vision_model import VisionModel
from ..models.translator import Translator
from ..models.generator_manager import GeneratorManager  # 替换原来的导入
logger = logging.getLogger(__name__)

class CaptionService:
    def __init__(self, model_type="simple"):
        """
        初始化服务
        
        Args:
            model_type: 模型类型 ('api', 'simple')
        """
        logger.info("初始化文案生成服务（双模式）...")
        self.vision_model = VisionModel()
        self.translator = Translator()

        self.generator_manager = GeneratorManager()
        logger.info(f"服务初始化完成。当前模式：{self.generator_manager.get_current_mode()}")


    
    def process_image(self, image_path, styles=None):
        """
        处理图像并生成文案
        
        Args:
            image_path: 图片路径
            styles: 文案风格列表，如 ['幽默搞笑', '文艺清新']
        
        Returns:
            dict: 包含描述和各风格文案的字典
        """
        if styles is None:
            styles = ['幽默搞笑', '文艺清新', '简洁直接']
        
        try:
            logger.info(f"Processing image: {image_path}")
            
            # 步骤1: 使用视觉模型生成英文描述
            logger.info("Step 1: Generating image caption...")
            en_caption = self.vision_model.generate_caption(image_path)
            
            # 步骤2: 翻译成中文
            logger.info("Step 2: Translating to Chinese...")
            zh_caption = self.translator.translate(en_caption)
            
            # 步骤3: 为每种风格生成文案
            logger.info("Step 3: Generating style captions...")
            captions = {}
            for style in styles:
                caption = self.generator_manager.generate_caption(zh_caption, style)
                captions[style] = caption
            
            result = {
                'success': True,
                'image_description': zh_caption,
                'original_description': en_caption,
                'captions': captions,
                'styles': styles
            }
            
            logger.info("Image processing completed successfully.")
            return result
            
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def save_uploaded_file(self, file):
        """保存上传的文件"""
        # 生成唯一文件名
        ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
        filename = f"{uuid.uuid4().hex}.{ext}"
        
        # 确保扩展名合法
        if ext not in ['jpg', 'jpeg', 'png', 'gif']:
            ext = 'jpg'
            filename = f"{uuid.uuid4().hex}.{ext}"
        
        save_path = os.path.join('static', 'uploads', filename)
        
        # 保存文件
        file.save(save_path)
        
        # 如果是gif，转换为jpg（简化处理）
        if ext == 'gif':
            img = Image.open(save_path)
            img = img.convert('RGB')
            filename = filename.replace('.gif', '.jpg')
            save_path = save_path.replace('.gif', '.jpg')
            img.save(save_path, 'JPEG')
        
        return filename, save_path