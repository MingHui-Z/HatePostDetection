def fix_dataloader_path_issue():
    """修复dataloader中的路径问题"""

    dataloader_path = "models/roberta_resnet/dataloader_adv_train.py"

    print(f"\n修复 {dataloader_path} ...")

    with open(dataloader_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 显示有问题的代码行
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'split_file' in line and 'open' in line:
            print(f"第 {i + 1} 行: {line.strip()}")

    # 修复路径拼接问题（Windows反斜杠问题）
    old_code = """
        split_file = os.path.join(data_path, 'files', split+'.json')
        with open(split_file,'r') as f:
"""

    new_code = """
        split_file = os.path.join(data_path, 'files', split+'.json')
        # 修复Windows路径问题
        split_file = split_file.replace('\\\\', '/')
        with open(split_file,'r') as f:
"""

    if old_code.strip() in content:
        content = content.replace(old_code, new_code)
        print("✓ 已修复路径拼接问题")

    # 保存修复后的文件
    fixed_path = "models/roberta_resnet/dataloader_adv_train_fixed.py"
    with open(fixed_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ 已保存修复版: {fixed_path}")

    return fixed_path


fixed_dataloader = fix_dataloader_path_issue()