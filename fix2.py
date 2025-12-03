import os


def fix_syntax_error():
    """修复语法错误"""

    print("修复语法错误...")

    script_path = "models/roberta_resnet/robresgat_fb4_simple.py"

    # 读取文件内容
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 查找第460行附近的代码
    lines = content.split('\n')

    print("检查第455-465行代码:")
    for i in range(454, 466):  # 查看455-465行
        if i < len(lines):
            print(f"行 {i + 1}: {lines[i]}")

    # 修复字符串未闭合的问题
    # 查找未闭合的print语句
    for i, line in enumerate(lines):
        if 'print("' in line and not line.strip().endswith('")'):
            # 找到未闭合的字符串
            print(f"发现未闭合字符串在第 {i + 1} 行: {line}")

            # 修复这一行
            if 'print("Skipping SMOTE' in line:
                lines[i] = '    print("Skipping SMOTE data augmentation due to compatibility issues...")'
            elif 'print("Applying incremental SMOTE' in line:
                lines[i] = '    print("Applying incremental SMOTE to training dataset...")'

    # 重新组合内容
    fixed_content = '\n'.join(lines)

    # 保存修复后的文件
    fixed_path = "models/roberta_resnet/robresgat_fb4_simple_fixed.py"
    with open(fixed_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    print(f"✓ 语法错误已修复: {fixed_path}")
    return fixed_path


def create_clean_version():
    """创建干净的版本，重新生成简化版"""

    print("\n创建干净的简化版本...")

    # 从原始文件开始
    original_path = "models/roberta_resnet/robresgat_fb4_final.py"

    with open(original_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 安全地移除SMOTE相关代码
    import re

    # 移除SMOTE类定义
    content = re.sub(r'class IncrementalSMOTEMemeDataset.*?^def',
                     'def', content, flags=re.DOTALL | re.MULTILINE)

    # 移除SMOTE应用代码，直接使用原始训练集
    smote_application = '''
    # 跳过SMOTE数据增强
    print("Skipping SMOTE data augmentation, using original training set...")

    # 使用原始训练集
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=args.workers)
    '''

    # 替换SMOTE相关代码
    old_smote_code = '''print("Applying incremental SMOTE to training dataset...")
    print("Preparing dataset for SMOTE...")

    smote_train_dataset = IncrementalSMOTEMemeDataset(train_dataset, n_components=100, batch_size=100)
    train_loader = DataLoader(smote_train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=args.workers)'''

    content = content.replace(old_smote_code, smote_application)

    # 保存干净的版本
    clean_path = "models/roberta_resnet/robresgat_fb4_clean.py"
    with open(clean_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ 已创建干净版本: {clean_path}")
    return clean_path


def create_minimal_working_version():
    """创建最小可工作版本"""

    print("\n创建最小可工作版本...")

    minimal_code = '''import os
import sys
import torch
import torch.nn as nn
import argparse
from torch.utils.data import DataLoader
from transformers import RobertaModel, RobertaTokenizer
import torchvision.models as models
from dataloader_adv_train_fixed import meme_dataset

# 添加项目根目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def main():
    # 基本配置
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch_size', type=int, default=8)
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--max_len', type=int, default=128)
    parser.add_argument('--epochs', type=int, default=5)
    args = parser.parse_args([])  # 使用空列表避免命令行参数

    # 初始化tokenizer
    TOKENIZER = RobertaTokenizer.from_pretrained('roberta-base')

    # 数据集路径
    dataset_name = "fb"

    print("Loading datasets...")

    # 加载数据集
    train_dataset = meme_dataset(dataset_name, 'train', TOKENIZER, None, args)
    val_dataset = meme_dataset(dataset_name, 'val', TOKENIZER, None, args)
    test_dataset = meme_dataset(dataset_name, 'test', TOKENIZER, None, args)

    print(f"Train dataset size: {len(train_dataset)}")
    print(f"Val dataset size: {len(val_dataset)}")
    print(f"Test dataset size: {len(test_dataset)}")

    # 创建数据加载器
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=args.workers)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False, num_workers=args.workers)
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False, num_workers=args.workers)

    print("Data loaders created successfully!")

    # 简单的模型测试
    print("Testing with one batch...")

    for batch in train_loader:
        print("Batch keys:", batch.keys())
        print("Input IDs shape:", batch['input_ids'].shape)
        print("Images shape:", batch['image'].shape)
        print("Labels:", batch['label'])
        break

    print("Program completed successfully!")

if __name__ == "__main__":
    main()
'''

    minimal_path = "models/roberta_resnet/robresgat_fb4_minimal_test.py"
    with open(minimal_path, 'w', encoding='utf-8') as f:
        f.write(minimal_code)

    print(f"✓ 已创建最小测试版本: {minimal_path}")
    return minimal_path


# 执行修复
print("=" * 60)
print("修复语法错误并创建可运行版本")
print("=" * 60)

# 1. 修复语法错误
fixed_version = fix_syntax_error()

# 2. 创建干净版本
clean_version = create_clean_version()

# 3. 创建最小测试版本
minimal_version = create_minimal_working_version()

print("\n" + "=" * 60)
print("修复完成！")
print("=" * 60)
print("可以尝试运行以下版本：")
print(f"1. 语法修复版: python {fixed_version}")
print(f"2. 干净版本: python {clean_version}")
print(f"3. 最小测试版: python {minimal_version}")
print("\n推荐运行顺序：")
print("1. 先运行最小测试版确认基础功能")
print("2. 然后运行干净版本进行完整训练")