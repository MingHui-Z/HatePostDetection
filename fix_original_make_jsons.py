def fix_original_make_jsons():
    """直接修复原始的make_jsons_fb.py文件"""

    original_file = "C:/Users/lunor/Desktop/yan1/HatePostDetection/make_jsons_fb.py"

    # 备份原始文件
    backup_file = original_file + ".backup"

    try:
        # 读取原始内容
        with open(original_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 创建备份
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)

        # 修复关键行：将 'img' 改为 'image_path'
        old_line = "dict_temp['img'] = point['img'].split('/')[-1]"
        new_line = "dict_temp['img'] = point['image_path'].split('/')[-1]"

        if old_line in content:
            content = content.replace(old_line, new_line)
            print(f"已修复行: {old_line} -> {new_line}")
        else:
            # 如果格式稍有不同，尝试其他可能的写法
            variations = [
                ("point['img']", "point['image_path']"),
                ('point["img"]', 'point["image_path"]'),
                ("point.get('img')", "point.get('image_path')")
            ]

            for old_var, new_var in variations:
                if old_var in content:
                    content = content.replace(old_var, new_var)
                    print(f"已修复: {old_var} -> {new_var}")
                    break

        # 写回修复后的内容
        with open(original_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"原始文件已修复并备份到: {backup_file}")

    except Exception as e:
        print(f"修复文件出错: {e}")


fix_original_make_jsons()