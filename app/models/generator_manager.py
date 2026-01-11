# app/models/generator_manager.py
import logging
import os

logger = logging.getLogger(__name__)

class GeneratorManager:
    """
    生成器管理器：根据配置动态选择使用哪种生成策略。
    """

    def __init__(self):
        # 读取配置，决定当前使用哪个生成器
        # 可以通过环境变量 GENERATOR_TYPE 控制：'simple' 或 'api'
        self.generator_type = os.getenv("GENERATOR_TYPE", "simple").lower()
        self._generator = None
        self._initialize_generator()

    def _initialize_generator(self):
        """根据类型初始化对应的生成器"""
        if self.generator_type == "api":
            try:
                from .api_generator import APIGenerator
                self._generator = APIGenerator()
                logger.info(f"✅ 生成器管理器已初始化：[API模式]")
            except Exception as e:
                logger.error(f"初始化API生成器失败，将回退到Simple模式: {e}")
                self._fallback_to_simple()
        else:  # 默认为'simple'或其他无效值
            self._fallback_to_simple()

    def _fallback_to_simple(self):
        """回退到Simple生成器"""
        try:
            from .simple_generator import SimpleTextGenerator
            self._generator = SimpleTextGenerator()
            self.generator_type = "simple"  # 确保状态同步
            logger.info(f"✅ 生成器管理器已初始化：[Simple模板模式]")
        except Exception as e:
            logger.error(f"初始化Simple生成器也失败: {e}")
            raise

    def generate_caption(self, image_description: str, style: str = "通用") -> str:
        """对外统一接口，调用当前生成器"""
        if self._generator is None:
            return f"系统错误：生成器未初始化。描述：{image_description}"
        return self._generator.generate_caption(image_description, style)

    def get_current_mode(self) -> str:
        """获取当前生成器的类型，可用于前端显示"""
        return self.generator_type