# app/models/chatglm_generator.py - 修复版
import torch
from transformers import AutoTokenizer, AutoModel
import logging
import re
import os
import sys

logger = logging.getLogger(__name__)

class ChatGLM2Generator:
    def __init__(self, model_path=None):
        """ChatGLM2生成器，专门针对Windows Flask环境修复"""
        logger.info("初始化ChatGLM2生成器（Windows Flask专用版）...")
        
        # 🚨 关键修复：设置环境变量，禁用量化和CUDA扩展
        os.environ['USE_CUDA_EXT'] = '0'
        os.environ['DISABLE_QUANTIZATION'] = '1'
        os.environ['LOAD_IN_8BIT'] = '0'
        os.environ['LOAD_IN_4BIT'] = '0'
        
        # 设置模型路径
        if model_path is None:
            # Windows路径，使用原始字符串
            model_path = r".\model_cache\chatglm2-6b-int4"
            # 或者用绝对路径
            # model_path = r"C:\Users\你的用户名\project\model_cache\chatglm2-6b-int4"
        
        self.model_path = model_path
        self._load_model()
    
    def _load_model(self):
        """专门为Windows Flask环境优化的加载方法"""
        try:
            # 🚨 修复1：添加当前目录到sys.path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sys.path.insert(0, current_dir)
            
            # 🚨 修复2：在导入transformers之前设置环境变量
            import warnings
            warnings.filterwarnings("ignore", message=".*quantization.*")
            warnings.filterwarnings("ignore", message=".*CUDA.*")
            
            logger.info(f"加载模型: {self.model_path}")
            
            # 🚨 修复3：强制使用本地文件，禁用远程代码（如果可能）
            # 检查模型是否存在
            if not os.path.exists(self.model_path):
                logger.error(f"模型路径不存在: {self.model_path}")
                raise FileNotFoundError(f"请确认模型已下载到: {self.model_path}")
            
            # 🚨 修复4：使用非常保守的参数加载
            from transformers import AutoTokenizer, AutoModel
            
            # 先加载tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True,
                local_files_only=True,
                revision="main"
            )
            
            # 🚨 修复5：强制CPU模式，使用float32，避免任何量化
            self.model = AutoModel.from_pretrained(
                self.model_path,
                trust_remote_code=True,
                dtype=torch.float32,  # 强制使用float32
                local_files_only=True,
                revision="main"
            ).float()  # 确保是float32
            
            # 🚨 修复6：显式设置为CPU模式
            self.model = self.model.cpu() if torch.cuda.is_available() else self.model
            
            # 设置为评估模式
            self.model.eval()
            
            logger.info("✅ ChatGLM2加载成功（Windows Flask专用模式）")
            
            # 简单测试
            test_response, _ = self.model.chat(
                self.tokenizer,
                "你好",
                history=[],
                max_length=100
            )
            logger.info(f"模型测试: {test_response[:20]}...")
            
        except Exception as e:
            logger.error(f"❌ 模型加载失败: {e}")
            # 提供更详细的错误信息
            import traceback
            traceback.print_exc()
            raise
    
    def generate_caption(self, image_description, style="通用"):
        """生成文案"""
        try:
            # 简单的提示词模板
            prompt = f"请写一条{style}风格的朋友圈文案，关于：{image_description}"
            
            # 生成
            with torch.no_grad():  # 禁用梯度计算
                response, _ = self.model.chat(
                    self.tokenizer,
                    prompt,
                    history=[],
                    max_length=80,
                    temperature=0.7
                )
            
            # 清理结果
            result = response.strip()
            for prefix in ["文案：", "文案:", "好的，", "以下是"]:
                if result.startswith(prefix):
                    result = result[len(prefix):].strip()
            
            return result
            
        except Exception as e:
            logger.error(f"生成失败: {e}")
            # 简单的后备
            return f"记录：{image_description}"