# config/generator_config.py
import os

class GeneratorConfig:
    """生成器配置"""
    
    # 模型类型：chatglm2, chatglm, simple
    MODEL_TYPE = os.environ.get('MODEL_TYPE', 'chatglm2')
    
    # ChatGLM2 配置
    CHATGLM2_PATH = os.environ.get('CHATGLM2_PATH', r'.\model_cache\chatglm2-6b-int4')
    
    # 设备配置
    DEVICE = os.environ.get('DEVICE', 'auto')  # auto, cuda, cpu
    
    # 生成参数
    MAX_LENGTH = int(os.environ.get('MAX_LENGTH', '100'))
    TEMPERATURE = float(os.environ.get('TEMPERATURE', '0.7'))
    
    @classmethod
    def get_config(cls):
        return {
            'model_type': cls.MODEL_TYPE,
            'chatglm2_path': cls.CHATGLM2_PATH,
            'device': cls.DEVICE,
            'max_length': cls.MAX_LENGTH,
            'temperature': cls.TEMPERATURE
        }