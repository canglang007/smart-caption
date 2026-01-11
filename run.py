# run.py - 修改启动部分
import sys
import os
from dotenv import load_dotenv 
load_dotenv()

# 第3步：调试信息（在加载后打印，这才是真实值）
print(f"🔍 [环境变量检查] 工作目录: {os.getcwd()}")
print(f"🔍 [环境变量检查] GENERATOR_TYPE = '{os.environ.get('GENERATOR_TYPE', '未设置（将使用默认值: simple）')}'")
api_key = os.environ.get('AI_API_KEY')
print(f"🔍 [环境变量检查] AI_API_KEY 前几位 = '{api_key[:8] + '...' if api_key and len(api_key) > 8 else '未设置'}'")


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
print(f"🔍 [DEBUG] 当前 GENERATOR_TYPE 环境变量值为: '{os.environ.get('GENERATOR_TYPE')}'")
print(f"🔍 [DEBUG] 当前 AI_API_KEY 环境变量值为: '{os.environ.get('AI_API_KEY')}'")
from app import create_app
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    #logging.info(f"启动服务: http://{host}:{port}")
    print(f"🚀 启动服务，端口: {port}")
    app.run(host=host, port=port, debug=False)