# app/routes/upload_routes.py
from flask import request, jsonify, send_from_directory, current_app
import os
from ..services.caption_service import CaptionService
from app.routes import main_bp

caption_service = CaptionService()

@main_bp.route('/')
def index():
    """首页"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>智能朋友圈文案生成</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .upload-box { border: 2px dashed #ccc; padding: 40px; text-align: center; margin: 20px 0; }
            #preview { max-width: 300px; margin: 20px auto; }
            .result { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .loading { display: none; color: #666; }
        </style>
    </head>
    <body>
        <h1>🤖 智能朋友圈文案生成</h1>
        <p>上传图片，AI为你生成多种风格的朋友圈文案</p>
        
        <div class="upload-box">
            <input type="file" id="imageInput" accept="image/*">
            <p>或将图片拖拽到此处</p>
        </div>
        
        <div id="previewContainer" style="display:none;">
            <h3>图片预览</h3>
            <img id="preview" src="" alt="预览">
        </div>
        
        <div>
            <h3>选择文案风格：</h3>
            <label><input type="checkbox" name="style" value="幽默搞笑" checked> 幽默搞笑</label>
            <label><input type="checkbox" name="style" value="文艺清新" checked> 文艺清新</label>
            <label><input type="checkbox" name="style" value="简洁直接" checked> 简洁直接</label>
            <label><input type="checkbox" name="style" value="诗意抒情"> 诗意抒情</label>
        </div>
        
        <button onclick="generateCaption()" style="padding: 10px 20px; font-size: 16px;">生成文案</button>
        
        <div id="loading" class="loading">⏳ AI正在思考中...</div>
        
        <div id="results" style="display:none;">
            <h2>生成结果</h2>
            <p><strong>图片描述：</strong> <span id="description"></span></p>
            <h3>推荐文案：</h3>
            <div id="captions"></div>
        </div>
        
        <script>
            document.getElementById('imageInput').addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        document.getElementById('preview').src = e.target.result;
                        document.getElementById('previewContainer').style.display = 'block';
                    }
                    reader.readAsDataURL(file);
                }
            });
            
            async function generateCaption() {
                const fileInput = document.getElementById('imageInput');
                if (!fileInput.files[0]) {
                    alert('请先选择一张图片');
                    return;
                }
                
                // 获取选中的风格
                const styles = Array.from(document.querySelectorAll('input[name="style"]:checked'))
                    .map(cb => cb.value);
                
                const formData = new FormData();
                formData.append('image', fileInput.files[0]);
                formData.append('styles', JSON.stringify(styles));
                
                document.getElementById('loading').style.display = 'block';
                document.getElementById('results').style.display = 'none';
                
                try {
                    const response = await fetch('/api/generate', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        document.getElementById('description').textContent = result.image_description;
                        
                        const captionsDiv = document.getElementById('captions');
                        captionsDiv.innerHTML = '';
                        
                        for (const [style, caption] of Object.entries(result.captions)) {
                            const div = document.createElement('div');
                            div.className = 'result';
                            div.innerHTML = `<strong>${style}：</strong> ${caption}`;
                            captionsDiv.appendChild(div);
                        }
                        
                        document.getElementById('results').style.display = 'block';
                    } else {
                        alert('生成失败：' + result.error);
                    }
                } catch (error) {
                    alert('请求失败：' + error.message);
                } finally {
                    document.getElementById('loading').style.display = 'none';
                }
            }
        </script>
    </body>
    </html>
    '''

@main_bp.route('/api/generate', methods=['POST'])
def generate_caption():
    """API接口：生成文案"""
    try:
        # 检查文件
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': '没有上传文件'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': '未选择文件'}), 400
        
        # 获取风格参数
        styles = request.form.get('styles', '["幽默搞笑", "文艺清新", "简洁直接"]')
        import json
        try:
            styles = json.loads(styles)
        except:
            styles = ['幽默搞笑', '文艺清新', '简洁直接']
        
        # 保存文件并处理
        filename, save_path = caption_service.save_uploaded_file(file)
        
        # 生成文案
        result = caption_service.process_image(save_path, styles)
        
        # 添加图片URL
        if result['success']:
            result['image_url'] = f'/static/uploads/{filename}'
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@main_bp.route('/static/uploads/<filename>')
def uploaded_file(filename):
    """提供上传的图片"""
    return send_from_directory('static/uploads', filename)