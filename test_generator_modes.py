# test_generator_modes.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 1. 测试Simple模式
print("=== 测试 Simple（模板）模式 ===")
os.environ["GENERATOR_TYPE"] = "simple"  # 设为模板模式

from app.services.caption_service import CaptionService
service_simple = CaptionService()
print(f"当前模式: {service_simple.generator_manager.get_current_mode()}")
result = service_simple.process_image("test.jpg", ["幽默搞笑"])  # 需准备一张测试图片
print(f"生成结果: {result}\n")

# 2. 测试API模式 (确保已配置正确的API_KEY)
print("=== 测试 API（智能）模式 ===")
os.environ["GENERATOR_TYPE"] = "api"
os.environ["AI_API_KEY"] = "sk-794b5ae40ad74bc791d2df3524eb203a"  # 替换为你的测试key

# 重新初始化服务以加载新配置
service_api = CaptionService()
print(f"当前模式: {service_api.generator_manager.get_current_mode()}")
# 出于测试成本考虑，可以注释掉实际API调用，或使用一个简单的描述
test_description = "一只可爱的猫咪在沙发上睡觉"
# 模拟调用生成器（不触发完整图片处理流程）
try:
    from app.models.generator_manager import GeneratorManager
    gm = GeneratorManager()
    caption = gm.generate_caption(test_description, "幽默搞笑")
    print(f"API生成结果: {caption}")
except Exception as e:
    print(f"API模式测试可能失败（如密钥无效）: {e}")