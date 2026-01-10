# diagnose_chatglm2.py
import os
import sys
import torch

print("=" * 60)
print("ChatGLM2 环境诊断工具")
print("=" * 60)

# 1. 检查Python路径
print("\n1. Python路径:")
for path in sys.path:
    print(f"  - {path}")

# 2. 检查环境变量
print("\n2. 环境变量:")
env_vars = [
    'TRANSFORMERS_CACHE',
    'HF_HOME', 
    'USE_CUDA_EXT',
    'DISABLE_QUANTIZATION',
    'LOAD_IN_8BIT',
    'LOAD_IN_4BIT'
]
for var in env_vars:
    value = os.environ.get(var, '未设置')
    print(f"  {var}: {value}")

# 3. 检查PyTorch和CUDA
print("\n3. PyTorch信息:")
print(f"  PyTorch版本: {torch.__version__}")
print(f"  CUDA可用: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"  GPU设备: {torch.cuda.get_device_name(0)}")

# 4. 检查模型文件
print("\n4. 模型文件检查:")
model_path = r".\model_cache\chatglm2-6b-int4"
if os.path.exists(model_path):
    print(f"  ✅ 模型目录存在: {model_path}")
    files = os.listdir(model_path)
    print(f"  文件数量: {len(files)}")
    
    # 检查关键文件
    key_files = ['config.json', 'pytorch_model.bin', 'tokenizer.model']
    for f in key_files:
        if f in files:
            print(f"  ✅ {f} 存在")
        else:
            print(f"  ❌ {f} 缺失")
else:
    print(f"  ❌ 模型目录不存在: {model_path}")

# 5. 尝试加载模型（像test一样）
print("\n5. 尝试加载模型（test模式）:")
try:
    # 模拟test环境
    original_cwd = os.getcwd()
    print(f"  当前工作目录: {original_cwd}")
    
    # 切换到项目根目录（像test那样）
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    print(f"  切换到: {project_root}")
    
    # 设置环境变量
    os.environ['USE_CUDA_EXT'] = '0'
    os.environ['DISABLE_QUANTIZATION'] = '1'
    
    # 导入并加载
    from transformers import AutoTokenizer, AutoModel
    
    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        trust_remote_code=True,
        local_files_only=True
    )
    
    model = AutoModel.from_pretrained(
        model_path,
        trust_remote_code=True,
        dtype=torch.float32,
        local_files_only=True
    ).float()
    
    model.eval()
    
    print("  ✅ 模型加载成功（test模式）")
    
    # 测试生成
    response, _ = model.chat(tokenizer, "测试", history=[], max_length=1000)
    print(f"  生成测试: {response[:30]}...")
    
    # 切换回原始目录
    os.chdir(original_cwd)
    
except Exception as e:
    print(f"  ❌ 加载失败: {e}")
    import traceback
    traceback.print_exc()

# 6. 尝试Flask环境加载
print("\n6. 模拟Flask环境加载:")
try:
    # 模拟Flask应用工厂
    from app import create_app
    print("  ✅ Flask应用可以创建")
    
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        print("  ✅ Flask应用上下文可以进入")
        
        # 尝试导入服务
        from app.services.caption_service import CaptionService
        print("  ✅ 可以导入CaptionService")
        
except Exception as e:
    print(f"  ❌ Flask环境问题: {e}")

print("\n" + "=" * 60)
print("诊断完成")
print("=" * 60)