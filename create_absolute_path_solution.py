import os


def create_absolute_path_solution():
    """创建使用绝对路径的解决方案"""

    print("\n创建绝对路径解决方案...")

    solution_code = '''import os
import sys
import json

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def get_absolute_path(relative_path):
    """将相对路径转换为绝对路径"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_path = os.path.join(base_dir, relative_path)
    # 标准化路径（解决Windows反斜杠问题）
    absolute_path = os.path.normpath(absolute_path)
    return absolute_path

# 测试路径
test_paths = [
    "../../datasets/fb/files/train.json",
    "../../datasets/fb/files/val.json", 
    "../../datasets/fb/files/test.json"
]

print("路径检查:")
for rel_path in test_paths:
    abs_path = get_absolute_path(rel_path)
    exists = os.path.exists(abs_path)
    status = "✓ 存在" if exists else "✗ 缺失"
    print(f"{status}: {abs_path}")

if all(os.path.exists(get_absolute_path(p)) for p in test_paths):
    print("所有文件都存在，可以运行主程序")
else:
    print("有些文件缺失，需要创建")
'''

    with open("path_check.py", 'w', encoding='utf-8') as f:
        f.write(solution_code)

    print("✓ 已创建路径检查脚本")

    # 运行路径检查
    print("\n运行路径检查...")
    os.system("python path_check.py")


create_absolute_path_solution()