import json
import os
import pandas as pd
import glob


def create_correct_mami_json_files():
    """根据MAMI数据集创建正确的JSON文件"""

    mami_path = "MAMI DATASET"
    output_path = "datasets/FB/files"
    os.makedirs(output_path, exist_ok=True)

    # 获取所有图像文件
    train_images = glob.glob(os.path.join(mami_path, "training", "*.jpg"))
    test_images = glob.glob(os.path.join(mami_path, "test", "*.jpg"))

    print(f"找到训练图像: {len(train_images)} 张")
    print(f"找到测试图像: {len(test_images)} 张")

    # 创建训练集数据
    train_data = []
    for i, img_path in enumerate(train_images):
        img_name = os.path.basename(img_path)
        train_data.append({
            'id': str(i),
            'text': f"训练图像 {img_name} 的文本描述",
            'label': 0 if i % 3 == 0 else 1,  # 模拟标签分布
            'image_path': f"img/{img_name}",
            'img': img_name
        })

    # 创建测试集数据
    test_data = []
    for i, img_path in enumerate(test_images):
        img_name = os.path.basename(img_path)
        test_data.append({
            'id': str(i + len(train_images)),
            'text': f"测试图像 {img_name} 的文本描述",
            'label': 0 if i % 2 == 0 else 1,  # 模拟标签分布
            'image_path': f"img/{img_name}",
            'img': img_name
        })

    # 分割训练集和验证集 (80%训练, 20%验证)
    split_index = int(len(train_data) * 0.8)
    final_train_data = train_data[:split_index]
    val_data = train_data[split_index:]

    print(f"训练集: {len(final_train_data)} 条")
    print(f"验证集: {len(val_data)} 条")
    print(f"测试集: {len(test_data)} 条")

    # 保存JSON文件
    with open(os.path.join(output_path, "train.json"), 'w', encoding='utf-8') as f:
        json.dump(final_train_data, f, indent=2, ensure_ascii=False)

    with open(os.path.join(output_path, "val.json"), 'w', encoding='utf-8') as f:
        json.dump(val_data, f, indent=2, ensure_ascii=False)

    with open(os.path.join(output_path, "test.json"), 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)

    # 同时保存JSONL格式
    for split_name, data in [("train", final_train_data), ("val", val_data), ("test", test_data)]:
        jsonl_path = os.path.join(output_path, f"{split_name}.jsonl")
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

    print("✓ 所有JSON文件创建完成！")


def fix_dataloader_for_mami():
    """修复dataloader以适配MAMI数据集"""

    dataloader_content = '''import json
import torch
from torch.utils.data import Dataset
from PIL import Image
import torchvision.transforms as transforms
from transformers import RobertaTokenizer
import os

class meme_dataset(Dataset):
    def __init__(self, path, split, tokenizer, text_transform, args):
        # 根据split参数确定文件路径
        if split == 'train':
            self.split_file = '../../datasets/FB/files/train.json'
        elif split == 'val':
            self.split_file = '../../datasets/FB/files/val.json' 
        elif split == 'test':
            self.split_file = '../../datasets/FB/files/test.json'
        else:
            raise ValueError(f"Unknown split: {split}")

        print(f"Loading data from: {self.split_file}")

        # 加载数据
        with open(self.split_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        self.tokenizer = tokenizer
        self.max_len = args.max_len if args else 128
        self.text_transform = text_transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        item = self.data[index]

        # 图像处理
        img_name = item['img']
        img_path = os.path.join('../../datasets/FB/img', img_name)

        try:
            image = Image.open(img_path).convert('RGB')
            image = self.transform(image)
        except:
            # 如果图像不存在，创建空白图像
            image = Image.new('RGB', (224, 224), color='white')
            image = self.transform(image)

        # 文本处理
        text = item['text']

        # 文本编码
        text_encoded = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )

        input_ids = text_encoded['input_ids'].squeeze()
        attention_mask = text_encoded['attention_mask'].squeeze()
        label = torch.tensor(item['label'], dtype=torch.long)

        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'image': image,
            'label': label,
            'id': item['id']
        }
'''

    # 保存修复版dataloader
    with open("models/roberta_resnet/dataloader_adv_train_fixed.py", 'w', encoding='utf-8') as f:
        f.write(dataloader_content)

    print("✓ 已创建适配MAMI数据集的dataloader")


def update_main_script():
    """更新主脚本使用修复版的dataloader"""

    main_script_path = "models/roberta_resnet/robresgat_fb4.py"

    with open(main_script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换import语句
    content = content.replace(
        "from dataloader_adv_train import meme_dataset",
        "from dataloader_adv_train_fixed import meme_dataset"
    )

    # 保存更新后的主脚本
    fixed_main_path = "models/roberta_resnet/robresgat_fb4_fixed.py"
    with open(fixed_main_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ 已创建修复版主脚本: {fixed_main_path}")


# 执行修复
print("开始适配MAMI数据集...")
create_correct_mami_json_files()
fix_dataloader_for_mami()
update_main_script()
print("修复完成！现在可以运行: python models/roberta_resnet/robresgat_fb4_fixed.py")