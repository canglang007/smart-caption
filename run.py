# run.py - 修改启动部分
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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

# 导入配置
try:
    from config.generator_config import GeneratorConfig
    config = GeneratorConfig.get_config()
    logging.info(f"使用配置: {config}")
except:
    logging.info("使用默认配置")

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    #logging.info(f"启动服务: http://{host}:{port}")
    print(f"🚀 启动服务，端口: {port}")
    app.run(host=host, port=port, debug=False)