# test_simple.py
import sys
sys.path.append('.')
from app.models.simple_generator import SimpleTextGenerator

generator = SimpleTextGenerator()
description = "树枝上有白花"
styles = ["幽默搞笑", "文艺清新", "简洁直接", "诗意抒情"]

print(f"图片描述：{description}\n")
for style in styles:
    result = generator.generate_caption(description, style)
    print(f"{style}：{result}")