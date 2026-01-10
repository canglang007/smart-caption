# app/services/caption_service.py
import os
import uuid
from PIL import Image
import logging
from ..models.vision_model import VisionModel
from ..models.translator import Translator
#from ..models.text_generator import TextGenerator
# from ..models.simple_generator import SimpleTextGenerator
logger = logging.getLogger(__name__)

class CaptionService:
    def __init__(self, model_type="simple"):
        """
        初始化服务
        
        Args:
            model_type: 模型类型 ('chatglm2', 'simple')
        """
        logger.info(f"正在初始化文案生成服务，使用模型: {model_type}")
        
        # 初始化视觉模型
        self.vision_model = VisionModel()
        
        # 初始化翻译器
        self.translator = Translator()
        
        # 根据类型选择文本生成器
        self.text_generator = self._init_text_generator(model_type)
        
        logger.info("文案生成服务初始化完成")
    
    def _init_text_generator(self, model_type):
        """初始化文本生成器"""
        if model_type == "chatglm2":
            try:
                from ..models.chatglm2_generator import ChatGLM2Generator
                
                # 尝试本地路径
                local_paths = [
                    r".\model_cache\chatglm2-6b-int4",  # 你的下载路径
                    r".\model_cache\ZhipuAI\chatglm2-6b-int4",
                ]
                
                model_path = None
                for path in local_paths:
                    if os.path.exists(path):
                        model_path = path
                        logger.info(f"使用本地模型: {model_path}")
                        break
                
                if model_path:
                    generator = ChatGLM2Generator(model_path=model_path)
                else:
                    logger.warning("未找到本地模型，尝试在线加载")
                    generator = ChatGLM2Generator(model_path="ZhipuAI/chatglm2-6b-int4")
                
                logger.info("ChatGLM2 生成器初始化成功")
                return generator
                
            except Exception as e:
                logger.error(f"ChatGLM2 初始化失败: {e}")
                logger.info("回退到 SimpleTextGenerator")
                return self._init_text_generator("simple")        
        else:  # simple
            from ..models.simple_generator import SimpleTextGenerator
            generator = SimpleTextGenerator()
            logger.info("SimpleTextGenerator 初始化成功")
            return generator
        # self.text_generator = TextGenerator()
        # self.text_generator = SimpleTextGenerator()  # 简单生成器
        # self.text_generator = APIGenerator(api_key="your-key")  # API

    
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
                caption = self.text_generator.generate_caption(zh_caption, style)
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