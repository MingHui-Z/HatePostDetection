import json
import os
import subprocess
import sys


def create_complete_fix():
    """创建完整的修复方案"""

    # 1. 首先修复原始make_jsons_fb.py文件
    fix_original_script()

    # 2. 创建修正版脚本作为备用
    create_corrected_version()

    # 3. 测试运行
    test_fixed_script()


def fix_original_script():
    """修复原始的make_jsons_fb.py文件"""
    print("=" * 60)
    print("步骤1: 修复原始make_jsons_fb.py文件")
    print("=" * 60)

    original_file = "make_jsons_fb.py"
    backup_file = "make_jsons_fb.py.backup"

    if not os.path.exists(original_file):
        print(f"错误: 找不到文件 {original_file}")
        return

    try:
        # 读取原始内容
        with open(original_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 创建备份
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 已创建备份: {backup_file}")

        # 修复关键行
        old_line = "dict_temp['img'] = point['img'].split('/')[-1]"
        new_line = "dict_temp['img'] = point['image_path'].split('/')[-1]"

        if old_line in content:
            content = content.replace(old_line, new_line)
            print(f"✓ 已修复: {old_line} -> {new_line}")
        else:
            # 查找类似的代码模式
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "point['img']" in line or 'point["img"]' in line:
                    print(f"找到相关行 {i + 1}: {line.strip()}")
                    # 简单替换img为image_path
                    content = content.replace("point['img']", "point['image_path']")
                    content = content.replace('point["img"]', 'point["image_path"]')
                    print("✓ 已修复字段引用")
                    break

        # 写回修复后的内容
        with open(original_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print("✓ 原始文件修复完成")

    except Exception as e:
        print(f"✗ 修复文件出错: {e}")


def create_corrected_version():
    """创建修正版脚本作为备用"""
    print("\n" + "=" * 60)
    print("步骤2: 创建修正版脚本作为备用")
    print("=" * 60)

    corrected_script = '''import json
import os

def main():
    """处理JSON文件，适配你的数据格式"""

    # 输入文件路径
    input_file = 'datasets/FB/files/test.jsonl'

    # 输出文件路径
    output_file = 'datasets/FB/files/processed_test.json'

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    try:
        # 读取JSONL文件
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        print(f"读取到 {len(lines)} 行数据")

        processed_data = []
        success_count = 0

        for line_num, line in enumerate(lines):
            try:
                point = json.loads(line.strip())

                # 创建处理后的字典
                dict_temp = {}

                # 图像字段映射：将 image_path 映射为 img
                if 'image_path' in point:
                    img_path = point['image_path']
                    if '/' in img_path:
                        dict_temp['img'] = img_path.split('/')[-1]
                    else:
                        dict_temp['img'] = img_path
                    success_count += 1
                else:
                    # 如果没有image_path，使用默认值
                    dict_temp['img'] = f"{point.get('id', str(line_num))}.jpg"

                # 其他字段
                dict_temp['text'] = point.get('text', '')
                dict_temp['label'] = point.get('label', 0)
                dict_temp['id'] = point.get('id', str(line_num))

                processed_data.append(dict_temp)

            except json.JSONDecodeError as e:
                print(f"第 {line_num + 1} 行JSON解析错误: {e}")
                continue

        # 保存处理后的数据
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)

        print(f"✓ 成功处理 {success_count}/{len(lines)} 条记录")
        print(f"✓ 输出文件: {output_file}")

        # 显示示例
        if processed_data:
            print("\\n前3条处理后的数据:")
            for i, item in enumerate(processed_data[:3]):
                print(f"  {i+1}: {item}")

        return True

    except FileNotFoundError:
        print(f"✗ 找不到输入文件: {input_file}")
        return False
    except Exception as e:
        print(f"✗ 处理过程中出错: {e}")
        return False

if __name__ == "__main__":
    main()
'''

    with open("make_jsons_fb_corrected.py", 'w', encoding='utf-8') as f:
        f.write(corrected_script)

    print("✓ 已创建修正版脚本: make_jsons_fb_corrected.py")


def test_fixed_script():
    """测试修复后的脚本"""
    print("\n" + "=" * 60)
    print("步骤3: 测试修复后的脚本")
    print("=" * 60)

    # 首先检查test.jsonl文件是否存在
    test_jsonl_path = "datasets/FB/files/test.jsonl"
    if not os.path.exists(test_jsonl_path):
        print(f"✗ 找不到测试文件: {test_jsonl_path}")
        print("请确保test.jsonl文件存在")
        return

    print("✓ 找到test.jsonl文件")

    # 测试修正版脚本
    print("\n测试修正版脚本...")
    try:
        result = subprocess.run([
            sys.executable,
            "make_jsons_fb_corrected.py"
        ], capture_output=True, text=True, cwd=os.getcwd())

        print("输出结果:")
        print(result.stdout)
        if result.stderr:
            print("错误信息:")
            print(result.stderr)

        if result.returncode == 0:
            print("✓ 修正版脚本运行成功!")
        else:
            print("✗ 修正版脚本运行失败")

    except Exception as e:
        print(f"✗ 运行修正版脚本出错: {e}")

    # 测试原始脚本（修复后）
    print("\n测试原始脚本（修复后）...")
    try:
        result = subprocess.run([
            sys.executable,
            "make_jsons_fb.py"
        ], capture_output=True, text=True, cwd=os.getcwd())

        print("输出结果:")
        print(result.stdout)
        if result.stderr:
            print("错误信息:")
            print(result.stderr)

        if result.returncode == 0:
            print("✓ 原始脚本（修复后）运行成功!")
        else:
            print("✗ 原始脚本（修复后）运行失败")

    except Exception as e:
        print(f"✗ 运行原始脚本出错: {e}")


def verify_output():
    """验证输出文件"""
    print("\n" + "=" * 60)
    print("步骤4: 验证输出文件")
    print("=" * 60)

    output_file = "datasets/FB/files/processed_test.json"

    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                processed_data = json.load(f)

            print(f"✓ 找到输出文件，包含 {len(processed_data)} 条记录")

            if processed_data:
                print("\n输出文件前3条记录:")
                for i, item in enumerate(processed_data[:3]):
                    print(f"  {i + 1}: {item}")

                # 检查字段
                first_item = processed_data[0]
                required_fields = ['img', 'text', 'label', 'id']
                missing_fields = [f for f in required_fields if f not in first_item]

                if not missing_fields:
                    print("✓ 所有必需字段都存在")
                else:
                    print(f"✗ 缺少字段: {missing_fields}")
            else:
                print("✗ 输出文件为空")

        except Exception as e:
            print(f"✗ 读取输出文件出错: {e}")
    else:
        print(f"✗ 输出文件不存在: {output_file}")


# 运行完整的修复流程
if __name__ == "__main__":
    print("开始修复make_jsons_fb.py脚本...")
    print("当前工作目录:", os.getcwd())
    print()

    create_complete_fix()
    verify_output()

    print("\n" + "=" * 60)
    print("修复完成！")
    print("=" * 60)
    print("\n下一步操作建议:")
    print("1. 如果修正版脚本运行成功，可以使用它")
    print("2. 如果原始脚本修复后也能运行，可以继续使用原始脚本")
    print("3. 检查生成的processed_test.json文件是否符合预期")