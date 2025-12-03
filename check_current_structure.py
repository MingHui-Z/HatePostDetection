import os
import json


def check_current_structure():
    """检查当前目录结构"""
    print("当前工作目录:", os.getcwd())
    print("\n检查datasets目录结构:")

    datasets_path = "datasets"
    if os.path.exists(datasets_path):
        for root, dirs, files in os.walk(datasets_path):
            level = root.replace(datasets_path, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                if file.endswith('.json'):
                    print(f"{subindent}{file}")
    else:
        print("datasets目录不存在")


check_current_structure()