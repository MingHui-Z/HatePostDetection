import shutil
import glob
import os


def copy_mami_images():
    """复制MAMI数据集的图像文件到FB/img目录"""

    mami_path = "MAMI DATASET"
    img_dest = "datasets/FB/img"
    os.makedirs(img_dest, exist_ok=True)

    copied_count = 0

    # 复制训练图像
    train_src = os.path.join(mami_path, "training")
    if os.path.exists(train_src):
        train_images = glob.glob(os.path.join(train_src, "*.jpg"))
        for img_path in train_images:
            img_name = os.path.basename(img_path)
            dest_path = os.path.join(img_dest, img_name)
            if not os.path.exists(dest_path):
                shutil.copy2(img_path, dest_path)
                copied_count += 1

    # 复制测试图像
    test_src = os.path.join(mami_path, "test")
    if os.path.exists(test_src):
        test_images = glob.glob(os.path.join(test_src, "*.jpg"))
        for img_path in test_images:
            img_name = os.path.basename(img_path)
            dest_path = os.path.join(img_dest, img_name)
            if not os.path.exists(dest_path):
                shutil.copy2(img_path, dest_path)
                copied_count += 1

    print(f"✓ 已复制 {copied_count} 张图像到 {img_dest}")


copy_mami_images()