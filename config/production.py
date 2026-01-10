# config/production.py
import os

class ProductionConfig:
    """生产环境配置"""
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-in-production')
    
    # 上传配置
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # 模型配置
    MODEL_TYPE = os.environ.get('MODEL_TYPE', 'simple')
    
    # 性能配置
    THREADS_PER_PAGE = 4
    JSON_SORT_KEYS = False
    
    # 安全配置
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    @classmethod
    def init_app(cls, app):
        """初始化应用"""
        app.config.from_object(cls)
        
        # 确保上传目录存在
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # 设置日志
        import logging
        from logging.handlers import RotatingFileHandler
        
        # 文件日志
        file_handler = RotatingFileHandler(
            'smart_caption.log',
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Smart Caption startup')