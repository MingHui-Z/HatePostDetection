import json
import os


def create_missing_json_files():
    """创建所有缺失的JSON文件"""

    print("\n创建缺失的JSON文件...")

    # 目标路径
    target_dir = "datasets/fb/files"
    os.makedirs(target_dir, exist_ok=True)

    # 创建train.json
    train_data = [
        {
            "id": str(i),
            "text": f"训练样本文本 {i}",
            "label": i % 2,
            "img": f"{10000 + i}.jpg",
            "image_path": f"img/{10000 + i}.jpg"
        }
        for i in range(100)
    ]

    with open(os.path.join(target_dir, "train.json"), 'w', encoding='utf-8') as f:
        json.dump(train_data, f, indent=2, ensure_ascii=False)
    print("✓ 已创建 train.json")

    # 创建val.json
    val_data = [
        {
            "id": str(i + 100),
            "text": f"验证样本文本 {i}",
            "label": (i + 1) % 2,
            "img": f"{20000 + i}.jpg",
            "image_path": f"img/{20000 + i}.jpg"
        }
        for i in range(20)
    ]

    with open(os.path.join(target_dir, "val.json"), 'w', encoding='utf-8') as f:
        json.dump(val_data, f, indent=2, ensure_ascii=False)
    print("✓ 已创建 val.json")

    # 创建test.json
    test_data = [
        {
            "id": str(i + 120),
            "text": f"测试样本文本 {i}",
            "label": (i + 2) % 2,
            "img": f"{30000 + i}.jpg",
            "image_path": f"img/{30000 + i}.jpg"
        }
        for i in range(30)
    ]

    with open(os.path.join(target_dir, "test.json"), 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    print("✓ 已创建 test.json")


create_missing_json_files()